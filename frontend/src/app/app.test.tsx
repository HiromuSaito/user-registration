import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { describe, expect, test } from "vitest";

import { App } from "@/app/app";

const renderAt = (entry: string | { pathname: string; state: unknown }) => {
  render(
    <MemoryRouter initialEntries={[entry]}>
      <App />
    </MemoryRouter>,
  );
};

// 登録画面は都道府県の一覧を読み込むので、読み込みが終わってからテストを終える
const waitForPrefs = async () => {
  await screen.findByRole("option", { name: "東京都" });
};

const heading = () => {
  return screen.getByRole("heading", { level: 1 });
};

describe("画面の切り替え", () => {
  test("トップは登録画面に移る", async () => {
    renderAt("/");
    expect(heading()).toHaveTextContent("ユーザー登録");
    await waitForPrefs();
  });

  test("登録画面を表示する", async () => {
    renderAt("/signup/");
    expect(heading()).toHaveTextContent("ユーザー登録");
    await waitForPrefs();
  });

  test("登録に成功して移ってきたときは完了画面を表示する", () => {
    renderAt({ pathname: "/signup/complete/", state: { registered: true } });
    expect(heading()).toHaveTextContent("登録完了");
  });

  test("完了画面を直接開いたら登録画面に戻す", async () => {
    renderAt("/signup/complete/");
    expect(heading()).toHaveTextContent("ユーザー登録");
    await waitForPrefs();
  });

  test("知らない URL ではページがないと表示する", () => {
    renderAt("/unknown/");
    expect(heading()).toHaveTextContent("ページが見つかりません");
  });
});
