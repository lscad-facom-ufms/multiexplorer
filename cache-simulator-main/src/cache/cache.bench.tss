import {bench, describe} from "vitest";
import {CacheSimulator} from "./cache-simulator.ts";
import {CacheParameters} from "./cache-parameters.ts";
import {Memory} from "./memory.ts";
import {bigintToAddress} from "../helpers/address.ts";

describe('cache runtime performance', () => {
    const parameters = new CacheParameters(4n, 4n, 1n, 64n, 'LRU');

    const address1 = bigintToAddress(parameters, 0b000_11n);
    const address2 = bigintToAddress(parameters, 0b001_11n);
    const address3 = bigintToAddress(parameters, 0b010_11n);
    const address4 = bigintToAddress(parameters, 0b011_11n);

    const memory = new Memory();
    const data = 123n;
    memory.write(address1, data);
    memory.write(address2, data);
    memory.write(address3, data);
    memory.write(address4, data);

    const cache = new CacheSimulator(parameters, memory)

    console.log = () => false;

    bench("memory reads", () => {
        cache.read(address1);
    }, {time: 2_000, warmupTime: 500})
});

describe('cache initialization performance', () => {
    const memory = new Memory();

    bench("cache initialization", () => {
        const parameters = new CacheParameters(4096n, 128n, 128n, 64n, 'LRU');
        new CacheSimulator(parameters, memory)
    }, {warmupIterations: 3, iterations: 5})
});
