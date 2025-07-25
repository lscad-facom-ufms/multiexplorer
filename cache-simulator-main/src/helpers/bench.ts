export const time = (fn: () => void): number => {
    const start = Date.now();
    fn();
    return Date.now() - start;
}
