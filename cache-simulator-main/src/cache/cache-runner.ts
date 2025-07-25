import {CacheParameters} from "./cache-parameters.ts";
import {CacheSimulator} from "./cache-simulator.ts";
import {Memory} from "./memory.ts";
import {DataStore} from "./data-store.ts";
import {range} from "../helpers/number.ts";
import {suppressLogs} from "../helpers/function.ts";

type RunnerOptions = {
    simulationLogs?: boolean;
}

export class CacheRunner {
    caches: CacheSimulator[] = [];

    lastSimulatedCycle = -1;
    underlying = new Memory();

    constructor(
        public readonly chainParameters: CacheParameters[],
        public readonly instructions: bigint[],
        public readonly options?: RunnerOptions,
    ) {
        const lastIndex = chainParameters.length - 1;
        for (let i = lastIndex; i >= 0; i--) {
            const underlying: DataStore = i === lastIndex ? this.underlying : this.caches[i + 1];
            this.caches[i] = new CacheSimulator(this, chainParameters[i], underlying);
            this.caches[i].setLevel(i + 1);
        }
    }

    getUnderlying() {
        return this.underlying;
    }

    getEntryCache() {
        return this.caches[0];
    }

    getLastHistoryFromLevel(levelIndex = 0) {
        const cache = this.caches[levelIndex];

        for (let cycle = this.lastSimulatedCycle; cycle >= 0; cycle--) {
            if (cache.getAccessForCycle(cycle)) {
                return cache.getAccessForCycle(cycle);
            }
        }
    }

    buildHistory(cacheIndex: number, count: number) {
        const from = Math.max(0, this.lastSimulatedCycle - count);
        const to = Math.max(0, this.lastSimulatedCycle);
        const cache = this.caches[cacheIndex];

        return range(from, to, true).map((cycle) => {
            return cache.getAccessForCycle(cycle);
        }).filter(Boolean);
    }

    getCurrentCycle() {
        return this.lastSimulatedCycle
    }

    step() {
        if (++this.lastSimulatedCycle >= this.instructions.length) {
            return;
        }

        const instruction = this.instructions[this.lastSimulatedCycle];

        const access = suppressLogs(!this.options?.simulationLogs, () => {
            return this.read(instruction);
        })

        return access;
    }

    run() {
        while (this.lastSimulatedCycle < this.instructions.length) {
            this.step();
        }
        this.lastSimulatedCycle--;
    }

    private read(address: bigint) {
        const entry = this.getEntryCache();

        return entry.read(address);
    }

    // @ts-expect-error - missing implementation
    private write(): void {
        // TODO
    }

    /** @deprecated */
    get hits() {
        return this.getEntryCache().hits;
    }

    /** @deprecated */
    get misses() {
        return this.getEntryCache().misses;
    }

    /** @deprecated */
    get reads() {
        return this.getEntryCache().reads;
    }

    /** @deprecated */
    get writes() {
        return this.getEntryCache().writes;
    }

    /** @deprecated */
    get sets() {
        return this.getEntryCache().sets;
    }


    /** @deprecated */
    get parameters() {
        return this.getEntryCache().parameters;
    }

}
