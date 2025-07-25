import {bench, describe} from "vitest";
import {range} from "./array.ts";

describe.only('ways to initialize 0 arrays', () => {
    bench("range()", () => {
        range(1_000_000).map(() => 0);
    })

    bench("new Array()", () => {
        new Array(1_000_000).fill(0);
    })

    bench("new Array() + for", () => {
        const arr = new Array(1_000_000);
        for (let i = 0; i < arr.length; i++) {
            arr[i] = 0;
        }
    })

    bench("Array.from", () => {
        Array.from({length: 1_000_000}, () => 0);
    });

    bench("new Array() with no fill", () => {
        new Array(1_000_000);
    });

    bench("empty array + push", () => {
        const arr = [];
        for (let i = 0; i < 1_000_000; i++) {
            arr.push(0);
        }
    });
});


describe.only('ways to initialize object arrays', () => {
    bench("range()", () => {
        range(1_000_000).map(() => ({}));
    })

    bench("new Array() + for", () => {
        const arr = new Array(1_000_000);
        for (let i = 0; i < arr.length; i++) {
            arr[i] = {};
        }
    })

    bench("Array.from", () => {
        Array.from({length: 1_000_000}, () => ({}));
    });

    bench("empty array + push", () => {
        const arr = [];
        for (let i = 0; i < 1_000_000; i++) {
            arr.push({});
        }
    });
})
