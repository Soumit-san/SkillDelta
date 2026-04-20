import axios from "axios";

// ── API Base URL ──────────────────────────────────────────────────────────────
// Hardcoded to Hugging Face to override any old Render variables in Vercel!
export const BASE_URL = "https://samd444-skilldelta.hf.space";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 20000,
});

// Attach token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Handle expired tokens globally
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (
      err.response?.status === 401 &&
      !err.config.url.includes("/auth/login")
    ) {
      localStorage.removeItem("token");
      localStorage.removeItem("user_id");
      window.location.href = "/";
    }
    return Promise.reject(err);
  }
);

/**
 * Aggressive multi-ping warm-up.
 * Fires 3 bare fetch() pings — now, 8 s, 16 s — so the HF Space
 * receives multiple hits the moment the app loads.
 * Uses bare fetch so there is zero axios overhead / no CORS preflight.
 */
export const wakeBackend = () => {
  const ping = () => fetch(`${BASE_URL}/health/ping`).catch(() => {});
  ping();                        // immediate
  setTimeout(ping, 8_000);      // 8 s
  setTimeout(ping, 16_000);     // 16 s
};

export default api;
