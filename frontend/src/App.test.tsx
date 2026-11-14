import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "./App.tsx";

// TODO: 画面のテストができたら消す。今はテストの道具（jsdom・jest-dom・準備のファイル）が
// つながって動くことを確かめるためと、テストが 1 つもないと vitest run が失敗するために置いている
test("見出しを表示する", () => {
  render(<App />);
  expect(
    screen.getByRole("heading", { name: "ユーザー登録" }),
  ).toBeInTheDocument();
});
