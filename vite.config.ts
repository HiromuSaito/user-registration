import { resolve } from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  root: "frontend",
  // Django の STATIC_URL と合わせる。ビルドしたファイルは Django の静的ファイルとして配信される
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: "dist",
    emptyOutDir: true,
    rolldownOptions: {
      // HTML は Django のテンプレートが返すので、index.html ではなく JS を入口にする。
      // 相対パスはビルドでは作業ディレクトリ、開発サーバーでは root から探されて食い違うため、絶対パスにする
      input: resolve(import.meta.dirname, "frontend/src/main.tsx"),
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["src/test/setup.ts"],
  },
});
