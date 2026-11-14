import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "./server.ts";

// 偽物を用意し忘れたリクエストが本物のネットワークに出ないよう、失敗させる
beforeAll(() => server.listen({ onUnhandledFrame: "error" }));
afterEach(() => {
  server.resetHandlers();
  // Vitest の globals を有効にしていないため、Testing Library の自動の後片付けが動かない
  cleanup();
});
afterAll(() => server.close());
