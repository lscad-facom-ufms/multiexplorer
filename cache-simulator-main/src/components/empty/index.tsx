import {ArrowArcRight, ArrowsCounterClockwise, FastForward, Gear, Play} from "@phosphor-icons/react";

export const Empty = () => {
    return <>
        <div
            className="text-center text-gray-800 mb-12"
        >
            <svg
                className="w-32 h-32 mx-auto mb-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                />
            </svg>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Get Started with Memory Cache Simulation</h2>
            <p className="text-xl text-gray-600">Follow these steps to begin your simulation journey</p>
        </div>

        <div className="space-y-6">
            <div
                className="bg-white p-6 rounded-xl shadow-md lg transition-shadow duration-300"
            >
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 1: Configure Cache</h3>
                <p className="text-gray-600">Select or configure your cache parameters to begin the simulation.</p>
            </div>

            <div
                className="bg-white p-6 rounded-xl shadow-md transition-shadow duration-300"
            >
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 2: Select Program</h3>
                <p className="text-gray-600">Choose a pre-defined program or upload your own to run in the simulator.</p>
            </div>

            <div
                className="bg-white p-6 rounded-xl shadow-md transition-shadow duration-300"
            >
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Step 3: Control Simulation</h3>
                <div className="flex justify-around items-center mt-6">
                    {[
                        {icon: Gear, label: "Settings"},
                        {icon: ArrowsCounterClockwise, label: "Reset"},
                        {icon: FastForward, label: "Fast Forward"},
                        {icon: ArrowArcRight, label: "Step"},
                        {icon: Play, label: "Play/Pause"},
                    ].map((item, index) => (
                        <div
                            key={index}
                            className="flex flex-col items-center "
                        >
                            <div className="p-3 bg-gray-100 rounded-full duration-300">
                                <item.icon className="h-6 w-6"/>
                            </div>
                            <span className="text-sm text-gray-600 mt-2duration-300">{item.label}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    </>
}
