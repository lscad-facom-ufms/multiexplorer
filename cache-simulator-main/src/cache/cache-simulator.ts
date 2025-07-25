import {DataStore} from "./data-store.ts";
import {CacheParameters} from "./cache-parameters.ts";
import {CacheSet} from "./cache-set.ts";
import {assertNonFalsy} from "../helpers/assertions.ts";
import {CacheAccess} from "./cache-access.ts";
import {LazyArray} from "../lazy/array.ts";
import {bigintToAddress} from "../helpers/address.ts";
import {CacheRunner} from "./cache-runner.ts";

export class CacheSimulator implements DataStore {
    sets: LazyArray<CacheSet>;

    private level = 0;

    accessHistory: Record<number, CacheAccess> = {};

    reads = 0n;
    writes = 0n;
    hits = 0n;
    misses = 0n;

    constructor(
        public readonly runner: CacheRunner,
        public readonly parameters: CacheParameters,
        public readonly underlying: DataStore,
    ) {
        this.sets = new LazyArray(
            Number(parameters.sets),
            (index) => new CacheSet(this, index),
        )
    }

    setLevel(level: number) {
        this.level = level;
    }

    getAccessForCycle(cycle: number): CacheAccess {
        return this.accessHistory[cycle];
    }

    getLevel() {
        return this.level;
    }

    getSetFromIndex(index: bigint): CacheSet {
        // TODO assert index is within bounds
        return this.sets.get(Number(index));
    }


    read(raw: bigint): void {
        // TODO Address is shareable between caches with different parameters
        const address = bigintToAddress(this.parameters, raw);
        console.log(`Parsing address 0x${address.raw.toString(16)}`, address);
        console.log(`Reading address 0x${address.raw.toString(16)} in set ${address.index}`);

        const set = this.getSetFromIndex(address.index);
        assertNonFalsy(set, `Set not found for index ${address.index}`);

        const access = set.read(address);

        this.accessHistory[this.runner.getCurrentCycle()] = {
            cycle: this.runner.getCurrentCycle(),
            setIndex: address.index,
            setAccess: access,
        }
    }


    write(): void {

    }
}
