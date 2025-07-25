import {CacheParameters} from "../../cache/cache-parameters.ts";
import {range} from "../../helpers/number.ts";
import {BlockProps} from "./types.ts";
import {SimpleBlock} from "./components/simple-block.tsx";
import {DetailedBlock} from "./components/detailed-block.tsx";

type ParameterVisualizerProps = {
    parameters: CacheParameters;
}

const detailed = true;

const Block = (props: BlockProps) => {
    return <ul className="flex">
        {detailed && <DetailedBlock {...props}/>}
        {!detailed && <SimpleBlock {...props}/>}
    </ul>
}

// TODO add DnD feature to reorder caches?
export const ParameterVisualizer = ({parameters}: ParameterVisualizerProps) => {
    return <table className="text-xs text-gray-800 whitespace-nowrap">
        <thead>
        <tr>
            <th></th>
            {range(0, Number(parameters.blocksPerSet)).map(blockIndex => (
                <th>Block {blockIndex}</th>
            ))}
        </tr>
        </thead>
        <tbody>
        {range(0, Number(parameters.sets)).map(setIndex => (
            <tr>
                <td>Set {setIndex}</td>
                {range(0, Number(parameters.blocksPerSet)).map(blockIndex => (
                    <td className="pl-2">
                        <Block
                            setIndex={setIndex}
                            blockIndex={blockIndex}
                            wordsPerBlock={Number(parameters.wordsPerBlock)}
                        />
                    </td>
                ))}
            </tr>
        ))}
        </tbody>
    </table>
}
