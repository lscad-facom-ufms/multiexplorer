export class CacheParameters {
    constructor(
        public readonly sets: bigint,
        public readonly blocksPerSet: bigint,
        public readonly wordsPerBlock: bigint,
        public readonly wordSize: bigint, // bits
        public readonly hitTime: bigint, // ns
        public readonly missPenalty: bigint, // ns
        public readonly policy: 'LRU' | 'FIFO',
    ) {
    }
}
