import { api } from "../api";
import { DataTable } from "../components/DataTable";
import { useToast } from "../components/Toast";
import { useSubmit } from "../components/form";
import { useLoad } from "../components/useLoad";
import type { User } from "../types";

export function UsersPage() {
  const notify = useToast();
  const [users, reload] = useLoad(api.listUsers, []);

  const remove = async (u: User) => {
    if (!confirm(`Delete user ${u.name} (${u.adharno})?`)) return;
    try {
      notify((await api.deleteUser(u.adharno)).message);
      reload();
    } catch (err) {
      notify((err as Error).message, true);
    }
  };

  const mark = useSubmit(async (f) => {
    notify((await api.markVaccinated(f.num("adharno"))).message);
    return true;
  });

  return (
    <>
      <div className="card">
        <h2>Registered users</h2>
        <DataTable
          rows={users}
          rowKey={(u) => u.adharno}
          columns={[["adharno", "Aadhaar No."], ["name", "Name"], ["age", "Age"], ["phone", "Phone"]]}
          actions={(u) => <button type="button" className="small danger" onClick={() => remove(u)}>Delete</button>}
        />
      </div>
      <form className="card" onSubmit={mark.onSubmit}>
        <h2>Mark as vaccinated</h2>
        <p className="hint">Marks dose 1 as given, or dose 2 if dose 1 is already marked.</p>
        <div className="row">
          <label>Aadhaar No. <input name="adharno" type="number" required /></label>
        </div>
        <button disabled={mark.pending}>Mark vaccinated</button>
      </form>
    </>
  );
}
