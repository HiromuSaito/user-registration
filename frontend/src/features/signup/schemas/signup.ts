import { z } from "zod";

const requiredMessage = (name: string) => `${name}は必須です。`;

const USERNAME_MIN_LENGTH = 3;
const PASSWORD_MIN_LENGTH = 8;
export const USERNAME_MAX_LENGTH = 150;
export const EMAIL_MAX_LENGTH = 254;
export const TEL_MAX_LENGTH = 20;

export const signupSchema = z.object({
  username: z
    .string()
    .min(1, requiredMessage("ユーザー名"))
    // サーバーは日本語などの文字も通すので、英数字ではなく Unicode の文字と数字で表す
    .regex(
      /^[\p{L}\p{N}_.@+-]+$/u,
      "ユーザー名には、文字、数字、@/./+/-/_ だけを使えます。",
    )
    .min(
      USERNAME_MIN_LENGTH,
      `ユーザー名は${USERNAME_MIN_LENGTH}文字以上で入力してください。`,
    ),
  email: z
    .string()
    .min(1, requiredMessage("メールアドレス"))
    // サーバーの email-validator と同じ判定はできないので、基本の形式だけを検証し、細かい違反はサーバーに任せる
    .regex(
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      "メールアドレスの形式が正しくありません。",
    ),
  password: z
    .string()
    .min(1, requiredMessage("パスワード"))
    .min(
      PASSWORD_MIN_LENGTH,
      `このパスワードは短すぎます。最低 ${PASSWORD_MIN_LENGTH} 文字以上必要です。`,
    )
    .regex(/[A-Z]/, "パスワードには大文字を1文字以上含めてください。")
    .regex(/[a-z]/, "パスワードには小文字を1文字以上含めてください。")
    .regex(/[0-9]/, "パスワードには数字を1文字以上含めてください。"),
  tel: z
    .string()
    // サーバーは全角の数字を半角に直して受け付けるので、ここでも半角に変換してから検証する
    .transform((value) => value.normalize("NFKC"))
    .refine(
      (value) => value === "" || /^[0-9]+$/.test(value),
      "電話番号は数字のみで入力してください。",
    )
    .transform((value) => (value === "" ? null : value)),
  pref: z.string().min(1, requiredMessage("都道府県")).transform(Number),
});

export type SignupFormValues = z.input<typeof signupSchema>;
export type SignupInput = z.output<typeof signupSchema>;
