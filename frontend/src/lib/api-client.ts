export class ApiError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(status: number, body: unknown) {
    super(`API のリクエストが ${status} で失敗しました`);
    this.status = status;
    this.body = body;
  }
}

const CSRF_COOKIE_NAME = "csrftoken";

const getCookie = (name: string): string | undefined => {
  return document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith(`${name}=`))
    ?.slice(name.length + 1);
};

const readJsonOrNull = async (response: Response): Promise<unknown> => {
  try {
    return await response.json();
  } catch {
    return null;
  }
};

const request = async <T>(path: string, init: RequestInit): Promise<T> => {
  // テストの jsdom では fetch が相対 URL を解決しないため、今のページの origin から絶対 URL を作る
  const response = await fetch(new URL(path, window.location.origin), init);
  const body = await readJsonOrNull(response);
  if (!response.ok) {
    throw new ApiError(response.status, body);
  }
  return body as T;
};

export const api = {
  get: <TResponse = never>(path: string): Promise<TResponse> => {
    return request<TResponse>(path, { method: "GET" });
  },
  post: <TBody = never, TResponse = never>(
    path: string,
    data: NoInfer<TBody>,
  ): Promise<TResponse> => {
    return request<TResponse>(path, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie(CSRF_COOKIE_NAME) ?? "",
      },
      body: JSON.stringify(data),
    });
  },
};
