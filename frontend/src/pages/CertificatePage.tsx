import { useState } from "react";
import { api } from "../api";
import { KeyValue } from "../components/KeyValue";
import { useSubmit } from "../components/form";
import type { Certificate } from "../types";

const CERT_LABELS: Partial<Record<keyof Certificate, string>> = {
  name: "Name", adharno: "Aadhaar No.", age: "Age", phone: "Phone",
  regid: "Registration ID", ndose: "Doses booked",
  DOA1: "Dose 1 date", h_id1: "Dose 1 hospital", amt1: "Dose 1 amount",
  DOA2: "Dose 2 date", h_id2: "Dose 2 hospital", amt2: "Dose 2 amount",
};

export function CertificatePage() {
  const [cert, setCert] = useState<{ data: Certificate; dose: 1 | 2 } | null>(null);

  const lookup = useSubmit(async (f) => {
    setCert(null);
    const dose = f.num("dose") as 1 | 2;
    setCert({ data: await api.getCertificate(f.num("adharno"), dose), dose });
  });

  return (
    <>
      <form className="card" onSubmit={lookup.onSubmit}>
        <h2>Get certificate</h2>
        <div className="row">
          <label>Aadhaar No. <input name="adharno" type="number" required /></label>
          <label>
            Dose
            <select name="dose">
              <option value={1}>Dose 1</option>
              <option value={2}>Dose 2</option>
            </select>
          </label>
        </div>
        <button disabled={lookup.pending}>View certificate</button>
      </form>
      {cert && (
        <div className="card certificate">
          <h2>Vaccination Certificate (Dose {cert.dose})</h2>
          <KeyValue data={cert.data} labels={CERT_LABELS} />
        </div>
      )}
    </>
  );
}
