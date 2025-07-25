import { BigNumber } from "../big-number.tsx";
import { Serialized } from "../serializers/serialized.tsx";
import { CacheRunner } from "../../cache/cache-runner.ts";
import { formatTimeFromNs } from "../../helpers/number.ts";

type GlobalStatusBarProps = {
  runner: CacheRunner;
};

export const GlobalStatusBar = ({ runner }: GlobalStatusBarProps) => {
  const caches = runner.caches;

  if (!runner.getLastHistoryFromLevel(0)) {
    return undefined;
  }

  const getRuntime = (cacheIndex = 0): number => {
    const cache = caches[cacheIndex];

    const hitTime = Number(cache.hits) * Number(cache.parameters.hitTime);
    const missTime = Number(cache.misses) * Number(cache.parameters.hitTime);
    const penaltyTime = caches[cacheIndex + 1]
      ? getRuntime(cacheIndex + 1)
      : Number(cache.misses) * Number(cache.parameters.missPenalty);

    return hitTime + missTime + penaltyTime;
  };

  const getHitLayer = () => {
    for (let i = 0; i < caches.length; i++) {
      if (!runner.getLastHistoryFromLevel(i)!.setAccess.replacementReason) {
        return i;
      }
    }

    return null;
  };

  const getStatus = () => {
    const layer = getHitLayer();

    if (layer === null) {
      return "MISS";
    }

    return `Hit on L${layer + 1}`;
  };

  return (
    <div className="bg-gray-200">
      <div className="mx-auto container flex py-2 gap-8 pl-4">
        <h2 className="px-2 py-1 text-lg font-bold self-center border border-black rounded-lg">
          GLOBAL
        </h2>
        <BigNumber
          key="cycle"
          description="Cycle"
          value={runner.getCurrentCycle() + 1}
        />
        <BigNumber
          key="address"
          description="Address"
          value={
            <Serialized.Address
              value={runner.getLastHistoryFromLevel(0)!.setAccess.address.raw}
            />
          }
        />
        <BigNumber
          key="instructions"
          description="Instructions"
          value={`${runner.getCurrentCycle() + 1}/${
            runner.instructions.length
          }`}
        />
        <BigNumber
          key="runtime"
          description="Runtime"
          value={formatTimeFromNs(getRuntime(), 2)}
        />
        <BigNumber key="status" description="Status" value={getStatus()} />
      </div>
    </div>
  );
};
