import { api } from "../api";
import { DataTable, type Column } from "../components/DataTable";
import { useToast } from "../components/Toast";
import { useSubmit } from "../components/form";
import { useLoad } from "../components/useLoad";
import type { Dose } from "../types";

const COLUMNS: Column<Dose>[] = [
  ["did", "ID"], ["hid", "Hospital"], ["dose_name", "Name"], ["price", "Price"], ["dose_date", "Date"],
  ["slot1", "S1"], ["slot1_used", "S1 used"], ["slot2", "S2"], ["slot2_used", "S2 used"],
  ["slot3", "S3"], ["slot3_used", "S3 used"], ["slot4", "S4"], ["slot4_used", "S4 used"],
];

export function DosesPage() {
  const notify = useToast();
  const [doses, reload] = useLoad(api.listDoses, []);

  const add = useSubmit(async (f) => {
    const res = await api.addDose({
      hid: f.optNum("hid"),
      dose_name: f.str("dose_name"),
      price: f.num("price"),
      dose_date: f.str("dose_date"),
      slot1: f.num("slot1"),
      slot2: f.num("slot2"),
      slot3: f.num("slot3"),
      slot4: f.num("slot4"),
    });
    notify(`${res.message} (ID ${res.did}, hospital ${res.hid})`);
    reload();
    return true;
  });

  return (
    <>
      <div className="card">
        <h2>Dose details</h2>
        <DataTable rows={doses} rowKey={(d) => d.did} columns={COLUMNS} />
      </div>
      <form className="card" onSubmit={add.onSubmit}>
        <h2>Add dose</h2>
        <div className="row">
          <label>Hospital ID <input name="hid" type="number" /></label>
          <label>Dose name <input name="dose_name" maxLength={15} required /></label>
          <label>Price <input name="price" type="number" min={0} required /></label>
          <label>Date <input name="dose_date" type="date" required /></label>
        </div>
        <div className="row">
          {[1, 2, 3, 4].map((n) => (
            <label key={n}>Slot {n} capacity <input name={`slot${n}`} type="number" min={0} required /></label>
          ))}
        </div>
        <button disabled={add.pending}>Add dose</button>
      </form>
    </>
  );
}
