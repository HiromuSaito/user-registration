import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

import { App } from "@/app/app";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    {/* サーバーが /app/ の配下を SPA に回しているので、ルートはその下からの道筋で書く */}
    <BrowserRouter basename="/app">
      <App />
    </BrowserRouter>
  </StrictMode>,
);
