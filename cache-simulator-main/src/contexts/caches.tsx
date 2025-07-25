import {
  createContext,
  FC,
  PropsWithChildren,
  useContext,
  useState,
  useEffect,
} from "react";
import { CacheParameters } from "../cache/cache-parameters.ts";
import { ADDRESS_SIZE } from "../constants/arch.ts";
import { loadCaches, saveCaches } from "../utils/storage-cache.ts";

export type CacheContextType = {
  caches: CacheParameters[][];
  setCaches: (caches: CacheParameters[][]) => void;
};

const initialCaches: CacheParameters[][] = [
  [
    {
      sets: 32n,
      blocksPerSet: 2n,
      wordsPerBlock: 8n,
      wordSize: ADDRESS_SIZE,
      hitTime: 1n,
      missPenalty: 10n,
      policy: "LRU",
    },
  ],
  [
    {
      sets: 64n,
      blocksPerSet: 1n,
      wordsPerBlock: 64n,
      wordSize: ADDRESS_SIZE,
      hitTime: 1n,
      missPenalty: 10n,
      policy: "LRU",
    },
  ],
  [
    {
      sets: 1n,
      blocksPerSet: 16n,
      wordsPerBlock: 16n,
      wordSize: ADDRESS_SIZE,
      hitTime: 1n,
      missPenalty: 10n,
      policy: "LRU",
    },
    {
      sets: 32n,
      blocksPerSet: 32n,
      wordsPerBlock: 32n,
      wordSize: ADDRESS_SIZE,
      hitTime: 1n,
      missPenalty: 10n,
      policy: "LRU",
    },
  ],
];

export const CacheContext = createContext<CacheContextType>(
  {} as CacheContextType
);
export const useCaches = () => useContext(CacheContext);

export const CachesProvider: FC<PropsWithChildren> = ({ children }) => {
  const [caches, setCaches] = useState<CacheParameters[][]>(initialCaches);

  useEffect(() => {
    const stored = loadCaches();
    if (stored && stored.length > 0) {
      setCaches(stored);
    } else {
      setCaches(initialCaches);
      saveCaches(initialCaches);
    }
  }, []);

  return (
    <CacheContext.Provider value={{ caches, setCaches }}>
      {children}
    </CacheContext.Provider>
  );
};
