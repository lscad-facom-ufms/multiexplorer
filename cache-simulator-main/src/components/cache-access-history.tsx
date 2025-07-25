import { CheckCircle2, XCircle } from "lucide-react";
import { clsx } from "clsx";
import { CacheAccess } from "../cache/cache-access.ts";
import { Serialized } from "./serializers/serialized.tsx";
import { ReactNode } from "react";

function AddressPart({
  label,
  value,
  color,
}: {
  label: string;
  value: ReactNode;
  color: string;
}) {
  return (
    <div
      className={`flex items-center ${color} rounded-lg px-2 py-1 shadow-sm gap-1`}
    >
      <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">
        {label}:
      </span>
      <span className="text-xs font-bold text-gray-700 tracking-wide">
        {value}
      </span>
    </div>
  );
}

export function CacheAccessCard({ access }: { access: CacheAccess }) {
  return (
    <div className={clsx(`border rounded-lg mb-2`)}>
      <div className="p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium text-gray-800">
              Cycle {String(access.cycle)}
            </span>
            <div
              className={clsx(
                "flex px-2 py-1 items-center text-xs rounded-full",
                {
                  "bg-red-500 text-white": access.setAccess.replacementReason,
                  "bg-green-500 text-white":
                    !access.setAccess.replacementReason,
                }
              )}
            >
              {!access.setAccess.replacementReason ? (
                <CheckCircle2 className="mr-1 h-3 w-3" />
              ) : (
                <XCircle className="mr-1 h-3 w-3" />
              )}
              {!access.setAccess.replacementReason ? "Hit" : "Miss"}
            </div>
          </div>
          <span className="text-sm font-mono">
            <Serialized.Address value={access.setAccess.address.raw} />
          </span>
        </div>
        <div className="mt-3 flex justify-end space-x-2">
          {/*TODO parse the address*/}
          <AddressPart
            color="bg-blue-200"
            label="Tag"
            value={<Serialized.Tag value={access.setAccess.address.tag} />}
          />
          <AddressPart
            color="bg-red-200"
            label="Set"
            value={
              <Serialized.Index
                value={BigInt(access.setAccess.address.index)}
              />
            }
          />
          <AddressPart
            color="bg-green-200"
            label="Block"
            value={
              <Serialized.BlockOffset
                value={BigInt(access.setAccess.replacedIndex)}
              />
            }
          />
        </div>
      </div>
    </div>
  );
}

export default function CacheAccessHistory({
  history,
}: {
  history: CacheAccess[];
}) {
  return (
    <div className="w-full max-w-2xl mx-auto">
      {history.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          No cache accesses yet.
        </div>
      ) : (
        <div className="flex flex-col-reverse space-y-2">
          {history.map((access) => (
            <CacheAccessCard key={access.cycle} access={access} />
          ))}
        </div>
      )}
    </div>
  );
}
