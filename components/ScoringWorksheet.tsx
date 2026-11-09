"use client";
// M1 + M2: the collateral-free credit scoring worksheet. The analyst enters a
// collateral-less trader's alternative data and the island scores it live,
// with a written rationale and a recommended decision. Keeping a score writes
// it to this device through lib/db.ts (M3). No network, no server, no account.
import { useMemo, useState } from "react";
import { useCollection } from "@/components/kit/useCollection";
import { scoreTrader, type TraderInput } from "@/lib/scoring";

export type ScoredRecord = {
  trader: TraderInput;
  score: number;
  decision: string;
  rationale: string;
};

const empty = { name: "", inflow: "", outflow: "", sales: "", pastLoans: "", repaidOnTime: "" };

function toNumber(value: string): number {
  const n = Number(value);
  return Number.isFinite(n) && n >= 0 ? n : 0;
}

export default function ScoringWorksheet() {
  const [form, setForm] = useState(empty);
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState(false);
  const { items, status, add } = useCollection<ScoredRecord>("scored-traders");

  const input: TraderInput = useMemo(
    () => ({
      name: form.name.trim(),
      inflow: toNumber(form.inflow),
      outflow: toNumber(form.outflow),
      sales: toNumber(form.sales),
      pastLoans: toNumber(form.pastLoans),
      repaidOnTime: toNumber(form.repaidOnTime),
    }),
    [form],
  );

  const hasData =
    input.name !== "" ||
    input.inflow > 0 ||
    input.outflow > 0 ||
    input.sales > 0 ||
    input.pastLoans > 0;

  const result = useMemo(() => (hasData ? scoreTrader(input) : null), [hasData, input]);

  const set = (key: keyof typeof empty) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f) => ({ ...f, [key]: event.target.value }));
    setSaved(false);
  };

  const keep = async () => {
    if (!result || saving) return;
    setSaving(true);
    setSaveError(false);
    try {
      await add({ trader: input, score: result.score, decision: result.decision, rationale: result.rationale });
      setSaved(true);
    } catch {
      setSaveError(true);
    } finally {
      setSaving(false);
    }
  };

  const reset = () => {
    setForm(empty);
    setSaved(false);
    setSaveError(false);
  };

  return (
    <div className="worksheet">
      <h3>Enter the trader's alternative data</h3>
      <p className="worksheet__intro">
        One-off, offline scoring for a single collateral-less trader. The score, the rationale and the
        recommended decision update as the figures change.
      </p>
      <div className="worksheet__form">
        <label htmlFor="ws-name">Trader name</label>
        <input id="ws-name" value={form.name} onChange={set("name")} placeholder="e.g. Keza" />
        <div className="worksheet__row">
          <div>
            <label htmlFor="ws-inflow">Monthly mobile-money inflow (RWF)</label>
            <input id="ws-inflow" inputMode="numeric" value={form.inflow} onChange={set("inflow")} placeholder="0" />
          </div>
          <div>
            <label htmlFor="ws-outflow">Monthly mobile-money outflow (RWF)</label>
            <input id="ws-outflow" inputMode="numeric" value={form.outflow} onChange={set("outflow")} placeholder="0" />
          </div>
        </div>
        <label htmlFor="ws-sales">Average monthly market sales (RWF)</label>
        <input id="ws-sales" inputMode="numeric" value={form.sales} onChange={set("sales")} placeholder="0" />
        <div className="worksheet__row">
          <div>
            <label htmlFor="ws-loans">Past loans</label>
            <input id="ws-loans" inputMode="numeric" value={form.pastLoans} onChange={set("pastLoans")} placeholder="0" />
          </div>
          <div>
            <label htmlFor="ws-repaid">Repaid on time</label>
            <input id="ws-repaid" inputMode="numeric" value={form.repaidOnTime} onChange={set("repaidOnTime")} placeholder="0" />
          </div>
        </div>
        <div className="worksheet__actions">
          <button type="button" className="button button--gold" onClick={() => { void keep(); }} aria-label="Keep this score on this device">
            Keep this score on this device
          </button>
          <button type="button" className="button button--quiet" onClick={reset}>
            Clear
          </button>
        </div>
      </div>
      <div className="worksheet__result" role="status" aria-live="polite">
        {status === "loading" && <p className="worksheet__state">Counting the marks in the circle.</p>}
        {status === "error" && (
          <p className="worksheet__state worksheet__state--error">The standing did not save. Check the line and enter it again.</p>
        )}
        {!hasData && status !== "loading" && (
          <p className="worksheet__state">No standing entered yet. Start with the person, not the form.</p>
        )}
        {status === "ready" && items.length === 0 && !hasData && (
          <p className="worksheet__state">No standing entered yet. Start with the person, not the form.</p>
        )}
        {result && (
          <div className="worksheet__score">
            <p className="worksheet__score-line">
              Creditworthiness: <strong>{result.score}</strong> / 100
            </p>
            <p className={`worksheet__decision worksheet__decision--${result.decision.replace(/[^a-z]/g, "")}`}>
              Recommended decision: <strong>{result.decision}</strong>
            </p>
            <p className="worksheet__rationale">{result.rationale}</p>
          </div>
        )}
        {saved && <p className="worksheet__kept">Kept on this device. Find it under Kept records.</p>}
        {saveError && (
          <p className="worksheet__state worksheet__state--error">The standing did not save. Check the line and enter it again.</p>
        )}
      </div>
    </div>
  );
}
