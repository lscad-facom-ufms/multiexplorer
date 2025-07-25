// TODO: type-guard it
export const assertNonFalsy = (value: any, message: string) => {
    if (!value) {
        throw new Error(message || `Expected non-falsy value, got ${value}`);
    }
}
