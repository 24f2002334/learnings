const API_BASE = "/api";

async function apiRequest(path, { method = "GET", body, isForm = false } = {}) {
  const token = localStorage.getItem("ppa_token");
  const headers = {};
  if (!isForm) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    data = null;
  }

  if (!res.ok) {
    const message = (data && (data.error || data.detail)) || `Request failed (${res.status})`;
    const err = new Error(message);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}

const api = {
  get: (path) => apiRequest(path, { method: "GET" }),
  post: (path, body, opts = {}) => apiRequest(path, { method: "POST", body, ...opts }),
  put: (path, body) => apiRequest(path, { method: "PUT", body }),
};
