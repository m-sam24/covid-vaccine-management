import { useRef } from "react";
import { api } from "../api";
import { DataTable } from "../components/DataTable";
import { useToast } from "../components/Toast";
import { useSubmit } from "../components/form";
import { useLoad } from "../components/useLoad";
import type { Dose, SlotAvailability, SlotNumber } from "../types";

const SLOTS: SlotNumber[] = [1, 2, 3, 4];
type Row = SlotAvailability & { price?: number };

const doseKey = (hid: number, date: string) => `${hid}|${date}`;

async function loadRows(): Promise<Row[]> {
  const [slots, doses] = await Promise.all([api.availableSlots(), api.listDoses()]);
  const byKey = new Map<string, Dose>(doses.map((d) => [doseKey(d.hid, d.dose_date), d]));
  return slots.map((s) => ({ ...s, price: byKey.get(doseKey(s.hid, s.dose_date))?.price }));
}

export function BookPage() {
  const notify = useToast();
  const formRef = useRef<HTMLFormElement>(null);
  const [rows, reload] = useLoad(loadRows, []);

  const pick = (row: Row, slot: SlotNumber) => {
    const form = formRef.current!;
    const set = (name: string, value: string | number | undefined) =>
      ((form.elements.namedItem(name) as HTMLInputElement).value = value === undefined ? "" : String(value));
    set("hid", row.hid);
    set("dose_date", row.dose_date);
    set("slot", slot);
    set("amt2", row.price);
    (form.elements.namedItem("adharno") as HTMLInputElement).focus();
  };

  const book = useSubmit(async (f) => {
    const res = await api.bookVaccine({
      adharno: f.num("adharno"),
      hid: f.num("hid"),
      slot: f.num("slot") as SlotNumber,
      dose_date: f.str("dose_date"),
      amt2: f.optNum("amt2"),
    });
    notify(res.amount !== undefined ? `${res.message} (Reg ID ${res.regid}, amount ₹${res.amount})` : res.message);
    reload();
    return true;
  });

  return (
    <>
      <div className="card">
        <h2>Available slots</h2>
        <p className="hint">Pick a slot, then enter your Aadhaar number below.</p>
        <DataTable
          rows={rows}
          rowKey={(r) => doseKey(r.hid, r.dose_date)}
          columns={[["hid", "Hospital ID"], ["dose_name", "Dose"], ["dose_date", "Date"], ["price", "Price"]]}
          actions={(r) => (
            <div className="actions">
              {SLOTS.map((n) => {
                const left = r[`slot${n}_left`];
                return (
                  <button key={n} type="button" className={`small${left > 0 ? "" : " secondary"}`} disabled={left <= 0} onClick={() => pick(r, n)}>
                    Slot {n} · {left} left
                  </button>
                );
              })}
            </div>
          )}
        />
      </div>

      <form ref={formRef} className="card" onSubmit={book.onSubmit}>
        <h2>Book</h2>
        <div className="row">
          <label>Aadhaar No. <input name="adharno" type="number" required /></label>
          <label>Hospital ID <input name="hid" type="number" required /></label>
          <label>Dose date <input name="dose_date" type="date" required /></label>
          <label>
            Slot
            <select name="slot" required>
              {SLOTS.map((n) => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>
          <label>Amount (dose 2) <input name="amt2" type="number" min={0} /></label>
        </div>
        <button disabled={book.pending}>Book vaccine</button>
      </form>
    </>
  );
}
