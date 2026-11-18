import { Moon, Sun } from "@phosphor-icons/react";
import { useTheme } from "../theme";
import styles from "./Layout.module.css";

/** A native button, so Enter, Space and the focus outline work without extra code. */
export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const dark = theme === "dark";
  return (
    <button
      type="button"
      className={styles.menuButton}
      aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
      title={dark ? "Switch to light mode" : "Switch to dark mode"}
      onClick={toggle}
    >
      {dark ? <Sun size={22} aria-hidden="true" /> : <Moon size={22} aria-hidden="true" />}
    </button>
  );
}
