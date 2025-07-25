import { Slider, SliderSingleProps } from "antd";

export type NonDynamicSliderProps = SliderSingleProps;

export const NonDynamicSlider = ({
  value,
  min = 0,
  max = 100,
  onChange,
  ...rest
}: NonDynamicSliderProps) => {
  function internalOnChange(val: number) {
    onChange?.(val);
  }

  return (
    <Slider
      min={min}
      max={max}
      value={value}
      onChange={internalOnChange}
      {...rest}
    />
  );
};
