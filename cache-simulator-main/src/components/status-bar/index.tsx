import { clsx } from "clsx";
import { BigNumber } from "../big-number.tsx";
import { formatPercentage, formatTimeFromNs } from "../../helpers/number.ts";
import { CacheAccess } from "../../cache/cache-access.ts";
import { Serialized } from "../serializers/serialized.tsx";
import { CacheRunner } from "../../cache/cache-runner.ts";

export type StatusBarProps = {
  runner: CacheRunner;
  cacheIndex: number;
  history: CacheAccess;
  cycle: number;
  instructions: bigint[];
};
export const StatusBar = ({
  runner,
  cacheIndex,
  history,
  cycle,
}: StatusBarProps) => {
  const caches = runner.caches;
  const cache = caches[cacheIndex];

  const hitRate = Number(cache.hits) / Number(cache.reads);

  const getAverageAccessTime = (cacheIndex = 0): number => {
    const cache = caches[cacheIndex];
    const hitRate = Number(cache.hits) / Number(cache.reads);
    const missRate = 1 - hitRate;

    const penaltyTime = caches[cacheIndex + 1]
      ? getAverageAccessTime(cacheIndex + 1)
      : Number(cache.parameters.missPenalty);

    return Number(cache.parameters.hitTime) + penaltyTime * missRate;
  };

  return (
    <div
      className={clsx(
        {
          "bg-red-500":
            cycle === history.cycle && history.setAccess.replacementReason,
          "bg-green-500":
            cycle === history.cycle && !history.setAccess.replacementReason,
          "bg-gray-200 opacity-20": cycle !== history.cycle,
        },
        "mb-4"
      )}
    >
      <div className="mx-auto container flex py-2 gap-8 pl-4">
        <h2
          className={clsx(
            "px-2 py-1 text-lg font-bold font-mono self-center border rounded-lg",
            {
              "border-black": true,
            }
          )}
        >
          L{cache.getLevel().toString()} CACHE
        </h2>
        <BigNumber
          key="tag"
          description="Tag"
          value={
            <Serialized.Address
              value={history.setAccess.address.tag}
              padStartLength={9}
              padStart="0"
            />
          }
        />
        <BigNumber
          key="set"
          description="Set"
          value={String(history.setIndex)}
        />
        <BigNumber
          key="block"
          description="Block index"
          value={String(history.setAccess.replacedIndex)}
        />
        <BigNumber
          key="hot-rate"
          description="Hit-rate"
          value={formatPercentage(hitRate)}
        />
        <BigNumber
          key="average-access-time"
          description="Average access time"
          value={formatTimeFromNs(getAverageAccessTime(cacheIndex))}
        />
        <BigNumber
          key="result"
          description="Result"
          value={history.setAccess.replacementReason ? "MISS" : "HIT"}
        />
      </div>
    </div>
  );
};
