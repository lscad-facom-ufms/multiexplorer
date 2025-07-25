export const range = (from: number, to?: number) => {
    if (to === undefined) {
        to = from;
        from = 0;
    }

    return Array(to - from).fill(0);
}

export const interleaveMap = <T, R>(
    array: T[],
    mapper: (element: T, index: number) => R,
    separator: (element: T, index: number) => R,
) => {
    return array.flatMap((element, index) => {
        if (index === 0) {
            return [mapper(element, index)];
        }

        return [
            separator(element, index),
            mapper(element, index),
        ];
    });
}
