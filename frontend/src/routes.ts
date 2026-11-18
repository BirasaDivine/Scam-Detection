/** Real path, so the link can be shared. Netlify serves index.html for it (see netlify.toml). */
export const PRIVACY_PATH = "/privacy";

export type Page = "app" | "insights" | "privacy";

export function pageFor(pathname: string, hash: string): Page {
  if (hash === "#insights") return "insights";
  if (pathname.replace(/\/+$/, "") === PRIVACY_PATH || hash === "#privacy") return "privacy";
  return "app";
}
