import { api } from "../api";
import { DataTable } from "../components/DataTable";
import { useToast } from "../components/Toast";
import { useSubmit } from "../components/form";
import { useLoad } from "../components/useLoad";

export function HospitalsPage() {
  const notify = useToast();
  const [hospitals, reload] = useLoad(api.listHospitals, []);

  const insertDummy = async () => {
    try {
      notify((await api.insertDummyHospitals()).message);
      reload();
    } catch (err) {
      notify((err as Error).message, true);
    }
  };

  const add = useSubmit(async (f) => {
    const res = await api.addHospital({
      hospital_name: f.str("hospital_name"),
      address: f.str("address"),
      pincode: f.num("pincode"),
      phone: f.num("phone"),
      dr_name: f.str("dr_name"),
    });
    notify(`${res.message} (ID ${res.h_id})`);
    reload();
    return true;
  });

  const update = useSubmit(async (f) => {
    const res = await api.updateHospital(f.num("h_id"), { phone: f.optNum("phone"), dr_name: f.optStr("dr_name") });
    notify(res.message);
    reload();
    return true;
  });

  return (
    <>
      <div className="card">
        <div className="card-head">
          <h2>Hospitals</h2>
          <button type="button" className="secondary" onClick={insertDummy}>Insert sample hospitals</button>
        </div>
        <DataTable
          rows={hospitals}
          rowKey={(h) => h.h_id}
          columns={[["h_id", "ID"], ["hospital_name", "Name"], ["address", "Address"], ["pincode", "Pincode"], ["phone", "Phone"], ["dr_name", "Doctor"]]}
        />
      </div>
      <div className="grid">
        <form className="card" onSubmit={add.onSubmit}>
          <h2>Add hospital</h2>
          <label>Name <input name="hospital_name" maxLength={30} required /></label>
          <label>Address <input name="address" maxLength={50} required /></label>
          <label>Pincode <input name="pincode" type="number" required /></label>
          <label>Phone <input name="phone" type="number" required /></label>
          <label>Doctor <input name="dr_name" maxLength={20} required /></label>
          <button disabled={add.pending}>Add</button>
        </form>
        <form className="card" onSubmit={update.onSubmit}>
          <h2>Update hospital</h2>
          <label>Hospital ID <input name="h_id" type="number" required /></label>
          <label>New phone <input name="phone" type="number" /></label>
          <label>New doctor <input name="dr_name" maxLength={20} /></label>
          <button disabled={update.pending}>Update</button>
        </form>
      </div>
    </>
  );
}
