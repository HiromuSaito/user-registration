import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

const PREFS = [
  { code: 1, name: "北海道" },
  { code: 13, name: "東京都" },
];

// 登録画面は開くたびに都道府県の一覧を読むので、どのテストでも返す
export const server = setupServer(
  http.get("/api/prefs/", () => HttpResponse.json(PREFS)),
);
