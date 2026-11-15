import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { Field } from "@/components/ui/field";
import { createUser } from "@/features/signup/api/create-user";
import { getPrefs, type Pref } from "@/features/signup/api/get-prefs";
import {
  EMAIL_MAX_LENGTH,
  signupSchema,
  TEL_MAX_LENGTH,
  USERNAME_MAX_LENGTH,
  type SignupFormValues,
  type SignupInput,
} from "@/features/signup/schemas/signup";
import { setServerErrors } from "@/utils/form-errors";

const SIGNUP_FAILED =
  "登録できませんでした。入力内容を確かめて、もう一度お試しください。";
const PREFS_LOAD_FAILED =
  "都道府県を読み込めませんでした。ページを再読み込みしてください。";

type SignupFormProps = {
  onSuccess: () => void;
};

export const SignupForm = ({ onSuccess }: SignupFormProps) => {
  const [prefs, setPrefs] = useState<Pref[] | null>(null);
  const [prefsFailed, setPrefsFailed] = useState(false);

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitted, isSubmitting },
  } = useForm<SignupFormValues, unknown, SignupInput>({
    resolver: zodResolver(signupSchema),
    mode: "onTouched",
    defaultValues: { username: "", email: "", password: "", tel: "", pref: "" },
  });

  useEffect(() => {
    // 画面を離れたあとに届いた結果で state を変えない
    let ignore = false;
    const loadPrefs = async () => {
      try {
        const result = await getPrefs();
        if (!ignore) setPrefs(result);
      } catch {
        if (!ignore) setPrefsFailed(true);
      }
    };
    loadPrefs();
    return () => {
      ignore = true;
    };
  }, []);

  const onSubmit = async (input: SignupInput) => {
    try {
      await createUser(input);
    } catch (error) {
      setServerErrors(
        error,
        setError,
        signupSchema.keyof().options,
        SIGNUP_FAILED,
      );
      return;
    }
    onSuccess();
  };

  const hasErrors = Object.keys(errors).length > 0;

  return (
    <form className="card form" noValidate onSubmit={handleSubmit(onSubmit)}>
      {isSubmitted && hasErrors && (
        <div className="form-summary">
          <p>
            {errors.root?.server?.message ??
              "入力内容に誤りがあります。各項目のメッセージをご確認ください。"}
          </p>
        </div>
      )}

      <Field
        id="id_username"
        label="ユーザー名"
        error={errors.username?.message}
      >
        {(control) => (
          <input
            {...control}
            {...register("username")}
            type="text"
            autoComplete="username"
            maxLength={USERNAME_MAX_LENGTH}
            required
          />
        )}
      </Field>

      <Field id="id_email" label="メールアドレス" error={errors.email?.message}>
        {(control) => (
          <input
            {...control}
            {...register("email")}
            type="email"
            autoComplete="email"
            maxLength={EMAIL_MAX_LENGTH}
            required
          />
        )}
      </Field>

      <Field
        id="id_password"
        label="パスワード"
        error={errors.password?.message}
      >
        {(control) => (
          <input
            {...control}
            {...register("password")}
            type="password"
            autoComplete="new-password"
            required
          />
        )}
      </Field>

      <Field id="id_tel" label="電話番号" optional error={errors.tel?.message}>
        {(control) => (
          <input
            {...control}
            {...register("tel")}
            type="tel"
            inputMode="numeric"
            autoComplete="tel"
            maxLength={TEL_MAX_LENGTH}
          />
        )}
      </Field>

      <Field
        id="id_pref"
        label="都道府県"
        error={errors.pref?.message}
        hint={prefsFailed ? PREFS_LOAD_FAILED : undefined}
      >
        {(control) => (
          <select
            {...control}
            {...register("pref")}
            disabled={prefs === null}
            required
          >
            <option value="">---------</option>
            {prefs?.map((pref) => (
              <option key={pref.code} value={pref.code}>
                {pref.name}
              </option>
            ))}
          </select>
        )}
      </Field>

      <button type="submit" className="button" disabled={isSubmitting}>
        {isSubmitting ? "送信中…" : "登録する"}
      </button>
    </form>
  );
};
