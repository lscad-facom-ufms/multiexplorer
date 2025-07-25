import {expect, test} from "vitest";
import {bitExtract, bitMask} from "./address.ts";

test('bitmasks are correct', () => {
    expect(bitMask(1n, 0n)).toBe(0b1n)
    expect(bitMask(2n, 0n)).toBe(0b11n)
    expect(bitMask(1n, 1n)).toBe(0b10n)
    expect(bitMask(2n, 1n)).toBe(0b110n)
});

test('bitextracts are correct', () => {
    expect(bitExtract(0b1n, 1n, 0n)).toBe(0b1n)
    expect(bitExtract(0b11n, 2n, 0n)).toBe(0b11n)
    expect(bitExtract(0b110n, 2n, 1n)).toBe(0b11n)
    expect(bitExtract(0b1010n, 2n, 2n)).toBe(0b10n)
})
