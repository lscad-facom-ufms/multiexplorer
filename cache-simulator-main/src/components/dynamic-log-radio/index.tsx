import {Radio, RadioProps} from "antd";
import {formatNumber, range} from "../../helpers/number.ts";
import {useEffect, useState} from "react";

type NewDynamicLogRadioProps = {
    onChange: (value: number) => void;
    options?: number;
    min?: number;
    max?: number;
}

type DynamicLogRadioProps = NewDynamicLogRadioProps & Omit<RadioProps, 'onChange'>;

export const DynamicLogRadio = ({
    value,
    onChange,
    min = -Number.MAX_SAFE_INTEGER,
    max = Number.MAX_SAFE_INTEGER,
    options = 2,
    ...rest
}: DynamicLogRadioProps) => {
    const logValue = Math.round(Math.log2(value));

    const [lowerRange, setLowerRange] = useState(getLowerRange(logValue));
    const [upperRange, setUpperRange] = useState(getUpperRange(logValue));

    const values = range(lowerRange, upperRange, true);

    // TODO: avoid having to use this
    useEffect(() => {
        if (logValue > lowerRange && logValue < upperRange) {
            return;
        }

        setLowerRange(getLowerRange(logValue));
        setUpperRange(getUpperRange(logValue));
    }, [value, lowerRange, upperRange]);

    function getLowerRange(currentValue: number) {
        return Math.max(min, currentValue - options);
    }

    function getUpperRange(currentValue: number) {
        const extraUpper = Math.max(0, getLowerRange(currentValue) - (currentValue - options));

        return Math.min(max, currentValue + options + extraUpper);
    }

    const internalOnChange: RadioProps['onChange'] = (e) => {
        const value = e.target.value;

        onChange?.(2 ** e.target.value);
        if (value === lowerRange || value === upperRange) {
            setLowerRange(getLowerRange(value));
            setUpperRange(getUpperRange(value));
        }
    }

    return <Radio.Group
        value={logValue}
        onChange={internalOnChange}
        {...rest}
    >
        {values.map(value => <Radio
            className="select-none"
            value={value}
        >
            {formatNumber(2 ** value)}
        </Radio>)}
    </Radio.Group>
}
