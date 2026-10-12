import { useEffect, useState, type ComponentType } from "react";
import { api } from "./api";
import { BookPage } from "./pages/BookPage";
import { CertificatePage } from "./pages/CertificatePage";
import { DosesPage } from "./pages/DosesPage";
import { HospitalsPage } from "./pages/HospitalsPage";
import { RegisterPage } from "./pages/RegisterPage";
import { UsersPage } from "./pages/UsersPage";

interface Tab {
  id: string;
  label: string;
  page: ComponentType;
  admin?: boolean;
}

const TABS: Tab[] = [
  { id: "register", label: "Register", page: RegisterPage },
  { id: "book", label: "Book Vaccine", page: BookPage },
  { id: "certificate", label: "Certificate", page: CertificatePage },
  { id: "hospitals", label: "Hospitals", page: HospitalsPage, admin: true },
  { id: "doses", label: "Doses", page: DosesPage, admin: true },
  { id: "users", label: "Users", page: UsersPage, admin: true },
];

type Status = "checking" | "connected" | "offline";

export default function App() {
  const [active, setActive] = useState(TABS[0].id);
  const [status, setStatus] = useState<Status>("checking");

  useEffect(() => {
    api.health().then(() => setStatus("connected"), () => setStatus("offline"));
  }, []);

  const Page = TABS.find((t) => t.id === active)!.page;

  const tabButton = (t: Tab) => (
    <button key={t.id} className={t.id === active ? "active" : ""} onClick={() => setActive(t.id)}>
      {t.label}
    </button>
  );

  return (
    <>
      <header>
        <h1>COVID Vaccine Management</h1>
        <span className={`badge ${status === "connected" ? "ok" : status === "offline" ? "err" : ""}`}>
          API {status}
        </span>
      </header>
      <nav>
        {TABS.filter((t) => !t.admin).map(tabButton)}
        <span className="sep">Admin:</span>
        {TABS.filter((t) => t.admin).map(tabButton)}
      </nav>
      <main>
        {/* key remounts the page so it refetches whenever the tab is opened */}
        <Page key={active} />
      </main>
    </>
  );
}
