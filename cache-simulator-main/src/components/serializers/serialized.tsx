import {Serializer, SerializerProps} from "./serializer.tsx";
import {useSettings} from "../../contexts/settings.tsx";

const SerializedAddress = ({serialization, ...rest}: SerializerProps) => {
    const {settings} = useSettings();

    return <Serializer serialization={serialization || settings.addressSerialization} {...rest}/>
}
const SerializedTag = ({serialization, ...rest}: SerializerProps) => {
    const {settings} = useSettings();

    return <Serializer serialization={serialization || settings.tagSerialization} {...rest} />
}
const SerializedIndex = ({serialization, ...rest}: SerializerProps) => {
    const {settings} = useSettings();

    return <Serializer serialization={serialization || settings.indexSerialization} {...rest}/>
}
const SerializedBlockOffset = ({serialization, ...rest}: SerializerProps) => {
    const {settings} = useSettings();

    return <Serializer serialization={serialization || settings.blockOffsetSerialization} {...rest}/>
}
const SerializedByteOffset = ({serialization, ...rest}: SerializerProps) => {
    const {settings} = useSettings();

    return <Serializer serialization={serialization || settings.byteOffsetSerialization} {...rest}/>
}

export const Serialized = {
    Address: SerializedAddress,
    Tag: SerializedTag,
    Index: SerializedIndex,
    BlockOffset: SerializedBlockOffset,
    ByteOffset: SerializedByteOffset,
}