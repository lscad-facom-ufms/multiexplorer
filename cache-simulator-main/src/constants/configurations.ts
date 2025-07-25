import {CacheParameters} from "../cache/cache-parameters.ts";

const DEFAULT_WORDS_CAPACITY = 2n ** 14n / 64n;

export const CACHE_CONFIGURATIONS: CacheParameters[][] = [
    [{
        sets: 64n,
        blocksPerSet: 1n,
        wordsPerBlock: DEFAULT_WORDS_CAPACITY / 64n,
        wordSize: 64n,
        hitTime: 1n,
        missPenalty: 10n,
        policy: 'LRU',
    }], [{
        sets: 32n,
        blocksPerSet: 2n,
        wordsPerBlock: DEFAULT_WORDS_CAPACITY / 2n / 32n,
        wordSize: 64n,
        hitTime: 1n,
        missPenalty: 10n,
        policy: 'LRU',
    }], [{
        sets: 1n,
        blocksPerSet: DEFAULT_WORDS_CAPACITY / 16n,
        wordsPerBlock: 16n,
        wordSize: 64n,
        hitTime: 1n,
        missPenalty: 10n,
        policy: 'LRU',
    }],
];
