import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { describe, expect, test } from "vitest";
import App from "./App.tsx";

function renderAt(entry: string | { pathname: string; state: unknown }) {
  render(
    <MemoryRouter initialEntries={[entry]}>
      <App />
    </MemoryRouter>,
  );
}

function heading() {
  return screen.getByRole("heading", { level: 1 });
}

describe("画面の切り替え", () => {
  test("トップは登録画面に移る", () => {
    renderAt("/");
    expect(heading()).toHaveTextContent("ユーザー登録");
  });

  test("登録画面を表示する", () => {
    renderAt("/signup/");
    expect(heading()).toHaveTextContent("ユーザー登録");
  });

  test("登録に成功して移ってきたときは完了画面を表示する", () => {
    renderAt({ pathname: "/signup/complete/", state: { registered: true } });
    expect(heading()).toHaveTextContent("登録完了");
  });

  test("完了画面を直接開いたら登録画面に戻す", () => {
    renderAt("/signup/complete/");
    expect(heading()).toHaveTextContent("ユーザー登録");
  });

  test("知らない URL ではページがないと表示する", () => {
    renderAt("/unknown/");
    expect(heading()).toHaveTextContent("ページが見つかりません");
  });
});
