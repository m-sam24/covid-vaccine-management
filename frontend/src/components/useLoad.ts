import { useCallback, useEffect, useState } from "react";
import { useToast } from "./Toast";

// Fetches data on mount; `reload` refetches after a mutation.
export function useLoad<T>(load: () => Promise<T>, initial: T) {
  const notify = useToast();
  const [data, setData] = useState<T>(initial);

  const reload = useCallback(() => {
    load().then(setData).catch((err: Error) => notify(err.message, true));
  }, []);

  useEffect(reload, [reload]);
  return [data, reload] as const;
}
