import { Navigate, Route, Routes } from "react-router";
import { NotFoundPage } from "@/components/not-found-page";
import { SignupCompletePage } from "@/features/signup/components/signup-complete-page";
import { SignupPage } from "@/features/signup/components/signup-page";

export const App = () => {
  return (
    <Routes>
      <Route index element={<Navigate to="/signup/" replace />} />
      <Route path="signup" element={<SignupPage />} />
      <Route path="signup/complete" element={<SignupCompletePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
