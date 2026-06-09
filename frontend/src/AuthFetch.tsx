type AuthFetchOptions = RequestInit;

export async function authFetch(
  url: string,
  options: AuthFetchOptions = {}
) {
  const token = localStorage.getItem("token");

  return fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
}