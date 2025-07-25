import {CacheSetAccess} from "./cache-set-access.ts";

export interface CacheAccess {
    readonly cycle: number,
    readonly setIndex: bigint,
    readonly setAccess: CacheSetAccess,
}
