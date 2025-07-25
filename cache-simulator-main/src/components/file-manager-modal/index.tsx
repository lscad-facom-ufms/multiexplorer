import { Modal, UploadProps, message } from "antd";
import { usePrograms } from "../../contexts/programs.tsx";
import { InboxOutlined } from "@ant-design/icons";
import Dragger from "antd/lib/upload/Dragger";
import { FileArchive } from "lucide-react";

type FileManagerModalProps = {
  open: boolean;
  onClose: () => void;
};

// TODO add DnD feature to reorder caches?
export const FileManagerModal = ({ open, onClose }: FileManagerModalProps) => {
  const { programs, setPrograms } = usePrograms();

  const uploaderProps: UploadProps = {
    name: "file",
    fileList: [],
    beforeUpload: async (file) => {
      // Check file extension
      if (!file.name.endsWith(".json")) {
        message.error("Only JSON files are supported.");
        return false;
      }
      try {
        const raw = await file.text();
        const json = JSON.parse(raw);
        // TODO validate the parsed content
        const instructions = json.map(
          (instruction: Record<string, string>) => instruction
        );
        setPrograms({ ...programs, [file.name]: instructions });
      } catch (e) {
        message.error("Invalid JSON file.");
        return false;
      }
      return false; // Prevent auto-upload
    },
  };

  return (
    <>
      <Modal
        title="Program manager"
        open={open}
        onCancel={onClose}
        cancelButtonProps={{ hidden: true }}
        okButtonProps={{ hidden: true }}
      >
        <Dragger {...uploaderProps}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">Click or drag file to start parsing</p>
          <p className="ant-upload-hint">
            Only TracerGrind texttrace dumps are supported!
          </p>
        </Dragger>

        <ul className="flex flex-col mt-4 gap-2">
          {Object.entries(programs).map(([name, instructions]) => (
            <li
              key={name}
              className="flex gap-4 px-4 py-2 items-center bg-gray-100 rounded-lg"
            >
              <FileArchive className="text-gray-500" />
              <div className="flex-grow">
                <h3>{name}</h3>
                <span className="text-xs text-gray-700">
                  {instructions.length} instructions
                </span>
              </div>
              {/*TODO implement trash*/}
              {/*<Trash className="text-gray-500"/>*/}
            </li>
          ))}
        </ul>
      </Modal>
    </>
  );
};
