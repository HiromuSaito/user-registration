import { Link } from "react-router";

export const NotFoundPage = () => {
  return (
    <>
      <h1 className="page-title">ページが見つかりません</h1>
      <div className="card">
        <Link className="button" to="/signup/">
          登録画面へ
        </Link>
      </div>
    </>
  );
};
