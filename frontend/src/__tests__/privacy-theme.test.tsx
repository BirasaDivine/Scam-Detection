import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import { RESULT_DISCLAIMER } from "../copy";
import { Root } from "../Root";
import { THEME_KEY } from "../theme";
import { mockBackend } from "../test-utils";

const html = document.documentElement;

function goTo(url: string) {
  window.history.replaceState(null, "", url);
}

beforeEach(() => {
  localStorage.clear();
  html.removeAttribute("data-theme");
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  goTo("/");
});

function footerLink() {
  return within(screen.getByRole("contentinfo")).getByRole("link", { name: "Privacy Policy" });
}

describe("Privacy Policy page", () => {
  it("renders at /privacy with its title, every section heading and the placeholders", () => {
    goTo("/privacy");
    render(<Root />);

    expect(screen.getByRole("heading", { level: 1, name: "Privacy Policy" })).toBeInTheDocument();
    expect(screen.getByText(/^Last updated: \S+/)).not.toHaveTextContent("[");
    const headings = screen.getAllByRole("heading", { level: 2 }).map((h) => h.textContent);
    expect(headings).toEqual([
      "What ScamGuard does.",
      "What we read.",
      "What we never keep.",
      "What stays on your device.",
      "What we count.",
      "Who can see the counts.",
      "Where it runs.",
      "How to use the result.",
      "Who it is for.",
      "Contact.",
    ]);
    const contact = screen.getByRole("heading", { name: "Contact." }).nextElementSibling;
    expect(contact).toHaveTextContent(/^\S+@\S+\.\S+$/);
    expect(screen.getByText(/We do not store or log the text of your messages/)).toBeInTheDocument();
    expect(screen.getByText(/the time, and a random check ID so that an optional scam-source answer/)).toBeInTheDocument();
    expect(screen.getByText(/We do not use these logs or link them to your checks\.$/)).toBeInTheDocument();
    expect(
      screen.getByText("Your light or dark theme choice is saved only in your browser. It is never sent to us."),
    ).toBeInTheDocument();
    expect(footerLink()).toHaveAttribute("href", "/privacy");
    expect(screen.getByRole("link", { name: /back to scamguard/i })).toHaveAttribute("href", "/");
  });

  it("is reached by its path from the main flow and the Insights page", () => {
    mockBackend();
    const { unmount } = render(<Root />);
    expect(footerLink()).toHaveAttribute("href", "/privacy");
    unmount();

    goTo("/#insights");
    render(<Root />);
    expect(screen.getByRole("heading", { name: "Insights" })).toBeInTheDocument();
    expect(footerLink()).toHaveAttribute("href", "/privacy");
  });

  it("is linked from a privacy line under the chat input", async () => {
    mockBackend();
    const user = userEvent.setup();
    render(<App />);
    const line = screen.getByText(/Your messages are checked in memory and never stored\./);
    expect(within(line).getByRole("link", { name: /privacy policy/i })).toHaveAttribute("href", "/privacy");

    await user.click(screen.getByRole("tab", { name: /paste text/i }));
    expect(screen.getByText(/Your messages are checked in memory and never stored\./)).toBeInTheDocument();
  });
});

describe("Theme toggle", () => {
  it("switches the theme, updates its label and remembers the choice", async () => {
    mockBackend();
    const user = userEvent.setup();
    const { unmount } = render(<App />);

    expect(html).toHaveAttribute("data-theme", "light"); // jsdom reports no dark device setting
    await user.click(screen.getByRole("button", { name: "Switch to dark mode" }));
    expect(html).toHaveAttribute("data-theme", "dark");
    expect(localStorage.getItem(THEME_KEY)).toBe("dark");
    const toggle = screen.getByRole("button", { name: "Switch to light mode" });

    // Keyboard: Enter and Space both work on the native button
    toggle.focus();
    await user.keyboard("{Enter}");
    expect(html).toHaveAttribute("data-theme", "light");
    expect(toggle).toHaveAccessibleName("Switch to dark mode");
    await user.keyboard(" ");
    expect(html).toHaveAttribute("data-theme", "dark");
    unmount();

    // A new visit starts from the saved choice
    html.removeAttribute("data-theme");
    render(<App />);
    expect(html).toHaveAttribute("data-theme", "dark");
    expect(screen.getByRole("button", { name: "Switch to light mode" })).toBeInTheDocument();
  });

  it("follows the device setting on a first visit", () => {
    mockBackend();
    vi.stubGlobal(
      "matchMedia",
      vi.fn((query: string) => ({
        matches: query === "(prefers-color-scheme: dark)",
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })),
    );
    render(<App />);
    expect(html).toHaveAttribute("data-theme", "dark");
    expect(screen.getByRole("button", { name: "Switch to light mode" })).toBeInTheDocument();
  });

  it("still works when storage is blocked", async () => {
    mockBackend();
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new DOMException("blocked", "SecurityError");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new DOMException("blocked", "SecurityError");
    });
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("button", { name: "Switch to dark mode" }));
    expect(html).toHaveAttribute("data-theme", "dark");
  });

  it("is in the header of the Privacy and Insights pages", () => {
    goTo("/privacy");
    const { unmount } = render(<Root />);
    expect(screen.getByRole("button", { name: "Switch to dark mode" })).toBeInTheDocument();
    unmount();

    goTo("/#insights");
    render(<Root />);
    expect(screen.getByRole("button", { name: "Switch to dark mode" })).toBeInTheDocument();
  });
});

describe("Result disclaimer", () => {
  it("is shown with the verdict", async () => {
    mockBackend();
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("tab", { name: /paste text/i }));
    await user.type(screen.getByLabelText("Chat text"), "Pay the fee now");
    await user.click(screen.getByRole("button", { name: /next step/i }));
    await user.click(screen.getByRole("button", { name: "Analyse" }));

    expect(await screen.findByRole("heading", { name: "This looks like a scam" })).toBeInTheDocument();
    expect(
      screen.getByText(
        "ScamGuard can make mistakes. Always confirm requests for money, PINs or codes with your bank or provider.",
      ),
    ).toBeInTheDocument();
    expect(RESULT_DISCLAIMER).toMatch(/^ScamGuard can make mistakes\./);
  });
});
