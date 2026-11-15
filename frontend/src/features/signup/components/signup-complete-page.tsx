import { Link, Navigate, useLocation } from "react-router";

export const SignupCompletePage = () => {
  const location = useLocation();
  // 印は登録に成功して移ってくるときにだけ渡すので、印がなければ直接開かれた
  if (!location.state?.registered) {
    return <Navigate to="/signup/" replace />;
  }

  return (
    <>
      <h1 className="page-title">登録完了</h1>
      <div className="card complete">
        <p className="complete-title">ユーザー登録が完了しました</p>
        <p className="complete-text">ご登録ありがとうございます。</p>
        <Link className="button" to="/signup/">
          登録画面へ
        </Link>
      </div>
    </>
  );
};
