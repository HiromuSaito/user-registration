import type { components } from "@/api/schema";
import { api } from "@/lib/api-client";
import type { SignupInput } from "@/features/signup/schemas/signup";

type UserCreateRequest = components["schemas"]["UserCreateRequest"];
type UserCreate = components["schemas"]["UserCreate"];

export const createUser = (input: SignupInput): Promise<UserCreate> => {
  return api.post<UserCreateRequest, UserCreate>("/api/users/", input);
};
