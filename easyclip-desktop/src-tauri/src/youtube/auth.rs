//! Google OAuth 2.0 for native apps: loopback redirect + PKCE.
//!
//! Deliberately *not* the deprecated OOB flow and *not* an embedded webview —
//! Google blocks embedded webviews for sign-in. The system browser is opened
//! instead, and a short-lived loopback listener on 127.0.0.1 catches the
//! redirect.

use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
use rand::RngCore;
use sha2::{Digest, Sha256};
use std::{
    io::{BufRead, BufReader, Write},
    net::{TcpListener, TcpStream},
    time::Duration,
};

use super::parse::{percent_decode, percent_encode};

pub const SCOPES: &str = concat!(
    "https://www.googleapis.com/auth/youtube.upload ",
    "https://www.googleapis.com/auth/youtube.readonly ",
    "https://www.googleapis.com/auth/userinfo.profile"
);

const AUTH_ENDPOINT: &str = "https://accounts.google.com/o/oauth2/v2/auth";
pub const TOKEN_ENDPOINT: &str = "https://oauth2.googleapis.com/token";

/// The PKCE pair for a single sign-in attempt.
#[derive(Debug, Clone)]
pub struct Pkce {
    pub verifier: String,
    pub challenge: String,
}

/// Generate a URL-safe random string of `length` characters.
fn random_token(length: usize) -> String {
    let mut bytes = vec![0u8; length];
    rand::rngs::OsRng.fill_bytes(&mut bytes);
    let encoded = URL_SAFE_NO_PAD.encode(&bytes);
    encoded.chars().take(length).collect()
}

/// Derive the S256 challenge for a verifier, per RFC 7636.
pub fn derive_challenge(verifier: &str) -> String {
    let digest = Sha256::digest(verifier.as_bytes());
    URL_SAFE_NO_PAD.encode(digest)
}

impl Pkce {
    pub fn generate() -> Self {
        // RFC 7636 allows 43..=128 characters; 64 is comfortably inside that.
        let verifier = random_token(64);
        let challenge = derive_challenge(&verifier);
        Self {
            verifier,
            challenge,
        }
    }
}

/// Build the Google consent URL.
pub fn build_auth_url(client_id: &str, redirect_uri: &str, challenge: &str, state: &str) -> String {
    format!(
        "{AUTH_ENDPOINT}?client_id={}&redirect_uri={}&response_type=code&scope={}&code_challenge={}&code_challenge_method=S256&state={}&access_type=offline&prompt=consent",
        percent_encode(client_id),
        percent_encode(redirect_uri),
        percent_encode(SCOPES),
        percent_encode(challenge),
        percent_encode(state),
    )
}

/// Pull `code` / `state` / `error` out of the first line of an HTTP request.
///
/// The request line looks like `GET /?code=…&state=… HTTP/1.1`.
pub fn parse_redirect_query(request_line: &str) -> Result<(String, String), String> {
    let path = request_line
        .split_whitespace()
        .nth(1)
        .ok_or_else(|| "Malformed redirect request".to_owned())?;
    let query = path.split_once('?').map(|(_, q)| q).unwrap_or("");

    let mut code = None;
    let mut state = None;
    let mut error = None;
    for pair in query.split('&') {
        if let Some((key, value)) = pair.split_once('=') {
            match key {
                "code" => code = Some(percent_decode(value)),
                "state" => state = Some(percent_decode(value)),
                "error" => error = Some(percent_decode(value)),
                _ => {}
            }
        }
    }

    if let Some(error) = error {
        return Err(match error.as_str() {
            "access_denied" => "Sign-in was cancelled in the browser".to_owned(),
            other => format!("Google returned an error: {other}"),
        });
    }
    match (code, state) {
        (Some(code), Some(state)) => Ok((code, state)),
        _ => Err("The redirect did not contain an authorisation code".to_owned()),
    }
}

fn respond(stream: &mut TcpStream, body: &str) {
    let response = format!(
        "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
        body.as_bytes().len(),
        body
    );
    let _ = stream.write_all(response.as_bytes());
    let _ = stream.flush();
}

fn success_page() -> String {
    // Bilingual, self-contained, no external assets.
    r#"<!doctype html><html><head><meta charset="utf-8"><title>EasyClip</title>
<style>body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#0c0c10;color:#eee;font-family:Segoe UI,Tahoma,sans-serif}
.card{text-align:center;border:1px solid #2a2a33;background:#121218;border-radius:16px;padding:44px 54px}
.tick{width:56px;height:56px;border-radius:50%;background:#1c3a17;color:#79dc50;display:flex;align-items:center;justify-content:center;font-size:30px;margin:0 auto 18px}
h1{font-size:17px;margin:0 0 8px}p{font-size:12px;color:#8a8a95;margin:4px 0}</style></head>
<body><div class="card"><div class="tick">&#10003;</div>
<h1>EasyClip is connected</h1><p>You can close this tab and return to the app.</p>
<p dir="rtl">حساب گوگل شما متصل شد. این صفحه را ببندید و به برنامه بازگردید.</p>
</div></body></html>"#
        .to_owned()
}

fn failure_page(message: &str) -> String {
    format!(
        r#"<!doctype html><html><head><meta charset="utf-8"><title>EasyClip</title>
<style>body{{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#0c0c10;color:#eee;font-family:Segoe UI,Tahoma,sans-serif}}
.card{{text-align:center;border:1px solid #4c2525;background:#161016;border-radius:16px;padding:44px 54px;max-width:420px}}
h1{{font-size:17px;margin:0 0 10px;color:#f28787}}p{{font-size:12px;color:#8a8a95}}</style></head>
<body><div class="card"><h1>Sign-in failed</h1><p>{}</p>
<p dir="rtl">ورود ناموفق بود. به برنامه بازگردید و دوباره تلاش کنید.</p></div></body></html>"#,
        message.replace('<', "").replace('>', "")
    )
}

/// A loopback listener bound to an ephemeral port on 127.0.0.1.
pub struct LoopbackServer {
    listener: TcpListener,
    port: u16,
}

impl LoopbackServer {
    pub fn bind() -> Result<Self, String> {
        let listener = TcpListener::bind("127.0.0.1:0")
            .map_err(|error| format!("Cannot open a local sign-in port: {error}"))?;
        let port = listener
            .local_addr()
            .map_err(|error| format!("Cannot read the local sign-in port: {error}"))?
            .port();
        Ok(Self { listener, port })
    }

    pub fn redirect_uri(&self) -> String {
        format!("http://127.0.0.1:{}", self.port)
    }

    /// Block until the browser hits the redirect, then return the auth code.
    ///
    /// Browsers commonly also request `/favicon.ico`; those are answered and
    /// ignored so they cannot consume the single real redirect.
    pub fn wait_for_code(self, expected_state: &str, timeout: Duration) -> Result<String, String> {
        self.listener
            .set_nonblocking(false)
            .map_err(|error| format!("Sign-in listener error: {error}"))?;

        let deadline = std::time::Instant::now() + timeout;
        for incoming in self.listener.incoming() {
            if std::time::Instant::now() > deadline {
                return Err("Sign-in timed out. Please try again.".to_owned());
            }
            let mut stream = match incoming {
                Ok(stream) => stream,
                Err(_) => continue,
            };
            let _ = stream.set_read_timeout(Some(Duration::from_secs(10)));

            let mut reader = BufReader::new(
                stream
                    .try_clone()
                    .map_err(|error| format!("Sign-in listener error: {error}"))?,
            );
            let mut request_line = String::new();
            if reader.read_line(&mut request_line).is_err() {
                continue;
            }

            if request_line.contains("/favicon.ico") {
                respond(&mut stream, "");
                continue;
            }

            return match parse_redirect_query(&request_line) {
                Ok((code, state)) => {
                    if state != expected_state {
                        respond(&mut stream, &failure_page("State mismatch."));
                        Err("Sign-in failed a security check (state mismatch)".to_owned())
                    } else {
                        respond(&mut stream, &success_page());
                        Ok(code)
                    }
                }
                Err(message) => {
                    respond(&mut stream, &failure_page(&message));
                    Err(message)
                }
            };
        }
        Err("Sign-in did not complete".to_owned())
    }
}

/// Generate an opaque anti-CSRF state value.
pub fn generate_state() -> String {
    random_token(32)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn derives_challenge_from_rfc7636_vector() {
        // The worked example from RFC 7636 Appendix B.
        let verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk";
        assert_eq!(
            derive_challenge(verifier),
            "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
        );
    }

    #[test]
    fn generated_verifier_is_rfc_compliant_length() {
        let pkce = Pkce::generate();
        let length = pkce.verifier.chars().count();
        assert!(
            (43..=128).contains(&length),
            "verifier length {length} outside RFC 7636 range"
        );
        assert_eq!(pkce.challenge, derive_challenge(&pkce.verifier));
    }

    #[test]
    fn generated_verifiers_are_unique() {
        assert_ne!(Pkce::generate().verifier, Pkce::generate().verifier);
    }

    #[test]
    fn builds_auth_url_with_encoded_parameters() {
        let url = build_auth_url("client-id", "http://127.0.0.1:5123", "chal", "st4te");
        assert!(url.starts_with(AUTH_ENDPOINT));
        assert!(url.contains("client_id=client-id"));
        assert!(url.contains("redirect_uri=http%3A%2F%2F127.0.0.1%3A5123"));
        assert!(url.contains("code_challenge=chal"));
        assert!(url.contains("code_challenge_method=S256"));
        assert!(url.contains("state=st4te"));
        assert!(url.contains("access_type=offline"));
        assert!(url.contains("prompt=consent"));
        // Scopes must be encoded, so raw spaces must not survive.
        assert!(!url.contains("auth/youtube.upload https"));
    }

    #[test]
    fn parses_successful_redirect() {
        let line = "GET /?code=4%2F0Axyz&state=abc123 HTTP/1.1";
        let (code, state) = parse_redirect_query(line).unwrap();
        assert_eq!(code, "4/0Axyz");
        assert_eq!(state, "abc123");
    }

    #[test]
    fn parses_denied_redirect() {
        let line = "GET /?error=access_denied&state=abc HTTP/1.1";
        let error = parse_redirect_query(line).unwrap_err();
        assert!(error.contains("cancelled"), "unexpected message: {error}");
    }

    #[test]
    fn rejects_redirect_without_code() {
        assert!(parse_redirect_query("GET / HTTP/1.1").is_err());
        assert!(parse_redirect_query("garbage").is_err());
    }

    #[test]
    fn binds_loopback_and_reports_uri() {
        let server = LoopbackServer::bind().unwrap();
        let uri = server.redirect_uri();
        assert!(uri.starts_with("http://127.0.0.1:"));
        assert!(server.port > 0);
    }
}
