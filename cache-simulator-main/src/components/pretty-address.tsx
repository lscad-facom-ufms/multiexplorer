import {FC} from "react";
import {bigintToAddress} from "../helpers/address.ts";
import {CacheParameters} from "../cache/cache-parameters.ts";
import {log2n} from "../helpers/bigint.ts";
import {ADDRESS_SIZE} from "../constants/arch.ts";

type Props = {
    value: bigint;
    parameters: CacheParameters;
}
export const PrettyAddress: FC<Props> = ({value, parameters}) => {
    const address = bigintToAddress(parameters, value);

    const tagSize = Number(ADDRESS_SIZE - log2n(parameters.wordsPerBlock) - log2n(parameters.sets));
    const indexSize = Number(log2n(parameters.sets));
    const offsetSize = Number(log2n(parameters.wordsPerBlock));

    function getTitle(label: string, value: bigint) {
        return `${label} = Hex: 0x${value.toString(16)} | Decimal: ${value} | Binary: ${value.toString(2)}b`;
    }

    return <p className="flex gap-1">
        <span title={getTitle('Tag', address.tag)}>
            {address.tag.toString(2).padStart(tagSize, '0')}
        </span>
        <span title={getTitle('Index', address.index)}>
            {address.index.toString(2).padStart(indexSize, '0')}
        </span>
        <span title={getTitle('Block Offset', address.blockOffset)}>
            {address.blockOffset.toString(2).padStart(offsetSize, '0')}
        </span>
        <span title={getTitle('Block Offset', address.blockOffset)}>
            {address.byteOffset.toString(2).padStart(offsetSize, '0')}
        </span>
    </p>;
}
