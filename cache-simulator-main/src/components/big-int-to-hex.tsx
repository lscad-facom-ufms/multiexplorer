import {FC} from "react";

type Props = {
    value: bigint;
}
export const BigIntToHex: FC<Props> = ({value}) => {
    return `0x${value.toString(16)}`;
}
