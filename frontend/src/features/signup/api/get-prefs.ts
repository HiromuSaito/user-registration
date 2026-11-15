import type { components } from "@/api/schema";
import { api } from "@/lib/api-client";

export type Pref = components["schemas"]["Pref"];

export const getPrefs = (): Promise<Pref[]> => {
  return api.get<Pref[]>("/api/prefs/");
};
