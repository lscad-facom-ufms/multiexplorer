import {CacheSimulator} from "./cache-simulator.ts";
import {Address} from "./address.ts";
import {CacheBlockAccess} from "./cache-block-access.ts";

export class CacheBlock {
    valid = false; // TODO deal with this later

    tag: bigint;
    data: bigint[];

    accessHistory: Record<number, CacheBlockAccess> = {};

    lastAccessedAt = 0;
    loadedAt = 0;

    constructor(
        private readonly cache: CacheSimulator,
        public readonly index: number
    ) {

        this.tag = 0n;
        this.data = [];
    }

    getTag() {
        return this.tag;
    }

    getIndex() {
        return this.index;
    }

    read(address: Address): CacheBlockAccess {
        this.cache.reads++;

        console.log(`Cache ${this.cache.getLevel()} reading 0x${address.raw.toString(16)}`)

        console.log(this.cache);

        if (this.valid && this.tag === address.tag) {
            this.cache.hits++;
            this.lastAccessedAt = this.cache.runner.getCurrentCycle();
            this.accessHistory[this.cache.runner.getCurrentCycle()] = {
                hit: true,
                address: address.raw,
            }
            return this.accessHistory[this.cache.runner.getCurrentCycle()];
        }

        this.cache.misses++;
        this.cache.underlying.read(address.raw);
        this.loadedAt = this.cache.runner.getCurrentCycle();
        this.lastAccessedAt = this.cache.runner.getCurrentCycle();
        this.tag = address.tag;
        this.valid = true;

        this.accessHistory[this.cache.runner.getCurrentCycle()] = {
            hit: false,
            address: address.raw,
        }

        return this.accessHistory[this.cache.runner.getCurrentCycle()];
    }

    write(address: Address, data: bigint) {
        this.cache.writes++;

        // TODO assert offset is within bounds
        const offset = Number(address.blockOffset);

        this.data[offset] = data;
        // TODO implement write policies
        this.cache.underlying.write(address.raw, data);
    }
}
