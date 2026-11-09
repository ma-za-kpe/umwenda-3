// The product's local database: offline first, on this device only (owner
// decision D1). Every record lives in the browser's IndexedDB through the
// pinned `idb` wrapper; nothing is sent anywhere. A collection is one kind of
// record ("routes", "estimates", "boards"...) in one object store keyed by
// [kind, id], so a product adds collections without a schema migration.
// Where IndexedDB is missing (a private window that refuses it, or the
// build's own prerender) the same API keeps records in memory for the visit.
import { openDB, type IDBPDatabase } from "idb";

const NAME = "crew-local";
const VERSION = 1;
const STORE = "records";

export type Saved<T> = { id: string; value: T; updated: number };

type Row = { kind: string; id: string; value: unknown; updated: number };

let opening: Promise<IDBPDatabase | null> | null = null;
const memory = new Map<string, Map<string, Row>>();

function database(): Promise<IDBPDatabase | null> {
  if (opening) return opening;
  opening =
    typeof indexedDB === "undefined"
      ? Promise.resolve(null)
      : openDB(NAME, VERSION, {
          upgrade(db) {
            const store = db.createObjectStore(STORE, { keyPath: ["kind", "id"] });
            store.createIndex("kind", "kind");
          },
        }).catch(() => null);
  return opening;
}

function inMemory(kind: string): Map<string, Row> {
  let rows = memory.get(kind);
  if (!rows) {
    rows = new Map();
    memory.set(kind, rows);
  }
  return rows;
}

/** A new record id: random, so two tabs never collide. */
export function newId(): string {
  const bytes = new Uint8Array(12);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

export interface Collection<T> {
  all(): Promise<Saved<T>[]>;
  get(id: string): Promise<Saved<T> | undefined>;
  put(id: string, value: T): Promise<Saved<T>>;
  remove(id: string): Promise<void>;
  clear(): Promise<void>;
}

/** One kind of record, newest first. `now` is injectable for tests. */
export function collection<T>(kind: string, now: () => number = Date.now): Collection<T> {
  const saved = (row: Row): Saved<T> => ({ id: row.id, value: row.value as T, updated: row.updated });
  return {
    async all() {
      const db = await database();
      const rows: Row[] = db
        ? await db.getAllFromIndex(STORE, "kind", kind)
        : Array.from(inMemory(kind).values());
      return rows.sort((a, b) => b.updated - a.updated).map(saved);
    },
    async get(id) {
      const db = await database();
      const row: Row | undefined = db ? await db.get(STORE, [kind, id]) : inMemory(kind).get(id);
      return row ? saved(row) : undefined;
    },
    async put(id, value) {
      const row: Row = { kind, id, value, updated: now() };
      const db = await database();
      if (db) await db.put(STORE, row);
      else inMemory(kind).set(id, row);
      return saved(row);
    },
    async remove(id) {
      const db = await database();
      if (db) await db.delete(STORE, [kind, id]);
      else inMemory(kind).delete(id);
    },
    async clear() {
      const db = await database();
      if (!db) {
        inMemory(kind).clear();
        return;
      }
      const keys = await db.getAllKeysFromIndex(STORE, "kind", kind);
      const done = db.transaction(STORE, "readwrite");
      await Promise.all([...keys.map((key) => done.store.delete(key)), done.done]);
    },
  };
}
