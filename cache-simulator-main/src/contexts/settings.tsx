import {createContext, FC, PropsWithChildren, useContext, useEffect, useState} from "react";

export enum SerializationType {
    BINARY = 'BINARY',
    DECIMAL = 'DECIMAL',
    HEXADECIMAL = 'HEXADECIMAL',
}

export type Settings = {
    autoStepperIntervalMs: number;
    simulationLogs: boolean;
    addressSerialization: SerializationType;
    tagSerialization: SerializationType;
    indexSerialization: SerializationType;
    blockOffsetSerialization: SerializationType;
    byteOffsetSerialization: SerializationType;
}

export type SettingsContextType = {
    settings: Settings;
    setSetting: <T extends keyof Settings>(setting: T, value: Settings[T]) => void;
    resetSettings: () => void;
}

const initialSettings: Settings = {
    autoStepperIntervalMs: 500,
    simulationLogs: true,
    addressSerialization: SerializationType.HEXADECIMAL,
    tagSerialization: SerializationType.HEXADECIMAL,
    indexSerialization: SerializationType.DECIMAL,
    blockOffsetSerialization: SerializationType.HEXADECIMAL,
    byteOffsetSerialization: SerializationType.HEXADECIMAL

}
export const SettingsContext = createContext<SettingsContextType>({} as SettingsContextType);
export const useSettings = () => useContext(SettingsContext);

export const useSetting = <T extends keyof Settings>(setting: T) => {
    const {settings, setSetting} = useSettings();

    return [settings[setting], (value: Settings[T]) => setSetting(setting, value)] as const;
}

// TODO figure out a proper way to handle new properties or wipe localStorage on new version
export const SettingsProvider: FC<PropsWithChildren> = ({children}) => {
    const [settings, setSettings] = useState<Settings>(() => {
        const stored = localStorage.getItem('settings');
        if (stored) {
            return JSON.parse(stored);
        }
        return initialSettings
    });

    useEffect(() => {
        localStorage.setItem('settings', JSON.stringify(settings));
    }, [settings]);

    const setSetting = <T extends keyof Settings>(setting: T, value: Settings[T]) => {
        setSettings(s => ({
                ...s,
                [setting]: value,
            }
        ));
    };

    const resetSettings = () => {
        setSettings(initialSettings);
    }

    return <SettingsContext.Provider value={{settings, setSetting, resetSettings}}>
        {children}
    </SettingsContext.Provider>
};
