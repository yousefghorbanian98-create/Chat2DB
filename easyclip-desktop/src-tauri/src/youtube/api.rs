//! Thin async client for the YouTube Data API v3 and Google's token endpoint.

use serde::{Deserialize, Serialize};
use std::time::Duration;

use super::parse::{
    format_duration, parse_iso8601_duration, percent_encode, uploads_playlist_for_channel,
    SourceRef,
};

const API_BASE: &str = "https://www.googleapis.com/youtube/v3";
const REQUEST_TIMEOUT: Duration = Duration::from_secs(45);

pub fn http_client() -> Result<reqwest::Client, String> {
    reqwest::Client::builder()
        .timeout(REQUEST_TIMEOUT)
        .user_agent("EasyClip-Desktop/0.3")
        .build()
        .map_err(|error| format!("Cannot create the HTTP client: {error}"))
}

#[derive(Debug, Clone, Deserialize)]
pub struct TokenResponse {
    pub access_token: String,
    #[serde(default)]
    pub refresh_token: Option<String>,
    #[serde(default)]
    pub expires_in: Option<u64>,
}

/// Exchange an authorisation code (with the PKCE verifier) for tokens.
pub async fn exchange_code(
    client: &reqwest::Client,
    client_id: &str,
    client_secret: &str,
    code: &str,
    verifier: &str,
    redirect_uri: &str,
) -> Result<TokenResponse, String> {
    let response = client
        .post(super::auth::TOKEN_ENDPOINT)
        .form(&[
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("code", code),
            ("code_verifier", verifier),
            ("grant_type", "authorization_code"),
            ("redirect_uri", redirect_uri),
        ])
        .send()
        .await
        .map_err(|error| format!("Token request failed: {error}"))?;

    let status = response.status();
    let body = response.text().await.unwrap_or_default();
    if !status.is_success() {
        return Err(describe_google_error(&body, status.as_u16()));
    }
    serde_json::from_str(&body).map_err(|error| format!("Malformed token response: {error}"))
}

/// Trade a refresh token for a fresh access token.
pub async fn refresh_access_token(
    client: &reqwest::Client,
    client_id: &str,
    client_secret: &str,
    refresh_token: &str,
) -> Result<TokenResponse, String> {
    let response = client
        .post(super::auth::TOKEN_ENDPOINT)
        .form(&[
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("refresh_token", refresh_token),
            ("grant_type", "refresh_token"),
        ])
        .send()
        .await
        .map_err(|error| format!("Token refresh failed: {error}"))?;

    let status = response.status();
    let body = response.text().await.unwrap_or_default();
    if !status.is_success() {
        if body.contains("invalid_grant") {
            return Err(
                "Your Google sign-in expired. While the OAuth app is in Testing mode Google \
                 invalidates refresh tokens after 7 days. Please connect again."
                    .to_owned(),
            );
        }
        return Err(describe_google_error(&body, status.as_u16()));
    }
    serde_json::from_str(&body).map_err(|error| format!("Malformed refresh response: {error}"))
}

/// Turn a Google error payload into something a human can act on.
pub fn describe_google_error(body: &str, status: u16) -> String {
    if let Ok(value) = serde_json::from_str::<serde_json::Value>(body) {
        let reason = value["error"]["errors"][0]["reason"]
            .as_str()
            .or_else(|| value["error"]["status"].as_str())
            .unwrap_or_default();
        let message = value["error"]["message"]
            .as_str()
            .or_else(|| value["error_description"].as_str())
            .or_else(|| value["error"].as_str())
            .unwrap_or("Unknown error");

        return match reason {
            "quotaExceeded" | "RESOURCE_EXHAUSTED" => {
                "Daily YouTube API quota exhausted. A default project allows about 6 uploads \
                 per day; the queue will resume after the quota resets at midnight Pacific time."
                    .to_owned()
            }
            "uploadLimitExceeded" => {
                "This channel hit YouTube's daily upload limit. Try again tomorrow.".to_owned()
            }
            "forbidden" | "PERMISSION_DENIED" => format!(
                "Google refused the request ({message}). Check that the YouTube Data API v3 is \
                 enabled and your account is listed as a Test user."
            ),
            "youtubeSignupRequired" => {
                "This Google account has no YouTube channel. Create one, then reconnect."
                    .to_owned()
            }
            _ => format!("Google API error {status}: {message}"),
        };
    }
    format!("Google API error {status}")
}

async fn get_json(
    client: &reqwest::Client,
    access_token: &str,
    url: &str,
) -> Result<serde_json::Value, String> {
    let response = client
        .get(url)
        .bearer_auth(access_token)
        .send()
        .await
        .map_err(|error| format!("Network request failed: {error}"))?;
    let status = response.status();
    let body = response.text().await.unwrap_or_default();
    if !status.is_success() {
        return Err(describe_google_error(&body, status.as_u16()));
    }
    serde_json::from_str(&body).map_err(|error| format!("Malformed API response: {error}"))
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ChannelInfo {
    pub id: String,
    pub title: String,
    pub thumbnail: String,
    pub subscriber_count: String,
    pub video_count: String,
    pub uploads_playlist: String,
}

/// The signed-in user's own channel.
pub async fn my_channel(
    client: &reqwest::Client,
    access_token: &str,
) -> Result<ChannelInfo, String> {
    let url = format!("{API_BASE}/channels?part=snippet,statistics,contentDetails&mine=true");
    let value = get_json(client, access_token, &url).await?;
    channel_from_json(&value).ok_or_else(|| {
        "This Google account does not have a YouTube channel yet. Create one and reconnect."
            .to_owned()
    })
}

/// Look up any channel by its id.
pub async fn channel_by_id(
    client: &reqwest::Client,
    access_token: &str,
    channel_id: &str,
) -> Result<ChannelInfo, String> {
    let url = format!(
        "{API_BASE}/channels?part=snippet,statistics,contentDetails&id={}",
        percent_encode(channel_id)
    );
    let value = get_json(client, access_token, &url).await?;
    channel_from_json(&value).ok_or_else(|| "That channel could not be found".to_owned())
}

pub fn channel_from_json(value: &serde_json::Value) -> Option<ChannelInfo> {
    let item = value["items"].as_array()?.first()?;
    Some(ChannelInfo {
        id: item["id"].as_str()?.to_owned(),
        title: item["snippet"]["title"].as_str().unwrap_or("").to_owned(),
        thumbnail: item["snippet"]["thumbnails"]["default"]["url"]
            .as_str()
            .unwrap_or("")
            .to_owned(),
        subscriber_count: item["statistics"]["subscriberCount"]
            .as_str()
            .unwrap_or("0")
            .to_owned(),
        video_count: item["statistics"]["videoCount"]
            .as_str()
            .unwrap_or("0")
            .to_owned(),
        uploads_playlist: item["contentDetails"]["relatedPlaylists"]["uploads"]
            .as_str()
            .unwrap_or("")
            .to_owned(),
    })
}

/// Resolve arbitrary user input to a concrete channel.
pub async fn resolve_channel(
    client: &reqwest::Client,
    access_token: &str,
    source: &SourceRef,
) -> Result<ChannelInfo, String> {
    match source {
        SourceRef::Channel(id) => channel_by_id(client, access_token, id).await,
        SourceRef::Video(id) => {
            let url = format!(
                "{API_BASE}/videos?part=snippet&id={}",
                percent_encode(id)
            );
            let value = get_json(client, access_token, &url).await?;
            let channel_id = value["items"][0]["snippet"]["channelId"]
                .as_str()
                .ok_or_else(|| "That video could not be found".to_owned())?;
            channel_by_id(client, access_token, channel_id).await
        }
        SourceRef::Handle(handle) => {
            let url = format!(
                "{API_BASE}/channels?part=snippet,statistics,contentDetails&forHandle=@{}",
                percent_encode(handle)
            );
            let value = get_json(client, access_token, &url).await?;
            match channel_from_json(&value) {
                Some(channel) => Ok(channel),
                None => Err(format!("No channel found for @{handle}")),
            }
        }
        SourceRef::LegacyName(name) => {
            let url = format!(
                "{API_BASE}/channels?part=snippet,statistics,contentDetails&forUsername={}",
                percent_encode(name)
            );
            let value = get_json(client, access_token, &url).await?;
            match channel_from_json(&value) {
                Some(channel) => Ok(channel),
                None => Err(format!(
                    "No channel found for the legacy name '{name}'. Try the @handle instead."
                )),
            }
        }
        SourceRef::Playlist(_) => {
            Err("Paste a channel or video link; playlists are listed directly".to_owned())
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct SourceVideo {
    pub id: String,
    pub title: String,
    pub published_at: String,
    pub thumbnail: String,
    pub duration_label: String,
    pub duration_seconds: u64,
    /// `true` when the video is Creative Commons and therefore safe to reuse.
    pub creative_commons: bool,
}

/// Page through a playlist and collect its video ids (cheap: 1 unit per page).
pub async fn playlist_video_ids(
    client: &reqwest::Client,
    access_token: &str,
    playlist_id: &str,
    max_videos: usize,
) -> Result<Vec<String>, String> {
    let mut ids = Vec::new();
    let mut page_token: Option<String> = None;

    loop {
        let mut url = format!(
            "{API_BASE}/playlistItems?part=contentDetails&maxResults=50&playlistId={}",
            percent_encode(playlist_id)
        );
        if let Some(token) = page_token.as_deref() {
            url.push_str(&format!("&pageToken={}", percent_encode(token)));
        }
        let value = get_json(client, access_token, &url).await?;
        if let Some(items) = value["items"].as_array() {
            for item in items {
                if let Some(id) = item["contentDetails"]["videoId"].as_str() {
                    ids.push(id.to_owned());
                }
            }
        }
        if ids.len() >= max_videos {
            ids.truncate(max_videos);
            break;
        }
        match value["nextPageToken"].as_str() {
            Some(token) => page_token = Some(token.to_owned()),
            None => break,
        }
    }
    Ok(ids)
}

/// Hydrate video ids into full metadata (50 per call, 1 unit each).
pub async fn videos_details(
    client: &reqwest::Client,
    access_token: &str,
    ids: &[String],
) -> Result<Vec<SourceVideo>, String> {
    let mut videos = Vec::new();
    for chunk in ids.chunks(50) {
        let url = format!(
            "{API_BASE}/videos?part=snippet,contentDetails,status&id={}",
            percent_encode(&chunk.join(","))
        );
        let value = get_json(client, access_token, &url).await?;
        if let Some(items) = value["items"].as_array() {
            for item in items {
                let seconds =
                    parse_iso8601_duration(item["contentDetails"]["duration"].as_str().unwrap_or(""));
                videos.push(SourceVideo {
                    id: item["id"].as_str().unwrap_or_default().to_owned(),
                    title: item["snippet"]["title"].as_str().unwrap_or("").to_owned(),
                    published_at: item["snippet"]["publishedAt"]
                        .as_str()
                        .unwrap_or("")
                        .to_owned(),
                    thumbnail: item["snippet"]["thumbnails"]["medium"]["url"]
                        .as_str()
                        .unwrap_or("")
                        .to_owned(),
                    duration_label: format_duration(seconds),
                    duration_seconds: seconds,
                    creative_commons: item["status"]["license"].as_str() == Some("creativeCommon"),
                });
            }
        }
    }
    Ok(videos)
}

/// List a channel's uploads, newest first.
pub async fn channel_videos(
    client: &reqwest::Client,
    access_token: &str,
    channel: &ChannelInfo,
    max_videos: usize,
) -> Result<Vec<SourceVideo>, String> {
    let playlist = if channel.uploads_playlist.is_empty() {
        uploads_playlist_for_channel(&channel.id)
            .ok_or_else(|| "Cannot determine the uploads playlist for that channel".to_owned())?
    } else {
        channel.uploads_playlist.clone()
    };
    let ids = playlist_video_ids(client, access_token, &playlist, max_videos).await?;
    if ids.is_empty() {
        return Ok(Vec::new());
    }
    videos_details(client, access_token, &ids).await
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn explains_quota_exhaustion_in_plain_language() {
        let body = r#"{"error":{"errors":[{"reason":"quotaExceeded"}],"message":"quota"}}"#;
        let message = describe_google_error(body, 403);
        assert!(message.contains("quota"));
        assert!(message.contains("6 uploads"));
    }

    #[test]
    fn explains_missing_channel() {
        let body = r#"{"error":{"errors":[{"reason":"youtubeSignupRequired"}],"message":"no channel"}}"#;
        assert!(describe_google_error(body, 401).contains("no YouTube channel"));
    }

    #[test]
    fn falls_back_for_unknown_shapes() {
        assert!(describe_google_error("not json", 500).contains("500"));
        let body = r#"{"error":{"message":"Bad thing"}}"#;
        assert!(describe_google_error(body, 400).contains("Bad thing"));
    }

    #[test]
    fn reads_channel_payloads() {
        let value: serde_json::Value = serde_json::from_str(
            r#"{"items":[{"id":"UCabc","snippet":{"title":"My Channel","thumbnails":{"default":{"url":"http://t"}}},
                "statistics":{"subscriberCount":"42","videoCount":"7"},
                "contentDetails":{"relatedPlaylists":{"uploads":"UUabc"}}}]}"#,
        )
        .unwrap();
        let channel = channel_from_json(&value).unwrap();
        assert_eq!(channel.id, "UCabc");
        assert_eq!(channel.title, "My Channel");
        assert_eq!(channel.subscriber_count, "42");
        assert_eq!(channel.uploads_playlist, "UUabc");
    }

    #[test]
    fn returns_none_for_empty_channel_list() {
        let value: serde_json::Value = serde_json::from_str(r#"{"items":[]}"#).unwrap();
        assert!(channel_from_json(&value).is_none());
    }
}
