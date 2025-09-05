// auth.js

const API_BASE = "http://127.0.0.1:8000";

// Save tokens
function saveTokens(access, refresh) {
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);

  document.cookie = `access_token=${access}; path=/`;
  document.cookie = `refresh_token=${refresh}; path=/`;

}

// Get tokens
function getAccessToken() {
  return localStorage.getItem("access_token");
}
function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

// Refresh token
async function refreshToken() {
  const refresh = getRefreshToken();
  if (!refresh) return null;

  const res = await fetch(`${API_BASE}/api/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });

  if (res.ok) {
    const data = await res.json();
    saveTokens(data.access, refresh);
    return data.access;
  } else {
    console.error("Refresh token failed");
    localStorage.clear();
    window.location.href = "/login/";
  }
}

// Generic API fetch with auto-refresh
async function apiFetch(url, options = {}) {
  let access = getAccessToken();
  if (!options.headers) options.headers = {};
  if (access) options.headers["Authorization"] = `Bearer ${access}`;

  let res = await fetch(API_BASE + url, options);

  // If token expired → refresh and retry
  if (res.status === 401 && getRefreshToken()) {
    access = await refreshToken();
    if (access) {
      options.headers["Authorization"] = `Bearer ${access}`;
      res = await fetch(API_BASE + url, options);
    }
  }

  return res;
}
