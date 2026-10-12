import type { ReactNode } from "react";

export type Column<T> = [key: keyof T & string, label: string];

interface Props<T> {
  rows: T[];
  columns: Column<T>[];
  rowKey: (row: T) => string | number;
  actions?: (row: T) => ReactNode;
}

export function DataTable<T>({ rows, columns, rowKey, actions }: Props<T>) {
  if (!rows.length) return <p className="empty">No records yet.</p>;
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map(([key, label]) => <th key={key}>{label}</th>)}
            {actions && <th />}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={rowKey(row)}>
              {columns.map(([key]) => <td key={key}>{String(row[key] ?? "")}</td>)}
              {actions && <td>{actions(row)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
