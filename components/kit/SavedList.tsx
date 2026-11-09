"use client";
// EXAMPLE ONLY (#326): a route that places this island is refused before it is
// pushed; the product writes its own island in components/Name.tsx.
// A client island on the local database: add, list and remove notes kept on
// this device. It shows every screen state (loading, empty, ready, error).
// A saved note rises in and a removed one fades out with the pinned motion
// library's small `animate` (`motion/mini`, on the browser's own animation
// engine: about 2 KB, so the page's first load stays light on a phone), and
// nothing moves when the visitor asks for reduced motion. Reach for
// `motion/react` only in an island that needs springs, gestures or layout
// animation. The crew replaces this island with the product's own core
// feature, built the same way.
import { animate } from "motion/mini";
import { useEffect, useId, useRef, useState } from "react";
import { useCollection } from "./useCollection";

type Note = { text: string };

const still = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

export default function SavedList({ kind = "notes", label = "Note" }: { kind?: string; label?: string }) {
  const { items, status, add, remove } = useCollection<Note>(kind);
  const [draft, setDraft] = useState("");
  const [fresh, setFresh] = useState<string | null>(null);
  const rows = useRef(new Map<string, HTMLLIElement>());
  const field = useId();
  const save = async () => {
    const text = draft.trim();
    if (!text) return;
    setFresh(await add({ text }));
    setDraft("");
  };
  useEffect(() => {
    const row = fresh ? rows.current.get(fresh) : undefined;
    if (row && !still()) {
      animate(row, { opacity: [0, 1], transform: ["translateY(8px)", "none"] }, { duration: 0.2 });
    }
  }, [fresh]);
  const discard = async (id: string) => {
    const row = rows.current.get(id);
    if (row && !still()) await animate(row, { opacity: 0 }, { duration: 0.2 });
    await remove(id);
  };
  return (
    <div className="saved-list">
      <label htmlFor={field}>{label}</label>
      <div className="saved-list__entry">
        <input
          id={field}
          value={draft}
          maxLength={200}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") void save();
          }}
        />
        <button type="button" className="button" onClick={() => void save()}>
          Save on this device
        </button>
      </div>
      <p className="saved-list__status" role="status" aria-live="polite">
        {status === "loading" && "Opening this device's notes…"}
        {status === "error" && "This browser will not keep notes; they last for this visit."}
        {status === "ready" && items.length === 0 && "Nothing saved yet."}
        {status === "ready" && items.length > 0 && `${items.length} saved on this device.`}
      </p>
      <ul className="saved-list__items">
        {items.map((item) => (
          <li
            key={item.id}
            ref={(row) => {
              if (row) rows.current.set(item.id, row);
              else rows.current.delete(item.id);
            }}
          >
            <span>{item.value.text}</span>
            <button type="button" className="button button--quiet" onClick={() => void discard(item.id)}>
              Remove<span className="visually-hidden"> {item.value.text}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
