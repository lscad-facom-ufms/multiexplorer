import {CacheParameters} from "../cache/cache-parameters.ts";
import {formatCapacity} from "./number.ts";

const parameterAssociativity = (parameter: CacheParameters): string => {
    if (parameter.blocksPerSet === 1n) {
        return 'Directly Mapped';
    }

    if (parameter.sets === 1n) {
        return 'Fully Associative';
    }

    return `${parameter.blocksPerSet}-Way Set Associative`;
}

export const parameterToHumanReadable = (parameter: CacheParameters): string => {
    const capacityBits = parameter.sets * parameter.blocksPerSet * parameter.wordsPerBlock * parameter.wordSize;
    const capacity = formatCapacity(capacityBits);
    const associativity = parameterAssociativity(parameter);

    return `${capacity},  ${associativity}, ${parameter.policy}`;
}

export const parametersToHumanReadable = (parameters: CacheParameters[]): string => {
    const level = parameters.length;
    if (level === 1) {
        return parameterToHumanReadable(parameters[0]);
    }

    const capacity = parametersToCapacity(parameters);
    return `${level}-level cache (${formatCapacity(capacity, 2)} total)`;
}

export const parameterToCapacity = (parameter: CacheParameters): bigint => {
    return parameter.sets * parameter.blocksPerSet * parameter.wordsPerBlock * parameter.wordSize;
}

export const parametersToCapacity = (parameters: CacheParameters[]): bigint => {
    return parameters.reduce((acc, parameter) => acc + parameterToCapacity(parameter), 0n);
}
