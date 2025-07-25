import {Slider, SliderSingleProps} from "antd";
import {useState} from "react";

export type DynamicSliderProps = SliderSingleProps;

// TODO add flag for not log2
export const DynamicSlider = ({value, max, onChange, ...rest}: DynamicSliderProps) => {
    const [internalMax, setInternalMax] = useState(max);

    function internalOnChange(value: number) {
        onChange?.(value);
    }

    function internalOnChangeComplete(value: number) {
        if (value === internalMax) {
            setInternalMax(internalMax + value);
        }
    }

    return <Slider
        max={internalMax}
        included
        value={value ?? 0}
        onChangeComplete={internalOnChangeComplete}
        onChange={internalOnChange}
        {...rest}
    />
}
