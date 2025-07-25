import {SerializationType} from "../../contexts/settings.tsx";

export type SerializerProps = {
    value: bigint;
    serialization?: SerializationType;
    padStartLength?: number;
    padStart?: string;
}

type SerializationConfig = {
    radix: number;
    prefix?: string;
    suffix?: string;
}
const configs: Record<SerializationType, SerializationConfig> = {
    [SerializationType.HEXADECIMAL]: {radix: 16, prefix: '0x'},
    [SerializationType.DECIMAL]: {radix: 10},
    [SerializationType.BINARY]: {radix: 2, prefix: '0b'}
}

export const Serializer = ({
                               value,
                               padStartLength,
                               padStart,
                               serialization = SerializationType.HEXADECIMAL
                           }: SerializerProps) => {
    const config = configs[serialization];

    const serialized = value
        .toString(config.radix)
        .toUpperCase()
        .padStart(padStartLength ?? 0, padStart ?? ' ');
    const result = [config.prefix, serialized, config.suffix].join('');

    return <span className="font-mono">{result}</span>
}