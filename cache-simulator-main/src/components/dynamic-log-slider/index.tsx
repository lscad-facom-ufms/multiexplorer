import {Slider, SliderSingleProps} from "antd";
import {useState} from "react";

export type DynamicSliderProps = SliderSingleProps;

const MAX_VALUE = 90; // 1024 Yotta

// TODO add flag for not log2
export const DynamicLogSlider = ({value, max, onChange, ...rest}: DynamicSliderProps) => {
    const [internalMax, setInternalMax] = useState(max);

    function internalOnChange(value: number) {
        onChange?.(2 ** value);
        console.log(value)
    }

    function internalOnChangeComplete(value: number) {
        if (value === internalMax) {
            setInternalMax(Math.min(MAX_VALUE, internalMax + 5));
        }
    }

    return <Slider
        max={internalMax}
        included
        value={Math.log2(value ?? 0)}
        onChangeComplete={internalOnChangeComplete}
        onChange={internalOnChange}
        {...rest}
    />
}
