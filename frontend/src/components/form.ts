import { useState, type FormEvent } from "react";
import { useToast } from "./Toast";

// Typed readers over a submitted form's FormData. Empty inputs read as undefined.
export class Fields {
  constructor(private fd: FormData) {}

  optStr(name: string): string | undefined {
    const v = this.fd.get(name);
    return typeof v === "string" && v.trim() !== "" ? v.trim() : undefined;
  }
  str(name: string): string {
    return this.optStr(name) ?? "";
  }
  optNum(name: string): number | undefined {
    const v = this.optStr(name);
    return v === undefined ? undefined : Number(v);
  }
  num(name: string): number {
    return this.optNum(name) ?? 0;
  }
}

// Wraps a submit handler: prevents default, disables the form while pending, toasts errors,
// and resets the form if the handler returns true.
export function useSubmit(handler: (f: Fields) => Promise<boolean | void>) {
  const notify = useToast();
  const [pending, setPending] = useState(false);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    setPending(true);
    try {
      if (await handler(new Fields(new FormData(form)))) form.reset();
    } catch (err) {
      notify((err as Error).message, true);
    } finally {
      setPending(false);
    }
  };

  return { onSubmit, pending };
}
