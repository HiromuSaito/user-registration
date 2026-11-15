import { describe, expect, test } from "vitest";

import {
  signupSchema,
  type SignupFormValues,
} from "@/features/signup/schemas/signup";

const VALID: SignupFormValues = {
  username: "taro",
  email: "taro@example.com",
  password: "Abcdefg1",
  tel: "",
  pref: "13",
};

const firstError = (field: keyof SignupFormValues, value: string) => {
  const result = signupSchema.safeParse({ ...VALID, [field]: value });
  return result.success
    ? undefined
    : result.error.issues.find((issue) => issue.path[0] === field)?.message;
};

describe("signupSchema", () => {
  test("正しい値は API に送る形に変える", () => {
    expect(signupSchema.parse(VALID)).toEqual({
      username: "taro",
      email: "taro@example.com",
      password: "Abcdefg1",
      tel: null,
      pref: 13,
    });
  });

  test.each([
    ["username", "", "ユーザー名は必須です。"],
    ["username", "ab", "ユーザー名は3文字以上で入力してください。"],
    [
      "username",
      "ta ro",
      "ユーザー名には、文字、数字、@/./+/-/_ だけを使えます。",
    ],
    ["email", "", "メールアドレスは必須です。"],
    ["email", "taro@example", "メールアドレスの形式が正しくありません。"],
    ["password", "", "パスワードは必須です。"],
    [
      "password",
      "Abcdef1",
      "このパスワードは短すぎます。最低 8 文字以上必要です。",
    ],
    ["password", "abcdefg1", "パスワードには大文字を1文字以上含めてください。"],
    ["password", "ABCDEFG1", "パスワードには小文字を1文字以上含めてください。"],
    ["password", "Abcdefgh", "パスワードには数字を1文字以上含めてください。"],
    ["tel", "090-1234", "電話番号は数字のみで入力してください。"],
    ["pref", "", "都道府県は必須です。"],
  ] as const)("%s が %j ならエラー", (field, value, message) => {
    expect(firstError(field, value)).toBe(message);
  });

  test("ユーザー名には日本語の文字も使える", () => {
    expect(firstError("username", "山田太郎")).toBeUndefined();
  });

  test("電話番号の全角の数字は半角に直す", () => {
    expect(signupSchema.parse({ ...VALID, tel: "０９０１２３４" }).tel).toBe(
      "0901234",
    );
  });
});
