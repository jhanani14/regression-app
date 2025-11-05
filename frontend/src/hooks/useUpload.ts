import { useState } from "react";
import api from "../api";

export function useUpload() {
  const [uploading, setUploading] = useState(false);

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);
    try {
      const res = await api.post("/datasets/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res.data;
    } finally {
      setUploading(false);
    }
  };

  return { uploadFile, uploading };
}
