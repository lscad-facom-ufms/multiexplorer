import {expect, test} from "vitest";
import {CacheSimulator} from "./cache-simulator.ts";
import {CacheParameters} from "./cache-parameters.ts";
import {Memory} from "./memory.ts";
import {bigintToAddress} from "../helpers/address.ts";
import {range} from "../helpers/array.ts";

test('cache register first access as miss', () => {
    const memory = new Memory();
    const parameters = new CacheParameters(4n, 1n, 1n, 64n, 'LRU');
    const cache = new CacheSimulator(parameters, memory)

    cache.read(bigintToAddress(parameters, 1n));

    expect(cache.hits).toBe(0n)
    expect(cache.misses).toBe(1n)
    expect(cache.reads).toBe(1n)
    expect(cache.writes).toBe(0n)
})
test('cache register second access as hit', () => {
    const memory = new Memory();
    const parameters = new CacheParameters(4n, 1n, 1n, 64n, 'LRU');
    const cache = new CacheSimulator(parameters, memory)

    cache.read(bigintToAddress(parameters, 1n));
    cache.read(bigintToAddress(parameters, 1n));

    expect(cache.hits).toBe(1n)
    expect(cache.misses).toBe(1n)
    expect(cache.reads).toBe(2n)
    expect(cache.writes).toBe(0n)
})
test('cache reads underlying data properly', () => {
    const address = 10n;
    const data = 123n;

    const parameters = new CacheParameters(4n, 1n, 1n, 64n, 'LRU');
    const memory = new Memory();
    memory.write(bigintToAddress(parameters, address), data);
    const cache = new CacheSimulator(parameters, memory)

    const readData = cache.read(bigintToAddress(parameters, address));

    expect(readData.data).toBe(data)

    expect(cache.hits).toBe(0n)
    expect(cache.misses).toBe(1n)
    expect(cache.reads).toBe(1n)
    expect(cache.writes).toBe(0n)
})
test('associative cache will is able to handle index collisions', () => {
    const parameters = new CacheParameters(4n, 4n, 1n, 64n, 'LRU');

    const address1 = bigintToAddress(parameters, 0b000_11n);
    const address2 = bigintToAddress(parameters, 0b001_11n);
    const address3 = bigintToAddress(parameters, 0b010_11n);
    const address4 = bigintToAddress(parameters, 0b011_11n);
    const data = 123n;

    const memory = new Memory();
    memory.write(address1, data);
    memory.write(address2, data);
    memory.write(address3, data);
    memory.write(address4, data);
    const cache = new CacheSimulator(parameters, memory)

    range(2).forEach(() => {
        cache.read(address1);
        cache.read(address2);
        cache.read(address3);
        cache.read(address4);
    })
    cache.read(bigintToAddress(parameters, 0b111_11n))

    expect(cache.hits).toBe(4n)
    expect(cache.misses).toBe(5n)
    expect(cache.reads).toBe(9n)
    expect(cache.writes).toBe(0n)
})
test('associative cache will LRU place block', () => {
    const parameters = new CacheParameters(4n, 4n, 1n, 64n, 'LRU');

    const address1 = bigintToAddress(parameters, 0b000_11n);
    const address2 = bigintToAddress(parameters, 0b001_11n);
    const address3 = bigintToAddress(parameters, 0b010_11n);
    const address4 = bigintToAddress(parameters, 0b011_11n);
    const newAddress = bigintToAddress(parameters, 0b111_11n);
    const data = 123n;

    const memory = new Memory();
    memory.write(address1, data);
    memory.write(address2, data);
    memory.write(address3, data);
    memory.write(address4, data);
    const cache = new CacheSimulator(parameters, memory)

    range(2).forEach(() => {
        cache.read(address4);
        cache.read(address3);
        cache.read(address2);
        cache.read(address1);
    })
    const cacheAccess = cache.read(newAddress)

    expect(cacheAccess.setAccess.replacedTag).toBe(0b11n)
})

test('associative cache will FIFO place block', () => {
    const parameters = new CacheParameters(4n, 4n, 1n, 64n, 'FIFO');

    const address1 = bigintToAddress(parameters, 0b000_11n);
    const address2 = bigintToAddress(parameters, 0b001_11n);
    const address3 = bigintToAddress(parameters, 0b010_11n);
    const address4 = bigintToAddress(parameters, 0b011_11n);
    const newAddress = bigintToAddress(parameters, 0b100_11n);
    const data = 123n;

    const memory = new Memory();
    memory.write(address1, data);
    memory.write(address2, data);
    memory.write(address3, data);
    memory.write(address4, data);
    const cache = new CacheSimulator(parameters, memory)

    cache.read(address1);
    cache.read(address2);
    cache.read(address3);
    cache.read(address4);
    range(2).forEach(() => {
        cache.read(address4);
        cache.read(address3);
        cache.read(address2);
        cache.read(address1);
    })
    const cacheAccess = cache.read(newAddress)

    expect(cacheAccess.setAccess.replacedTag).toBe(0b00n)
})
