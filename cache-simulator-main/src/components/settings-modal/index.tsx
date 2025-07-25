import {Button, Form, Modal, Select, SelectProps} from "antd";
import {InfoIcon} from "lucide-react";
import {SerializationType, useSettings} from "../../contexts/settings.tsx";
import {formatTimeFromNs} from "../../helpers/number.ts";
import {DynamicSlider} from "../dynamic-slider";

export type SettingsModalProps = {
    open: boolean;
    onClose: () => void;
}

const serializationOptions: SelectProps['options'] = [{
    label: 'Binary',
    value: SerializationType.BINARY,
}, {
    label: 'Decimal',
    value: SerializationType.DECIMAL,
}, {
    label: 'Hexadecimal',
    value: SerializationType.HEXADECIMAL
}]

export const SettingsModal = ({open, onClose}: SettingsModalProps) => {
    const {settings, setSetting, resetSettings} = useSettings();

    const [form] = Form.useForm();

    function handleResetSettings() {
        resetSettings();
    }

    return <>
        <Modal
            title="Settings modal"
            open={open}
            onCancel={onClose}
            cancelButtonProps={{hidden: true}}
            okButtonProps={{hidden: true}}
            maskClosable={false}
        >
            <Form
                form={form}
                layout="vertical"
                onValuesChange={console.log}
            >
                <Form.Item
                    label="Console simulation logs"
                    help="Simulation generates huge amounts of logs and may slow down the browser. Disable for better performance."
                >
                    <Select
                        value={String(settings.simulationLogs)}
                            onChange={value => {
                            setSetting('simulationLogs', value === 'true');
                        }}
                        options={[
                            {
                                value: 'true', label: "Enabled",
                            }, {
                                value: 'false', label: "Disabled",
                            },
                        ]}
                    />
                </Form.Item>
                <Form.Item
                    label={`Auto-stepper interval: ${formatTimeFromNs(Number(settings.autoStepperIntervalMs) * 1_000_000, 0)}`}
                >
                    <DynamicSlider
                        min={1}
                        max={1_000}
                        value={Number(settings.autoStepperIntervalMs)}
                        onChange={value => {
                            setSetting('autoStepperIntervalMs', value);
                        }}
                        defaultValue={Number(settings.autoStepperIntervalMs)}
                        tooltip={{open: false}}
                    />
                </Form.Item>
                <Form.Item
                    label="Address serialization"
                    help="How addresses are serialized in the entire application"
                >
                    <Select
                        value={settings.addressSerialization}
                        onChange={value => {
                            setSetting('addressSerialization', value as SerializationType);
                        }}
                        options={serializationOptions}
                    />
                </Form.Item>
                <Form.Item
                    label="Tag serialization"
                    help="How tags are serialized in the entire application"
                >
                    <Select
                        value={settings.tagSerialization}
                        onChange={value => {
                            setSetting('tagSerialization', value as SerializationType);
                        }}
                        options={serializationOptions}
                    />
                </Form.Item>
                <Form.Item
                    label="Set index serialization"
                    help="How indices are serialized in the entire application"
                >
                    <Select
                        value={settings.indexSerialization}
                        onChange={value => {
                            setSetting('indexSerialization', value as SerializationType);
                        }}
                        options={serializationOptions}
                    />
                </Form.Item>
                <Form.Item
                    label="Block offset serialization"
                    help="How block offsets are serialized in the entire application"
                >
                    <Select
                        value={settings.blockOffsetSerialization}
                        onChange={value => {
                            setSetting('blockOffsetSerialization', value as SerializationType);
                        }}
                        options={serializationOptions}
                    />
                </Form.Item>
                <Form.Item
                    label="Byte offset serialization"
                    help="How byte offsets are serialized in the entire application"
                >
                    <Select
                        value={settings.byteOffsetSerialization}
                        onChange={value => {
                            setSetting('byteOffsetSerialization', value as SerializationType);
                        }}
                        options={serializationOptions}
                    />
                </Form.Item>
                {/*<Form.Item*/}
                {/*    label="Option 1"*/}
                {/*>*/}
                {/*    <Select*/}
                {/*        defaultValue="opt1"*/}
                {/*        onChange={console.log}*/}
                {/*        options={[*/}
                {/*            {*/}
                {/*                value: 'opt1', label: "Option 1",*/}
                {/*            }, {*/}
                {/*                value: 'opt2', label: "Option 2",*/}
                {/*            }, {*/}
                {/*                value: 'opt3', label: "Option 3",*/}
                {/*            },*/}
                {/*        ]}*/}
                {/*    />*/}
                {/*</Form.Item>*/}
                {/*<Form.Item*/}
                {/*    label={`Auto-stepper interval: ${formatTimeFromNs(Number(stepperInterval))}`}*/}
                {/*>*/}
                {/*    <DynamicLogSlider*/}
                {/*        // TODO not BigInt conversion*/}
                {/*        max={10}*/}
                {/*        value={Number(stepperInterval)}*/}
                {/*        onChange={value => {*/}
                {/*            setStepperInterval(value);*/}
                {/*        }}*/}
                {/*        defaultValue={30}*/}
                {/*        tooltip={{open: false}}*/}
                {/*    />*/}

                {/*</Form.Item>*/}
                {/*<Form.Item*/}
                {/*    label="Address serialization format"*/}
                {/*>*/}
                {/*    <Select*/}
                {/*        defaultValue="hex"*/}
                {/*        onChange={console.log}*/}
                {/*        options={[*/}
                {/*            {*/}
                {/*                value: 'hex', label: "Hexadecimal",*/}
                {/*            }, {*/}
                {/*                value: 'octal', label: "Octal",*/}
                {/*            }, {*/}
                {/*                value: 'decimal', label: "Decimal",*/}
                {/*            }, {*/}
                {/*                value: 'binary', label: "Binary",*/}
                {/*            },*/}
                {/*        ]}*/}
                {/*    />*/}
                {/*</Form.Item>*/}
            </Form>

            <div className="flex gap-2 px-4 py-4 bg-gray-100 rounded-lg">
                <InfoIcon/>
                <p>
                    <span>Need help generating new memory access logs? </span>
                    <a
                        className="underline text-blue-500"
                        target="_blank"
                        href="https://github.com/HugoJF/tracergrind-docker"
                    >Learn more about log generation</a>
                </p>
            </div>

            <Button onClick={handleResetSettings} className="w-full my-2">Reset settings to default</Button>
        </Modal>
    </>
}
