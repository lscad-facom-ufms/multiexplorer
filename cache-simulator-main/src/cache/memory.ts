import {DataStore} from "./data-store.ts";

export class Memory implements DataStore {
    data = new Map<bigint, bigint>();

    readCount = 0;
    writeCount = 0;

    read(raw: bigint): bigint {
        this.readCount++;

        return this.data.get(raw) || BigInt(0);
    }

    write(raw: bigint, value: bigint): void {
        this.writeCount++;

        this.data.set(raw, value);
    }
}
