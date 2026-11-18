import { useEffect, useState } from "react";

// The inline script in index.html applies the theme before React renders, so there is no flash.
// It uses the same key and rules as this file: keep the two in step.

export type Theme = "light" | "dark";

export const THEME_KEY = "scamguard-theme";
const DARK_QUERY = "(prefers-color-scheme: dark)";

const isTheme = (value: unknown): value is Theme => value === "light" || value === "dark";

/** The user's saved choice, or null if they never chose or storage is blocked. */
export function storedTheme(): Theme | null {
  try {
    const value = localStorage.getItem(THEME_KEY);
    return isTheme(value) ? value : null;
  } catch {
    return null;
  }
}

function saveTheme(theme: Theme) {
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    // storage blocked: the choice lasts until the page is closed
  }
}

function darkQuery(): MediaQueryList | null {
  try {
    return typeof window.matchMedia === "function" ? window.matchMedia(DARK_QUERY) : null;
  } catch {
    return null;
  }
}

export function systemTheme(): Theme {
  return darkQuery()?.matches ? "dark" : "light";
}

export function applyTheme(theme: Theme) {
  document.documentElement.dataset.theme = theme;
}

/** The theme on the page now. Falls back to the stored choice, then the device setting. */
export function currentTheme(): Theme {
  const applied = document.documentElement.dataset.theme;
  return isTheme(applied) ? applied : (storedTheme() ?? systemTheme());
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(currentTheme);

  // Covers the case where the inline script did not run.
  useEffect(() => applyTheme(theme), [theme]);

  // Until the user picks a theme, follow changes to the device setting.
  useEffect(() => {
    const query = darkQuery();
    if (!query?.addEventListener) return;
    const onChange = (e: MediaQueryListEvent) => {
      if (!storedTheme()) setTheme(e.matches ? "dark" : "light");
    };
    query.addEventListener("change", onChange);
    return () => query.removeEventListener("change", onChange);
  }, []);

  function toggle() {
    const next: Theme = theme === "dark" ? "light" : "dark";
    saveTheme(next);
    setTheme(next);
  }

  return { theme, toggle };
}
