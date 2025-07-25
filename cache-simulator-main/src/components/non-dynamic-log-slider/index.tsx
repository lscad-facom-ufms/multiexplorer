import { Slider, SliderSingleProps } from "antd";

export type NonDynamicSliderProps = SliderSingleProps;

export const NonDynamicLogSlider = ({
  value,
  max,
  onChange,
  ...rest
}: NonDynamicSliderProps) => {
  function internalOnChange(value: number) {
    onChange?.(2 ** value);
    console.log(value);
  }

  return (
    <Slider
      max={max}
      included
      value={Math.log2(value ?? 0)}
      onChange={internalOnChange}
      {...rest}
    />
  );
};
