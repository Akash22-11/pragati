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
  } else {
    alert("Invalid credentials. Please try again.");
  }
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
