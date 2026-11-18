import { ArrowLeft } from "@phosphor-icons/react";
import { useEffect } from "react";
import { PageHeader, SiteFooter } from "../components/Layout";
import app from "../App.module.css";
import styles from "./PrivacyPage.module.css";

const LAST_UPDATED = "2026";
const CONTACT_EMAIL = "b.divine@alustudent.com";

const SECTIONS: { heading: string; body: string }[] = [
  {
    heading: "What ScamGuard does.",
    body:
      "ScamGuard checks a message or chat you choose to give it and tells you whether it looks like a scam. " +
      "It is a student capstone project at African Leadership University, not a bank or police service.",
  },
  {
    heading: "What we read.",
    body:
      "The text you paste or the WhatsApp .txt file you upload. We read it in memory only to give you a verdict.",
  },
  {
    heading: "What we never keep.",
    body:
      "We do not store or log the text of your messages, the names in them, or the file you upload. " +
      "We do not ask you to create an account.",
  },
  {
    heading: "What stays on your device.",
    body: "Your light or dark theme choice is saved only in your browser. It is never sent to us.",
  },
  {
    heading: "What we count.",
    body:
      "For each check we save the verdict, the format (single SMS, plain text or WhatsApp export), the time, " +
      "and a random check ID so that an optional scam-source answer can be attached to it. " +
      "If you choose to tell us where a scam came from (for example SMS or WhatsApp), we save that answer too. " +
      "None of this identifies you.",
  },
  {
    heading: "Who can see the counts.",
    body: "Only the project administrator, using a secret token, can see the totals on the Insights page.",
  },
  {
    heading: "Where it runs.",
    body:
      "The website is hosted on Netlify, the checking service on Render, and the counts database on Neon. " +
      "Your text passes through Render's servers for a moment while it is checked. " +
      "Like most websites, our hosting providers keep standard server logs, such as IP address and time, " +
      "for security and reliability. We do not use these logs or link them to your checks.",
  },
  {
    heading: "How to use the result.",
    body:
      "A verdict is a guide, not a guarantee. Before you send money or share a PIN or code, confirm the request " +
      "through an official channel, such as calling your bank or mobile money provider on its published number.",
  },
  {
    heading: "Who it is for.",
    body: "ScamGuard is intended for adults aged 18 and over.",
  },
];

export function PrivacyPage() {
  useEffect(() => {
    const previous = document.title;
    document.title = "Privacy Policy · ScamGuard";
    return () => {
      document.title = previous;
    };
  }, []);

  return (
    <div className={app.page}>
      <main className={`${app.main} ${styles.main}`}>
        <PageHeader />
        <article className={styles.policy} aria-labelledby="privacy-title">
          <h1 id="privacy-title" className={styles.title}>
            Privacy Policy
          </h1>
          <p className={styles.updated}>Last updated: {LAST_UPDATED}</p>
          {SECTIONS.map((s) => (
            <section key={s.heading} className={styles.section}>
              <h2 className={styles.heading}>{s.heading}</h2>
              <p>{s.body}</p>
            </section>
          ))}
          <section className={styles.section}>
            <h2 className={styles.heading}>Contact.</h2>
            <p>{CONTACT_EMAIL}</p>
          </section>
        </article>
        <a href="/" className={styles.back}>
          <ArrowLeft size={18} aria-hidden="true" />
          Back to ScamGuard
        </a>
      </main>
      <SiteFooter />
    </div>
  );
}
