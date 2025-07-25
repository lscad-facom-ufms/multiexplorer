import {range} from "../../../helpers/number.ts";
import {BlockProps} from "../types.ts";

export const DetailedBlock = ({wordsPerBlock, blockIndex, setIndex}: BlockProps) => {
    return <>
        <li
            className="flex items-center justify-center w-8 h-6 bg-blue-100 border"
            title={`Valid bit`}
        >V
        </li>
        <li
            className="flex items-center justify-center px-2 h-6 bg-green-100 border"
            title={`Valid bit`}
        >
            Tag
        </li>
        {range(0, Number(wordsPerBlock)).map(wordIndex => (
            <li
                title={`Set ${setIndex} Block ${blockIndex} Word ${wordIndex}`}
                className="flex items-center justify-center px-2 h-6 bg-gray-100 border cursor-pointer aspect-square"
            />
        ))}
    </>
}
