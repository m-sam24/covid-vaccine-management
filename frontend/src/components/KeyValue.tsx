export function KeyValue<T extends object>({ data, labels }: { data: T; labels: Partial<Record<keyof T, string>> }) {
  const entries = (Object.entries(labels) as [keyof T & string, string][]).filter(
    ([key]) => data[key] !== undefined && data[key] !== null,
  );
  return (
    <dl className="kv">
      {entries.map(([key, label]) => (
        <div key={key} style={{ display: "contents" }}>
          <dt>{label}</dt>
          <dd>{String(data[key])}</dd>
        </div>
      ))}
    </dl>
  );
}
