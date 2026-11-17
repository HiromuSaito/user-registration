import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router";
import { expect, test } from "vitest";

import { SignupCompletePage } from "@/features/signup/components/signup-complete-page";
import { SignupPage } from "@/features/signup/components/signup-page";
import { server } from "@/test/server";

test("登録に成功したら完了画面に移る", async () => {
  server.use(
    http.post("/api/users/", () => HttpResponse.json({}, { status: 201 })),
  );
  const user = userEvent.setup();
  render(
    <MemoryRouter initialEntries={["/signup/"]}>
      <Routes>
        <Route path="/signup/" element={<SignupPage />} />
        <Route path="/signup/complete/" element={<SignupCompletePage />} />
      </Routes>
    </MemoryRouter>,
  );
  await screen.findByRole("option", { name: "東京都" });

  await user.type(screen.getByLabelText("ユーザー名"), "taro");
  await user.type(screen.getByLabelText("メールアドレス"), "taro@example.com");
  await user.type(screen.getByLabelText("パスワード"), "Abcdefg1");
  await user.selectOptions(screen.getByLabelText("都道府県"), "東京都");
  await user.click(screen.getByRole("button", { name: "登録する" }));

  expect(
    await screen.findByRole("heading", { name: "登録完了" }),
  ).toBeInTheDocument();
});
