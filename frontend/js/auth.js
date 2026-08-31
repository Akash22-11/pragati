import { apiFetch } from "./api.js";

export async function login(email, password) {
  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  if (res && res.ok) {
    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    window.location.href = "/pages/dashboard.html";
    return;
  }

  // Throw instead of alert() so calling pages can show their own inline error.
  let message = "Invalid email or password. Please try again.";
  try {
    const errBody = await res.json();
    if (errBody && errBody.detail) message = errBody.detail;
  } catch (_) {
    // response wasn't JSON — keep default message
  }
  throw new Error(message);
}

export function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "/pages/login.html";
}

export function getToken() {
  return localStorage.getItem("access_token");
}

export function isLoggedIn() {
  return !!getToken();
}
