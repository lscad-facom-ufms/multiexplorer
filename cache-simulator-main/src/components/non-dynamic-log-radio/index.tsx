import { Radio, RadioProps } from "antd";
import { formatNumber, range } from "../../helpers/number.ts";
import { useMemo } from "react";

type NewDynamicLogRadioProps = {
  onChange: (value: number) => void;
  options?: number;
  min?: number;
  max?: number;
};

type NonDynamicLogRadioProps = NewDynamicLogRadioProps &
  Omit<RadioProps, "onChange">;

export const NonDynamicLogRadio = ({
  value,
  onChange,
  min = 0,
  max = 10,
  options = 2,
  ...rest
}: NonDynamicLogRadioProps) => {
  const logValue = Math.round(Math.log2(value));

  // Fixed range: from min to max
  const values = useMemo(() => range(min, max, true), [min, max]);

  const internalOnChange: RadioProps["onChange"] = (e) => {
    onChange?.(2 ** e.target.value);
  };

  return (
    <Radio.Group value={logValue} onChange={internalOnChange} {...rest}>
      {values.map((val) => (
        <Radio className="select-none" value={val} key={val}>
          {formatNumber(2 ** val)}
        </Radio>
      ))}
    </Radio.Group>
  );
};
