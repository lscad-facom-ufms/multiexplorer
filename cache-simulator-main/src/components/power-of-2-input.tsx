import {FC, useEffect, useRef, useState} from "react";
import {InputNumber} from "antd";

type Props = {
    value: number;
    onChange: (value: number | null) => void;
}

export const PowerOf2Input: FC<Props> = ({value, onChange}) => {
    const isTyping = useRef(false);
    const [internalValue, setInternalValue] = useState<number | null>(value);

    useEffect(() => {
        setInternalValue(value);
    }, [value]);

    function closestPowerOf2(newValue: number) {
        const log2 = Math.log2(newValue);
        const rounded = Math.round(log2);
        return 2 ** rounded;
    }

    function nextPowerOf2(newValue: number) {
        if (newValue < 1) {
            return 1;
        }

        if (newValue < value && value > 1) {
            return value / 2;
        }

        if (newValue > value) {
            return value * 2;
        }

        return value
    }

    function handleOnChange(newValue: number | null) {
        if (!newValue) {
            return void onChange(null);
        }

        if (!isTyping.current) {
            onChange(nextPowerOf2(newValue));
        } else {
            setInternalValue(newValue);
        }
    }

    function handleBlur() {
        isTyping.current = false;
        const newValue = closestPowerOf2(internalValue ?? 1);
        onChange(newValue);
        setInternalValue(newValue)
    }

    return <InputNumber
        value={internalValue}
        onChange={handleOnChange}
        onKeyDown={() => isTyping.current = true}
        onKeyUp={() => isTyping.current = false}
        onBlur={handleBlur}
    />
}
