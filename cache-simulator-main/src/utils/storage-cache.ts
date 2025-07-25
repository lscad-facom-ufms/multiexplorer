const CACHE_KEY = "cache-configurations";

function replacer(_key: string, value: any) {
  return typeof value === "bigint" ? value.toString() : value;
}

function reviver(key: string, value: any) {
  const bigintKeys = [
    "sets",
    "blocksPerSet",
    "wordsPerBlock",
    "wordSize",
    "hitTime",
    "missPenalty",
  ];
  if (bigintKeys.includes(key) && typeof value === "string") {
    return BigInt(value);
  }
  return value;
}

export function saveCaches(caches: any[][]) {
  localStorage.setItem(CACHE_KEY, JSON.stringify(caches, replacer));
}

export function loadCaches(): any[][] | null {
  const data = localStorage.getItem(CACHE_KEY);
  if (!data) return null;
  const parsed = JSON.parse(data, reviver);
  return parsed.map((item: any) => (Array.isArray(item) ? item : [item]));
}

export function addCache(newCache: any[]) {
  const caches = loadCaches() || [];
  caches.push(newCache);
  saveCaches(caches);
}

export function deleteCacheAtIndex(index: number) {
  const caches = loadCaches() || [];
  caches.splice(index, 1);
  saveCaches(caches);
}
