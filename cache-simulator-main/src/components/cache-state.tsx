import {useState} from 'react'
import {Check, ChevronDown, ChevronRight, X} from "lucide-react"
import {CacheSimulator} from "../cache/cache-simulator.ts";
import {blockAddressRange} from "../helpers/address.ts";
import {interleaveMap} from "../helpers/array.ts";
import {clsx} from "clsx";
import {Serialized} from "./serializers/serialized.tsx";

export type CacheStatusProps = {
    cache: CacheSimulator;
    highlight?: {
        hit: boolean,
        setIndex: bigint;
        blockIndex: number;
    };
}
export default function CacheState({cache, highlight}: CacheStatusProps) {
    const [collapsedSets, setCollapsedSets] = useState<number[]>([])

    const toggleSet = (setIndex: number) => {
        setCollapsedSets(prev =>
            prev.includes(setIndex)
                ? prev.filter(i => i !== setIndex)
                : [...prev, setIndex],
        )
    }

    return (
        <div className="space-y-2">
            {cache.sets.mapInitialized((set, setIndex) => (
                <div
                    key={String(setIndex)}
                    className={clsx('rounded-lg shadow-sm border border-gray-200 overflow-hidden', {
                        'bg-white': highlight?.setIndex !== BigInt(setIndex),
                        'border-2 border-red-500': !highlight?.hit && highlight?.setIndex === BigInt(setIndex),
                        'border-2 border-green-500': highlight?.hit && highlight?.setIndex === BigInt(setIndex),
                    })}
                >
                    <div
                        className="px-4 py-2 flex justify-between items-center cursor-pointer hover:bg-gray-50"
                        onClick={() => toggleSet(setIndex)}
                    >
                        <h2 className="text-sm font-medium text-gray-800">Set {setIndex}</h2>
                        {collapsedSets.includes(setIndex) ?
                            <ChevronDown className="w-4 h-4 text-gray-500"/>
                            :
                            <ChevronRight className="w-4 h-4 text-gray-500"/>
                        }
                    </div>
                    {!collapsedSets.includes(setIndex) && (
                        <div>
                            <table className="w-full text-xs">
                                <thead>
                                <tr className="bg-gray-50">
                                    <th className="px-3 py-2 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Block</th>
                                    <th className="px-3 py-2 text-center text-sm font-medium text-gray-500 uppercase tracking-wider">Valid</th>
                                    <th className="px-3 py-2 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Tag</th>
                                    <th className="px-3 py-2 text-left text-sm font-medium text-gray-500 uppercase tracking-wider">Memory
                                        Range
                                    </th>
                                    <th className="px-3 py-2 text-right text-sm font-medium text-gray-500 uppercase tracking-wider">Load</th>
                                    <th className="px-3 py-2 text-right text-sm font-medium text-gray-500 uppercase tracking-wider">Last
                                        Access
                                    </th>
                                </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                {set.blocks.mapInitialized((block, blockIndex) => (
                                    <tr
                                        key={blockIndex}
                                        className={clsx({
                                            'bg-red-100': !highlight?.hit && highlight?.blockIndex === blockIndex && setIndex === Number(highlight.setIndex),
                                            'bg-green-100': highlight?.hit && highlight?.blockIndex === blockIndex && setIndex === Number(highlight.setIndex),
                                        })}
                                    >
                                        <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">
                                            #{blockIndex}
                                        </td>
                                        <td className="px-3 py-2 whitespace-nowrap text-center">
                                            {block.valid ? (
                                                <Check
                                                    className="text-green-500 inline"
                                                    size={20}
                                                />
                                            ) : (
                                                <X
                                                    className="text-red-500 inline"
                                                    size={20}
                                                />
                                            )}
                                        </td>
                                        <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">
                                            <Serialized.Tag value={block.tag}/>
                                        </td>
                                        <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">
                                            {
                                                interleaveMap(
                                                    blockAddressRange(cache.parameters, set, block),
                                                    (address, index) => <Serialized.Address
                                                        key={[address, index].join('-')}
                                                        value={address}
                                                    />,
                                                    (address, index) => <span key={[address, index, 'label'].join('-')}> - </span>,
                                                )
                                            }
                                        </td>
                                        <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900 text-right">
                                            Cycle {String(block.loadedAt)}
                                        </td>
                                        <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900 text-right">
                                            Cycle {String(block.lastAccessedAt)}
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            ))}
        </div>
    )
}
