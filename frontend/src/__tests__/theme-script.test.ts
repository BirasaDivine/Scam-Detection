// @vitest-environment node
import { describe, expect, it } from "vitest";
import indexHtml from "../../index.html?raw";
import netlifyToml from "../../../netlify.toml?raw";
import { THEME_KEY } from "../theme";

const script = /<script>([\s\S]*?)<\/script>/.exec(indexHtml)?.[1] ?? "";

/** Runs the inline script against fake browser objects and returns the theme it set. */
function run(stored: string | null | "throws", deviceDark: boolean) {
  const attrs: Record<string, string> = {};
  const localStorage = {
    getItem: (key: string) => {
      if (stored === "throws") throw new Error("blocked");
      return key === THEME_KEY ? stored : null;
    },
  };
  const matchMedia = (q: string) => ({ matches: deviceDark && q === "(prefers-color-scheme: dark)" });
  const document = { documentElement: { setAttribute: (k: string, v: string) => (attrs[k] = v) } };
  new Function("localStorage", "matchMedia", "document", script)(localStorage, matchMedia, document);
  return attrs["data-theme"];
}

describe("theme script in index.html", () => {
  it("uses the saved choice, else the device setting", () => {
    expect(run("dark", false)).toBe("dark");
    expect(run("light", true)).toBe("light");
    expect(run(null, true)).toBe("dark");
    expect(run(null, false)).toBe("light");
    expect(run("purple", true)).toBe("dark");
    expect(run("throws", true)).toBe("dark");
  });

  it("is allowed by the Content-Security-Policy in netlify.toml", async () => {
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(script));
    const hash = btoa(String.fromCharCode(...new Uint8Array(digest)));
    expect(netlifyToml).toContain(`'sha256-${hash}'`);
  });
});
