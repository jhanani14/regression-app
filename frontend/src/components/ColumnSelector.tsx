type Props = {
  columns: string[];
  target: string;
  setTarget: (t: string) => void;
  features: string[];
  setFeatures: (f: string[]) => void;
};

export default function ColumnSelector({ columns, target, setTarget, features, setFeatures }: Props) {
  const toggleFeature = (c: string) =>
    setFeatures(features.includes(c) ? features.filter((x) => x !== c) : [...features, c]);

  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="glass p-4">
        <div className="label">Target</div>
        <select className="input" value={target} onChange={(e) => setTarget(e.target.value)}>
          <option value="" disabled>Select target</option>
          {columns.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>
      <div className="glass p-4">
        <div className="label">Features</div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-1 max-h-56 overflow-auto pr-1">
          {columns.map((c) => (
            <label key={c} className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={features.includes(c)} onChange={() => toggleFeature(c)} />
              <span>{c}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
