import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from "react";

type Notify = (message: string, isError?: boolean) => void;

const ToastContext = createContext<Notify>(() => {});

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<{ message: string; isError: boolean } | null>(null);
  const timer = useRef<number | undefined>(undefined);

  const notify = useCallback<Notify>((message, isError = false) => {
    setToast({ message, isError });
    clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setToast(null), 3500);
  }, []);

  return (
    <ToastContext.Provider value={notify}>
      {children}
      {toast && <div className={`toast${toast.isError ? " err" : ""}`}>{toast.message}</div>}
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
