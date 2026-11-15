import { useNavigate } from "react-router";
import { SignupForm } from "@/features/signup/components/signup-form";

export const SignupPage = () => {
  const navigate = useNavigate();

  return (
    <>
      <h1 className="page-title">ユーザー登録</h1>
      <SignupForm
        onSuccess={() =>
          navigate("/signup/complete/", { state: { registered: true } })
        }
      />
    </>
  );
};
