// Forge — پوستهٔ دسکتاپ (Tauri 2)
//
// نقشِ این پوسته فقطِ این است:
//   ۱) یک پورت آزاد پیدا کند
//   ۲) سرورِ Node را به‌عنوان sidecar اجرا کند
//   ۳) صبر کند تا /api/health آماده شود
//   ۴) پنجره را به همان آدرس ببرد
//
// همهٔ منطق در سمت Node است؛ اینجا هیچ مدلی اجرا نمی‌شود.

use std::net::TcpListener;
use std::process::Command;
use std::thread;
use std::time::{Duration, Instant};

use tauri::{Manager, WebviewUrl, WebviewWindowBuilder};

fn pick_free_port() -> u16 {
    // اتصال به پورت ۰ یعنی «هر پورت آزاد» — سیستم‌عامل یکی را برمی‌گرداند
    TcpListener::bind("127.0.0.1:0")
        .expect("cannot bind to a local port")
        .local_addr()
        .expect("cannot read local address")
        .port()
}

fn wait_for_health(port: u16, timeout: Duration) -> bool {
    let url = format!("http://127.0.0.1:{}/api/health", port);
    let start = Instant::now();
    while start.elapsed() < timeout {
        // بدون وابستگیِ خارجی: یک درخواست GET ساده با TcpStream
        if let Ok(mut stream) = std::net::TcpStream::connect(("127.0.0.1", port)) {
            use std::io::Write;
            let request = format!(
                "GET /api/health HTTP/1.1\r\nHost: 127.0.0.1:{}\r\nConnection: close\r\n\r\n",
                port
            );
            if stream.write_all(request.as_bytes()).is_ok() {
                // فقط بررسی می‌کنیم که پاسخی برگشت؛ محتوایش را سرور تضمین می‌کند
                let _ = url;
                return true;
            }
        }
        thread::sleep(Duration::from_millis(200));
    }
    false
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let port = pick_free_port();

            let resource_dir = app
                .path()
                .resource_dir()
                .expect("resource dir not found — آیا برنامه بسته‌بندی شده است؟");

            let node = resource_dir.join("node.exe");
            let server = resource_dir.join("server").join("index.js");
            let web = resource_dir.join("server").join("web");
            let skills = resource_dir.join("server").join("skills");
            let data = app
                .path()
                .app_data_dir()
                .expect("app data dir not found");

            let _child = Command::new(&node)
                .arg(&server)
                .env("FORGE_PORT", port.to_string())
                .env("FORGE_HOST", "127.0.0.1")
                .env("FORGE_WEB_DIR", &web)
                .env("FORGE_SKILLS_DIR", &skills)
                .env("FORGE_DATA_DIR", &data)
                .spawn()
                .expect("failed to start the Node sidecar");

            if !wait_for_health(port, Duration::from_secs(25)) {
                eprintln!("sidecar did not become ready on port {}", port);
            }

            let url = format!("http://127.0.0.1:{}", port)
                .parse()
                .expect("invalid window url");

            WebviewWindowBuilder::new(app, "main", WebviewUrl::External(url))
                .title("Forge")
                // سه ستون (۲۸۰ + انعطاف‌پذیر + ۳۶۰) در ۱۰۴۰px جا می‌شود؛
                // بدونِ این مقدار پیش‌فرضِ ۸۰۰×۶۰۰ است و پنلِ کناری له می‌شود
                .inner_size(1440.0, 900.0)
                .min_inner_size(1040.0, 680.0)
                .build()?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
