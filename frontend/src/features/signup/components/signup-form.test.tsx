import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { describe, expect, onTestFinished, test, vi } from "vitest";
import { server } from "@/test/server";
import { SignupForm } from "@/features/signup/components/signup-form";

const renderForm = async () => {
  const onSuccess = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSuccess={onSuccess} />);
  await screen.findByRole("option", { name: "東京都" });
  return { onSuccess, user };
};

const fillValid = async (user: ReturnType<typeof userEvent.setup>) => {
  await user.type(screen.getByLabelText("ユーザー名"), "taro");
  await user.type(screen.getByLabelText("メールアドレス"), "taro@example.com");
  await user.type(screen.getByLabelText("パスワード"), "Abcdefg1");
  await user.selectOptions(screen.getByLabelText("都道府県"), "東京都");
};

describe("SignupForm", () => {
  test("都道府県の一覧を API から読み込む", async () => {
    await renderForm();

    expect(screen.getByRole("option", { name: "北海道" })).toBeInTheDocument();
    expect(screen.getByLabelText("都道府県")).toBeEnabled();
  });

  test("都道府県を読み込めなかったら案内を出す", async () => {
    server.use(http.get("/api/prefs/", () => HttpResponse.error()));
    render(<SignupForm onSuccess={vi.fn()} />);

    expect(
      await screen.findByText(
        "都道府県を読み込めませんでした。ページを再読み込みしてください。",
      ),
    ).toBeInTheDocument();
  });

  test("入力の途中ではエラーを出さず、欄を離れたら出す", async () => {
    const { user } = await renderForm();
    const username = screen.getByLabelText("ユーザー名");

    await user.type(username, "ab");
    expect(
      screen.queryByText("ユーザー名は3文字以上で入力してください。"),
    ).not.toBeInTheDocument();

    await user.tab();
    expect(
      screen.getByText("ユーザー名は3文字以上で入力してください。"),
    ).toBeInTheDocument();
    expect(username).toHaveAttribute("aria-invalid", "true");
    expect(username).toHaveAttribute("aria-describedby", "id_username_error");
  });

  test("一度離れた欄は、直したその場でエラーを消す", async () => {
    const { user } = await renderForm();
    const username = screen.getByLabelText("ユーザー名");
    await user.type(username, "ab");
    await user.tab();

    await user.type(username, "c");

    expect(
      screen.queryByText("ユーザー名は3文字以上で入力してください。"),
    ).not.toBeInTheDocument();
    expect(username).not.toHaveAttribute("aria-invalid");
  });

  test("何も入れずに送信すると、必須の欄のエラーとまとめを出す", async () => {
    const { user, onSuccess } = await renderForm();

    await user.click(screen.getByRole("button", { name: "登録する" }));

    for (const name of [
      "ユーザー名",
      "メールアドレス",
      "パスワード",
      "都道府県",
    ]) {
      expect(screen.getByText(`${name}は必須です。`)).toBeInTheDocument();
    }
    expect(
      screen.getByText(
        "入力内容に誤りがあります。各項目のメッセージをご確認ください。",
      ),
    ).toBeInTheDocument();
    expect(onSuccess).not.toHaveBeenCalled();
  });

  test("送信すると API の形に変えた値と CSRF のトークンを送り、成功を知らせる", async () => {
    document.cookie = "csrftoken=test-token";
    onTestFinished(() => {
      document.cookie = "csrftoken=; max-age=0";
    });
    let received: { body: unknown; token: string | null } | undefined;
    server.use(
      http.post("/api/users/", async ({ request }) => {
        received = {
          body: await request.json(),
          token: request.headers.get("X-CSRFToken"),
        };
        return HttpResponse.json({}, { status: 201 });
      }),
    );
    const { user, onSuccess } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(received).toEqual({
      body: {
        username: "taro",
        email: "taro@example.com",
        password: "Abcdefg1",
        tel: null,
        pref: 13,
      },
      token: "test-token",
    });
    expect(onSuccess).toHaveBeenCalledOnce();
  });

  test("サーバーが返した欄のエラーを、その欄に出す", async () => {
    server.use(
      http.post("/api/users/", () =>
        HttpResponse.json(
          { email: ["このメールアドレスは既に登録されています。"] },
          { status: 400 },
        ),
      ),
    );
    const { user, onSuccess } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(
      await screen.findByText("このメールアドレスは既に登録されています。"),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("メールアドレス")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(onSuccess).not.toHaveBeenCalled();
  });

  test("サーバーが返した欄に属さないエラーを、まとめに出す", async () => {
    server.use(
      http.post("/api/users/", () =>
        HttpResponse.json(
          { non_field_errors: ["サーバーで登録を受け付けられませんでした。"] },
          { status: 400 },
        ),
      ),
    );
    const { user, onSuccess } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(
      await screen.findByText("サーバーで登録を受け付けられませんでした。"),
    ).toBeInTheDocument();
    expect(onSuccess).not.toHaveBeenCalled();
  });

  test("送信している間は、ボタンを押せなくする", async () => {
    let respond = () => {};
    const responded = new Promise<void>((resolve) => {
      respond = resolve;
    });
    server.use(
      http.post("/api/users/", async () => {
        await responded;
        return HttpResponse.json({}, { status: 201 });
      }),
    );
    const { user, onSuccess } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(
      await screen.findByRole("button", { name: "送信中…" }),
    ).toBeDisabled();
    respond();
    await waitFor(() => expect(onSuccess).toHaveBeenCalledOnce());
  });

  test("400 の中身が欄ごとのエラーの形でなければ、まとめにやり直しを促す文を出す", async () => {
    server.use(
      http.post("/api/users/", () =>
        HttpResponse.json({ detail: "JSON parse error" }, { status: 400 }),
      ),
    );
    const { user } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(
      await screen.findByText(
        "登録できませんでした。入力内容を確かめて、もう一度お試しください。",
      ),
    ).toBeInTheDocument();
  });

  test("登録できなかったら、まとめにやり直しを促す文を出す", async () => {
    server.use(
      http.post("/api/users/", () => new HttpResponse(null, { status: 403 })),
    );
    const { user, onSuccess } = await renderForm();
    await fillValid(user);

    await user.click(screen.getByRole("button", { name: "登録する" }));

    expect(
      await screen.findByText(
        "登録できませんでした。入力内容を確かめて、もう一度お試しください。",
      ),
    ).toBeInTheDocument();
    expect(onSuccess).not.toHaveBeenCalled();
  });
});
