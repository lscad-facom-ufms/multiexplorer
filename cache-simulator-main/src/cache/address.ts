export class Address {
    constructor(
        public readonly raw: bigint,
        public readonly tag: bigint,
        public readonly index: bigint,
        public readonly blockOffset: bigint,
        public readonly byteOffset: bigint,
    ) {
    }
}
