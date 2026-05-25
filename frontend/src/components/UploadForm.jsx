import { useState } from "react";

import api from "../services/api";

function UploadForm({
  onUploadSuccess,
}) {
  const [file, setFile] = useState(null);
  const [sourceType, setSourceType] =
    useState("SAP");
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file || isUploading) return;

    const formData = new FormData();

    formData.append("company_id", 1);

    formData.append(
      "source_type",
      sourceType
    );

    formData.append("file", file);

    setIsUploading(true);
    setMessage("");
    setError("");

    try {
      await api.post(
        "upload/",
        formData
      );

      setMessage("File uploaded successfully.");

      onUploadSuccess();
      setFile(null);
    } catch (error) {
      setError(
        error?.response?.data?.error ||
        "Upload failed. Please verify source type and file format."
      );
      console.error(error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="glass-panel rise rounded-3xl p-6 md:p-8">
      <h2 className="headline text-2xl font-semibold md:text-3xl">
        Upload ESG Data
      </h2>
      <p className="mt-2 text-sm text-slate-600 md:text-base">
        Select a source and upload a CSV to normalize records into review
        workflow.
      </p>
      <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-[180px_1fr_auto]">
        <select
          value={sourceType}
          onChange={(e) =>
            setSourceType(e.target.value)
          }
          className="rounded-xl border border-emerald-200 bg-white px-4 py-3 font-medium text-slate-700 outline-none transition focus:border-emerald-500"
        >

          <option value="SAP">SAP</option>

          <option value="UTILITY">
            Utility
          </option>

          <option value="TRAVEL">
            Travel
          </option>

        </select>

        <input
          type="file"
          key={file ? file.name : "empty"}
          onChange={(e) =>
            setFile(e.target.files[0])
          }
          className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-emerald-50 file:px-3 file:py-2 file:font-medium file:text-emerald-700 hover:file:bg-emerald-100"
        />

        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className="rounded-xl bg-emerald-700 px-6 py-3 font-semibold text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isUploading ? "Uploading..." : "Upload"}
        </button>
      </div>
      {message ? (
        <p className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
          {message}
        </p>
      ) : null}
      {error ? (
        <p className="mt-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}

export default UploadForm;
