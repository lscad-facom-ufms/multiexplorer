import {Modal} from "antd";
import {ParameterVisualizer} from "../parameter-visualizer";
import {CacheParameters} from "../../cache/cache-parameters.ts";

type ParameterVisualizerModalProps = {
    parameters: CacheParameters;
    open: boolean;
    onClose: () => void;
}

export const ParameterVisualizerModal = ({parameters, open, onClose}: ParameterVisualizerModalProps) => {
    return (
        <>
            <Modal
                className="ant-fullscreen"
                title="Cache configuration visualizer"
                open={open}
                onOk={onClose}
                okText="Close"
                cancelButtonProps={{hidden: true}}
            >
                <div
                    className="relative w-full h-full overflow-auto bg-gray-50 rounded-lg shadow"
                >
                    <div className="absolute inset-0">
                        <div className="p-4">
                            <ParameterVisualizer parameters={parameters}/>
                        </div>
                    </div>
                </div>
            </Modal>
        </>
    );
}
