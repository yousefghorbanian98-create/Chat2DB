import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * D-024 — نسخهٔ وب به‌عنوان PWA قابل نصب.
 *
 * «نصب‌پذیر» ادعایی است که باید بررسی شود، نه فرض. اگر مانیفست آیکون‌هایش
 * را نداشته باشد یا `start_url` نباشد، مرورگر دکمهٔ نصب را نشان نمی‌دهد
 * و کاربر فکر می‌کند خراب است.
 */

const root = resolve(__dirname, "..");
const pub = (f: string) => resolve(root, "public", f);

describe("PWA installability (D-024)", () => {
  const raw = readFileSync(pub("manifest.webmanifest"), "utf8");
  const manifest = JSON.parse(raw) as Record<string, unknown>;

  it("declares the fields browsers require to offer install", () => {
    expect(manifest.name).toBeTruthy();
    expect(manifest.short_name).toBeTruthy();
    expect(manifest.start_url).toBe("/");
    expect(manifest.display).toBe("standalone");
  });

  it("is a Persian RTL app, not a mislabelled English one", () => {
    expect(manifest.lang).toBe("fa");
    expect(manifest.dir).toBe("rtl");
  });

  it("points at icons that actually exist on disk", () => {
    const icons = manifest.icons as { src: string; sizes: string }[];
    expect(icons.length).toBeGreaterThanOrEqual(2);
    for (const icon of icons) {
      const file = pub(icon.src.replace(/^\//, ""));
      expect(existsSync(file), `missing icon file ${icon.src}`).toBe(true);
      const bytes = readFileSync(file);
      // امضای PNG — فایل خالی یا متنی پذیرفته نمی‌شود
      expect(bytes.subarray(0, 8)).toEqual(
        Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
      );
    }
  });

  it("has a 512x512 maskable icon — Android requires it", () => {
    const icons = manifest.icons as { src: string; sizes: string; purpose?: string }[];
    expect(icons.some((i) => i.sizes === "512x512" && i.purpose === "maskable")).toBe(true);
  });

  it("links the manifest from index.html", () => {
    const html = readFileSync(resolve(root, "index.html"), "utf8");
    expect(html).toContain('rel="manifest"');
    expect(html).toContain("/manifest.webmanifest");
    expect(html).toContain("apple-touch-icon");
  });

  it("service worker never caches API responses", () => {
    const sw = readFileSync(pub("sw.js"), "utf8");
    // دادهٔ API نباید از کش بیاید — وگرنه کاربر دادهٔ کهنه می‌بیند
    expect(sw).toContain('url.pathname.startsWith("/api/")');
    // «return» بدون پاسخ‌دهی یعنی مرورگر درخواست را دست‌نخورده می‌فرستد
    const apiBranch = sw.slice(sw.indexOf('url.pathname.startsWith("/api/")'));
    expect(apiBranch.slice(0, 60)).toMatch(/return\s*;/);
  });

  it("service worker handles HTML offline with a cache fallback", () => {
    const sw = readFileSync(pub("sw.js"), "utf8");
    expect(sw).toContain("caches.match(event.request)");
    expect(sw).toContain("catch(");
  });

  it("registers the service worker outside production too", () => {
    // اگر فقط در PROD ثبت شود، تا لحظهٔ تحویل هرگز آزموده نمی‌شود
    const main = readFileSync(resolve(root, "src/main.tsx"), "utf8");
    const block = main.slice(main.indexOf("serviceWorker"));
    expect(block).toContain('register("/sw.js")');
    expect(block).not.toContain("import.meta.env.PROD");
  });
});
