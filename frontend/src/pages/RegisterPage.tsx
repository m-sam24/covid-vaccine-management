import { useState } from "react";
import { api } from "../api";
import { KeyValue } from "../components/KeyValue";
import { useToast } from "../components/Toast";
import { useSubmit } from "../components/form";
import type { User } from "../types";

export const USER_LABELS = { adharno: "Aadhaar No.", name: "Name", age: "Age", phone: "Phone" } as const;

export function RegisterPage() {
  const notify = useToast();
  const [found, setFound] = useState<User | string | null>(null);

  const register = useSubmit(async (f) => {
    const res = await api.registerUser({ adharno: f.num("adharno"), name: f.str("name"), age: f.num("age"), phone: f.str("phone") });
    notify(res.message);
    return true;
  });

  const find = useSubmit(async (f) => {
    try {
      setFound(await api.getUserByPhone(f.str("phone")));
    } catch (err) {
      setFound((err as Error).message);
    }
  });

  const update = useSubmit(async (f) => {
    const changes = { name: f.optStr("name"), age: f.optNum("age"), phone: f.optStr("phone") };
    if (Object.values(changes).every((v) => v === undefined)) throw new Error("Enter at least one field to change");
    const res = await api.updateUser(f.num("adharno"), changes);
    notify(res.message);
    return true;
  });

  return (
    <div className="grid">
      <form className="card" onSubmit={register.onSubmit}>
        <h2>Register</h2>
        <label>Aadhaar No. <input name="adharno" type="number" required /></label>
        <label>Name <input name="name" maxLength={25} required /></label>
        <label>Age <input name="age" type="number" min={0} required /></label>
        <label>Phone <input name="phone" maxLength={11} required /></label>
        <button disabled={register.pending}>Register</button>
      </form>

      <div className="card">
        <h2>Find by phone</h2>
        <form className="inline" onSubmit={find.onSubmit}>
          <input name="phone" placeholder="Phone" required />
          <button disabled={find.pending}>Search</button>
        </form>
        {typeof found === "string" && <p className="empty">{found}</p>}
        {found && typeof found === "object" && <KeyValue data={found} labels={USER_LABELS} />}
      </div>

      <form className="card" onSubmit={update.onSubmit}>
        <h2>Update details</h2>
        <label>Aadhaar No. <input name="adharno" type="number" required /></label>
        <label>New name <input name="name" maxLength={25} /></label>
        <label>New age <input name="age" type="number" min={0} /></label>
        <label>New phone <input name="phone" maxLength={11} /></label>
        <button disabled={update.pending}>Update</button>
      </form>
    </div>
  );
}
