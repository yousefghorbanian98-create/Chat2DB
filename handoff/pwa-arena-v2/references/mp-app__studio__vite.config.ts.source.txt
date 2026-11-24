import { createRequire } from "node:module";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// خواندن نسخه با require — import JSON در بعضی محیط‌های CI با
// resolveJsonModule کار نمی‌کند و build/test را می‌شکند.
const pkg = createRequire(import.meta.url)("./package.json") as { version: string };

export default defineConfig({
  plugins: [react()],
  // نسخهٔ اپ در باندل — بنر به‌روزرسانی PWA (M20) بدون آن نمی‌توانست
  // نسخهٔ نصب‌شده را با manifest سرور مقایسه کند.
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: false,
    allowedHosts: true,
    // M46-c5 — در dev هیچ پراکسی‌ای نبود، پس کلاینت به `/api/v1/...` می‌زد و
    // Vite همان مسیر را به index.html برمی‌گرداند؛ یعنی استودیو در dev هرگز
    // به بک‌اند نمی‌رسید. در production همین کار را nginx.conf می‌کند.
    proxy: {
      "/api": {
        target: process.env.MP_API_TARGET ?? "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/health": {
        target: process.env.MP_API_TARGET ?? "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: true,
  },
  build: {
    outDir: "dist",
    chunkSizeWarningLimit: 1200,
    // Q11 — بعد از افزودن antd باندل تک‌تکه به ~1.26MB رسید و هشدار Vite
    // رد شد. جدا کردن vendorها دو فایده دارد: مرورگر/PWA فقط چیزی را
    // دوباره می‌گیرد که تغییر کرده، و باندل کتابخانهٔ UI از کد صفحه‌ها
    // جدا می‌شود تا اندازه‌اش قابل سنجش بماند.
    rollupOptions: {
      output: {
        manualChunks: {
          "vendor-antd": ["antd", "@ant-design/icons", "@ant-design/cssinjs"],
          "vendor-dates": ["react-multi-date-picker", "react-date-object"],
          "vendor-charts": ["recharts"],
          "vendor-motion": ["framer-motion"],
        },
      },
    },
  },
});
