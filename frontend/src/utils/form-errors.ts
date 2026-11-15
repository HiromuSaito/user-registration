import type { FieldValues, Path, UseFormSetError } from "react-hook-form";
import { ApiError } from "@/lib/api-client";

const isFieldErrors = (body: unknown): body is Record<string, string[]> => {
  return (
    typeof body === "object" &&
    body !== null &&
    Object.values(body).every(
      (messages) =>
        Array.isArray(messages) &&
        messages.length > 0 &&
        messages.every((message) => typeof message === "string"),
    )
  );
};

export const setServerErrors = <T extends FieldValues>(
  error: unknown,
  setError: UseFormSetError<T>,
  fieldNames: readonly Path<T>[],
  fallbackMessage: string,
): void => {
  if (!(
    error instanceof ApiError &&
    error.status === 400 &&
    isFieldErrors(error.body)
  )) {
    setError("root.server", { message: fallbackMessage });
    return;
  }
  for (const [key, messages] of Object.entries(error.body)) {
    const fieldName = fieldNames.find((name) => name === key);
    if (fieldName) {
      setError(fieldName, { message: messages[0] });
    } else {
      setError("root.server", { message: messages[0] });
    }
  }
};
