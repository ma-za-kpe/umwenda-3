"use client";
// A React view of one local collection (lib/db.ts) with the screen states the
// design spec names: loading, empty, ready and error. A client island reads
// it after hydration, so the server's HTML never depends on this device.
import { useCallback, useEffect, useMemo, useState } from "react";
import { collection, newId, type Saved } from "@/lib/db";

export type Status = "loading" | "ready" | "error";

export function useCollection<T>(kind: string) {
  const store = useMemo(() => collection<T>(kind), [kind]);
  const [items, setItems] = useState<Saved<T>[]>([]);
  const [status, setStatus] = useState<Status>("loading");

  const reload = useCallback(async () => {
    try {
      setItems(await store.all());
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  }, [store]);

  useEffect(() => {
    void reload();
  }, [reload]);

  const add = useCallback(
    async (value: T) => {
      const id = newId();
      await store.put(id, value);
      await reload();
      return id;
    },
    [store, reload],
  );
  const update = useCallback(
    async (id: string, value: T) => {
      await store.put(id, value);
      await reload();
    },
    [store, reload],
  );
  const remove = useCallback(
    async (id: string) => {
      await store.remove(id);
      await reload();
    },
    [store, reload],
  );

  return { items, status, add, update, remove, reload };
}
