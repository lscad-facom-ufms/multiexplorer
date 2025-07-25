import {BlockProps} from "../types.ts";

export const SimpleBlock = ({wordsPerBlock, blockIndex, setIndex}: BlockProps) => {
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
        <li
            title={`Set ${setIndex} Block ${blockIndex} Words 0-${wordsPerBlock - 1}`}
            className="flex w-32 items-center justify-center px-2 h-6 bg-gray-100 border cursor-pointer aspect-square"
        >
            {wordsPerBlock > 1 ? `${wordsPerBlock} words` : '1 word'}
        </li>
    </>
}
