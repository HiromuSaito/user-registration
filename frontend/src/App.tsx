import { Link, Navigate, Route, Routes, useLocation } from "react-router";

// TODO: 登録フォームを作るときに、画面ごとのファイルに分けて中身を作る
function SignupPage() {
  return <h1>ユーザー登録</h1>;
}

function SignupCompletePage() {
  const location = useLocation();
  // 登録に成功したときだけ、画面を移るときに印を渡す。直接開かれたら印がないので、フォームへ戻す
  if (!location.state?.registered) {
    return <Navigate to="/signup/" replace />;
  }
  return <h1>登録完了</h1>;
}

function NotFoundPage() {
  return (
    <>
      <h1>ページが見つかりません</h1>
      <Link to="/signup/">登録画面へ</Link>
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route index element={<Navigate to="/signup/" replace />} />
      <Route path="signup" element={<SignupPage />} />
      <Route path="signup/complete" element={<SignupCompletePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
