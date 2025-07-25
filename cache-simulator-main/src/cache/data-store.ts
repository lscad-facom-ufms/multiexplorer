// TODO remove any
export abstract class DataStore {
    abstract read(address: bigint): void;
    abstract write(address: bigint, value: bigint): void;
}
