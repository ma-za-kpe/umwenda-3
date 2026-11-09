"use client";
// M3 + M4: the kept records. Scored applications kept on this device, listed
// by trader name and date with score and decision; reopen one for its full
// detail, or pick two to compare side by side. Offline, on-device only.
import { useState } from "react";
import { useCollection } from "@/components/kit/useCollection";
import type { ScoredRecord } from "@/components/ScoringWorksheet";

function dateOf(item: { updated: number }): string {
  const d = new Date(item.updated);
  if (!Number.isNaN(d.getTime())) return d.toLocaleDateString();
  return "—";
}

export default function KeptRecords() {
  const { items, status } = useCollection<ScoredRecord>("scored-traders");
  const [openId, setOpenId] = useState<string | null>(null);
  const [picked, setPicked] = useState<string[]>([]);

  const togglePick = (id: string) => {
    setPicked((p) => (p.includes(id) ? p.filter((x) => x !== id) : p.length >= 2 ? [p[1], id] : [...p, id]));
  };

  const compare = picked.length === 2 ? items.filter((i) => picked.includes(i.id)) : [];
  const open = openId ? items.find((i) => i.id === openId) : undefined;

  return (
    <div className="records">
      <h3>Kept scored applications</h3>
      <p className="records__intro">
        The scored applications kept on this device, available offline. Open one to act on it, or pick two to
        compare side by side.
      </p>
      <p className="records__status" role="status" aria-live="polite">
        {status === "loading" && "Counting the marks in the circle."}
        {status === "error" && "The standing did not save. Check the line and enter it again."}
        {status === "ready" && items.length === 0 && "No standing entered yet. Start with the person, not the form."}
        {status === "ready" && items.length > 0 && `${items.length} record${items.length === 1 ? "" : "s"} kept on this device.`}
      </p>
      {status === "ready" && items.length > 0 && (
        <table className="records__table">
          <caption className="visually-hidden">Kept scored applications</caption>
          <thead>
            <tr>
              <th scope="col">Trader</th>
              <th scope="col">Date</th>
              <th scope="col">Score</th>
              <th scope="col">Decision</th>
              <th scope="col">Compare</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className={picked.includes(item.id) ? "records__row--picked" : undefined}>
                <td>
                  <button type="button" className="records__open" onClick={() => setOpenId(item.id)}>
                    {item.value.trader.name || "Unnamed trader"}
                  </button>
                </td>
                <td>{dateOf(item)}</td>
                <td>{item.value.score}</td>
                <td>{item.value.decision}</td>
                <td>
                  <input
                    type="checkbox"
                    aria-label={`Compare ${item.value.trader.name || "unnamed trader"}`}
                    checked={picked.includes(item.id)}
                    onChange={() => togglePick(item.id)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {open && (
        <div className="records__detail">
          <h4>{open.value.trader.name || "Unnamed trader"}</h4>
          <dl className="records__data">
            <div><dt>Mobile-money inflow</dt><dd>{open.value.trader.inflow.toLocaleString()} RWF</dd></div>
            <div><dt>Mobile-money outflow</dt><dd>{open.value.trader.outflow.toLocaleString()} RWF</dd></div>
            <div><dt>Average monthly market sales</dt><dd>{open.value.trader.sales.toLocaleString()} RWF</dd></div>
            <div><dt>Past loans</dt><dd>{open.value.trader.pastLoans}</dd></div>
            <div><dt>Repaid on time</dt><dd>{open.value.trader.repaidOnTime}</dd></div>
          </dl>
          <p className="records__score">Score: <strong>{open.value.score}</strong> / 100 — {open.value.decision}</p>
          <p className="records__rationale">{open.value.rationale}</p>
        </div>
      )}
      {compare.length === 2 && (
        <div className="records__compare">
          <h4>Side by side</h4>
          <div className="records__compare-grid">
            {compare.map((item) => (
              <div key={item.id} className="records__compare-col">
                <h5>{item.value.trader.name || "Unnamed trader"}</h5>
                <dl className="records__data">
                  <div><dt>Inflow</dt><dd>{item.value.trader.inflow.toLocaleString()}</dd></div>
                  <div><dt>Outflow</dt><dd>{item.value.trader.outflow.toLocaleString()}</dd></div>
                  <div><dt>Sales</dt><dd>{item.value.trader.sales.toLocaleString()}</dd></div>
                  <div><dt>Past loans</dt><dd>{item.value.trader.pastLoans}</dd></div>
                  <div><dt>Repaid on time</dt><dd>{item.value.trader.repaidOnTime}</dd></div>
                </dl>
                <p className="records__score">Score: <strong>{item.value.score}</strong> / 100 — {item.value.decision}</p>
                <p className="records__rationale">{item.value.rationale}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
