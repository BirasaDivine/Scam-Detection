import { useEffect, useState } from "react";
import App from "./App";
import { InsightsPage } from "./pages/InsightsPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { pageFor } from "./routes";

/** Picks the page from the address. The main flow stays at "/"; Insights is at #insights. */
export function Root() {
  const [page, setPage] = useState(() => pageFor(window.location.pathname, window.location.hash));
  useEffect(() => {
    const onChange = () => setPage(pageFor(window.location.pathname, window.location.hash));
    window.addEventListener("hashchange", onChange);
    window.addEventListener("popstate", onChange);
    return () => {
      window.removeEventListener("hashchange", onChange);
      window.removeEventListener("popstate", onChange);
    };
  }, []);
  if (page === "insights") return <InsightsPage />;
  if (page === "privacy") return <PrivacyPage />;
  return <App />;
}
