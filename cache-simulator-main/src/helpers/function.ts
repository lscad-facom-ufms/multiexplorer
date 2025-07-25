export const noop = () => {
};

export const suppressLogs = <T>(enabled: boolean, fn: () => T): T => {
    if (enabled) {
        const original = console.log;
        console.log = noop;
        const ret = fn();
        console.log = original;

        return ret;
    } else {
        return fn();
    }
}
