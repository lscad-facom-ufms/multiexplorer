import { Button, Form, Modal, Select, Tabs, TabsProps } from "antd";
import { useEffect, useState } from "react";
import { Clock, Cpu, ListRestart, Map, Shuffle, Zap } from "lucide-react";
import {
  parametersToCapacity,
  parameterToHumanReadable,
} from "../../helpers/parameters.ts";
import { CacheParameters } from "../../cache/cache-parameters.ts";
import {
  formatCapacity,
  formatNumber,
  formatTimeFromNs,
} from "../../helpers/number.ts";
// import { DynamicLogSlider } from "../dynamic-log-slider";
import { NonDynamicLogSlider } from "../non-dynamic-log-slider";
// import { DynamicLogRadio } from "../dynamic-log-radio";
import { NonDynamicLogRadio } from "../non-dynamic-log-radio";
import { ParameterVisualizerModal } from "../parameter-visualizer-modal";
// import { DynamicSlider } from "../dynamic-slider";
import { NonDynamicSlider } from "../non-dynamic-slider";
import { addCache as addCacheToStorage } from "../../utils/storage-cache.ts";

const defaultCache: CacheParameters = {
  sets: 32n,
  blocksPerSet: 2n,
  wordsPerBlock: 8n,
  wordSize: 64n,
  hitTime: 1n,
  missPenalty: 10n,
  policy: "LRU",
};

type ConfiguratorModalProps = {
  initialCaches?: CacheParameters[];
  open: boolean;
  onCreate: (caches: CacheParameters[]) => void;
  onClose: () => void;
};

function getNewDefaultCache() {
  return { ...defaultCache };
}

// TODO add DnD feature to reorder caches?
export const ConfiguratorModal = ({
  initialCaches,
  open,
  onCreate,
  onClose,
}: ConfiguratorModalProps) => {
  const [visualizerModalOpen, setVisualizerModalOpen] = useState(false);
  const [selectedCache, setSelectedCache] = useState(0);
  const [customCacheTiming, setCustomCacheTiming] = useState(false);
  const [caches, setCaches] = useState<CacheParameters[]>([
    getNewDefaultCache(),
    getNewDefaultCache(),
  ]);

  const [form] = Form.useForm();

  useEffect(() => {
    if (!open) {
      return;
    }

    if (initialCaches) {
      setCaches(initialCaches.map((cache) => ({ ...cache })));
    } else {
      setCaches([getNewDefaultCache()]);
    }
  }, [open]);

  function addCache() {
    setCaches([...caches, { ...defaultCache }]);
  }

  function removeCache(key: string) {
    setCaches(caches.filter((_, i) => i !== Number(key)));
  }

  const currentCache = caches[selectedCache];

  const handleCacheTabsEdit: TabsProps["onEdit"] = (event, action) => {
    if (action === "add") {
      addCache();
    } else {
      if (typeof event !== "string") {
        throw new Error(
          "Was not expecting a non-string TabProps.onEdit remove event"
        );
      }
      removeCache(event);
    }
  };

  const handleModalOk = () => {
    addCacheToStorage(caches);
    onCreate(caches);
    setSelectedCache(currentCache ? caches.indexOf(currentCache) : 0);
    onClose();
  };

  const handleModalCancel = () => {
    onClose();
  };

  const updateCache = <T extends keyof CacheParameters>(
    cacheIndex: number,
    property: T,
    value: CacheParameters[T]
  ) => {
    setCaches(
      caches.map((cache, i) => {
        if (i !== cacheIndex) {
          return cache;
        }
        return {
          ...cache,
          [property]: value,
        };
      })
    );
  };

  return (
    <>
      <ParameterVisualizerModal
        parameters={caches[0]}
        open={visualizerModalOpen}
        onClose={() => setVisualizerModalOpen(false)}
      />
      <Modal
        title={
          initialCaches
            ? "Editing Cache Configuration"
            : "Creating Cache Configuration"
        }
        width="50vw"
        open={open}
        onOk={handleModalOk}
        onCancel={handleModalCancel}
        maskClosable={false}
      >
        <Tabs
          defaultActiveKey={String(selectedCache)}
          type="editable-card"
          size="small"
          onChange={(key) => setSelectedCache(Number(key))}
          onEdit={handleCacheTabsEdit}
          items={caches.map((_, index) => ({
            label: `L${index + 1} Cache`,
            key: String(index),
            closable: true,
          }))}
        />

        <div className="h-full">
          <Form form={form} layout="vertical" onValuesChange={console.log}>
            <Form.Item
              label={`Number of sets: ${formatNumber(
                Number(currentCache.sets)
              )}`}
            >
              <NonDynamicLogSlider
                max={15}
                value={Number(currentCache.sets ?? 1)}
                onChange={(value) => {
                  updateCache(selectedCache, "sets", BigInt(value));
                }}
                defaultValue={30}
                tooltip={{ open: false }}
              />
            </Form.Item>
            <Form.Item
              label={`Blocks per Set: ${formatNumber(
                Number(currentCache.blocksPerSet)
              )}`}
            >
              <NonDynamicLogSlider
                max={5}
                value={Number(currentCache.blocksPerSet ?? 1n)}
                onChange={(value) => {
                  updateCache(selectedCache, "blocksPerSet", BigInt(value));
                }}
                defaultValue={30}
                tooltip={{ open: false }}
              />
            </Form.Item>
            <Form.Item label="Words per Block">
              <NonDynamicLogRadio
                min={0}
                max={6}
                value={Number(currentCache.wordsPerBlock)}
                onChange={(value) => {
                  updateCache(selectedCache, "wordsPerBlock", BigInt(value));
                }}
              />
            </Form.Item>
            <Form.Item label="Replacement Policy">
              <Select
                defaultValue="LRU"
                onChange={(value) => {
                  updateCache(selectedCache, "policy", value as "LRU" | "FIFO");
                }}
                options={[
                  {
                    value: "LRU",
                    label: (
                      <div className="flex items-center gap-1">
                        <Clock className="w-4" />
                        <span>LRU (Least Recently Used)</span>
                      </div>
                    ),
                  },
                  {
                    value: "FIFO",
                    label: (
                      <div className="flex items-center gap-1">
                        <ListRestart className="w-4" />
                        <span>FIFO (First In, First Out)</span>
                      </div>
                    ),
                  },
                  {
                    value: "RANDOM",
                    label: (
                      <div className="flex items-center gap-1">
                        <Shuffle className="w-4" />
                        <span>Random</span>
                      </div>
                    ),
                  },
                ]}
              />
            </Form.Item>
            <Form.Item label="Cache Timing">
              <Select
                defaultValue="default"
                onChange={(value) => {
                  setCustomCacheTiming(value === "custom");
                }}
                options={[
                  {
                    value: "default",
                    label: (
                      <div className="flex items-center gap-1">
                        <Zap className="w-4" />
                        <span>Default</span>
                      </div>
                    ),
                  },
                  {
                    value: "custom",
                    label: (
                      <div className="flex items-center gap-1">
                        <Cpu className="w-4" />
                        <span>Custom</span>
                      </div>
                    ),
                  },
                ]}
              />
            </Form.Item>

            {customCacheTiming && (
              <>
                <Form.Item
                  label={`Hit time: ${formatTimeFromNs(
                    Number(currentCache.hitTime)
                  )}`}
                >
                  <NonDynamicSlider
                    min={1}
                    max={100}
                    value={Number(currentCache.hitTime ?? 1n)}
                    onChange={(value) => {
                      updateCache(selectedCache, "hitTime", BigInt(value));
                    }}
                    defaultValue={30}
                    tooltip={{ open: false }}
                  />
                </Form.Item>

                <Form.Item
                  label={`Miss penalty: ${formatTimeFromNs(
                    Number(currentCache.missPenalty)
                  )}`}
                >
                  <NonDynamicSlider
                    min={1}
                    max={100}
                    value={Number(currentCache.missPenalty ?? 1n)}
                    onChange={(value) => {
                      updateCache(selectedCache, "missPenalty", BigInt(value));
                    }}
                    defaultValue={30}
                    tooltip={{ open: false }}
                  />
                </Form.Item>
              </>
            )}

            <div className="bg-gray-100 px-4 py-4 rounded">
              <div className="flex mb-2">
                <h2 className="flex-grow text-lg font-medium">
                  Cache Hierarchy Overview
                </h2>
                <Button
                  size="small"
                  icon={<Map size={16} />}
                  onClick={() => setVisualizerModalOpen(true)}
                >
                  View in visualizer
                </Button>
              </div>
              <ul className="my-1">
                {caches.map((cache, index) => (
                  <li key={index} className="flex justify-between">
                    <span>L{index + 1} Cache:</span>
                    <span>{parameterToHumanReadable(cache)}</span>
                  </li>
                ))}
              </ul>
              <span className="font-medium">
                Total Capacity:{" "}
                {formatCapacity(parametersToCapacity(caches), 2)}
              </span>
            </div>
          </Form>
        </div>
      </Modal>
    </>
  );
};
