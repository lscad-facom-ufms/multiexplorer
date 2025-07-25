import {Address} from "./address.ts";
import {CacheSimulator} from "./cache-simulator.ts";
import {CacheBlock} from "./cache-block.ts";
import {CacheSetAccess, ReplacementReason} from "./cache-set-access.ts";
import {LazyArray} from "../lazy/array.ts";
import {assertNonFalsy} from "../helpers/assertions.ts";

export class CacheSet {
    blocks: LazyArray<CacheBlock>;

    accessHistory: Record<number, CacheSetAccess> = {};

    constructor(
        private readonly cache: CacheSimulator,
        public readonly index: number,
    ) {
        this.blocks = new LazyArray(
            Number(this.cache.parameters.blocksPerSet),
            (index) => new CacheBlock(cache, index),
        )
    }

    read(address: Address): CacheSetAccess {
        console.log(`Reading address 0x${address.raw.toString(16)} tags available: ${this.blocks.mapInitialized(block => block.getTag())}`);
        const block = this.findBlockFromTag(address);

        if (!block) {
            console.log(`Block not found for address 0x${address.raw.toString(16)}`)
            const [replacement, reason] = this.getReplacementBlock();
            // TODO assert
            if (!replacement) {
                throw new Error("No replacement block found");
            }
            const replacedTag = replacement.getTag();
            const replacedIndex = replacement.getIndex();
            const access = replacement.read(address);

            const cycle = this.cache.runner.getCurrentCycle();
            this.accessHistory[cycle] = {
                replacementReason: reason,
                replacedTag: replacedTag,
                replacedIndex: replacedIndex,
                tagsAvailable: this.blocks.mapInitialized(block => block.getTag()),
                address: address,
                blockAccess: access,
            }

            return this.accessHistory[cycle];
        }

        console.log(`Block found for address 0x${address.raw.toString(16)}`)
        const access = block.read(address);
        this.accessHistory[this.cache.runner.getCurrentCycle()] = {
            replacementReason: null,
            replacedTag: null,
            replacedIndex: block.getIndex(),
            tagsAvailable: this.blocks.mapInitialized(block => block.getTag()),
            address: address,
            blockAccess: access,
        }

        return this.accessHistory[this.cache.runner.getCurrentCycle()];
    }

    write(address: Address, data: bigint) {
        const block = this.findBlockFromTag(address);

        // TODO figure out what happens here

        return block!.write(address, data);
    }

    private getReplacementBlock(): [CacheBlock, ReplacementReason] {
        const uninitializedBlock = this.blocks.findUninitialized();
        if (uninitializedBlock) {
            return [uninitializedBlock, ReplacementReason.Uninitialized];
        }

        const invalidBlock = this.blocks.findInitialized(block => !block.valid);
        if (invalidBlock) {
            return [invalidBlock, ReplacementReason.Invalid];
        }

        if (this.cache.parameters.policy.toUpperCase() === 'LRU') {
            // TODO why undefined is returned?
            return [this.getLruReplacementBlock() as CacheBlock, ReplacementReason.Lru];
        }

        if (this.cache.parameters.policy.toUpperCase() === 'FIFO') {
            // TODO why undefined is returned?
            return [this.getFifoReplacementBlock() as CacheBlock, ReplacementReason.Fifo];
        }

        console.warn('Unknown replacement policy, falling back to random');
        const replacement = this.blocks.get(
            Math.floor(Math.random() * this.blocks.length),
        );
        assertNonFalsy(replacement, "Somehow we found a non-initialized block");
        return [replacement as CacheBlock, ReplacementReason.Unknown]; // TODO type-guard
    }

    private getLruReplacementBlock() {
        // TODO bigint -> Number conversion
        const accessTimes = this.blocks.mapInitialized(block => block.lastAccessedAt).map(Number);
        const minAccessTime = Math.min(...accessTimes);

        return this.blocks.findInitialized(block => Number(block.lastAccessedAt) === minAccessTime);
    }

    private getFifoReplacementBlock() {
        // TODO bigint -> Number conversion
        const loadTimes = this.blocks.mapInitialized(block => block.loadedAt).map(Number);
        const minLoadTime = Math.min(...loadTimes);

        return this.blocks.findInitialized(block => Number(block.loadedAt) === minLoadTime);
    }

    private findBlockFromTag(address: Address) {
        const block = this.blocks.findInitialized(block => (
            block.valid && block.getTag() === address.tag
        ));

        if (!block) {
            return undefined;
        }

        return block;
    }
}
