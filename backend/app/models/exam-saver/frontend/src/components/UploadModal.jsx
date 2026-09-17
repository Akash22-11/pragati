import { useRef, useState } from "react";
import { uploadDocument } from "../api";

const ACCENT = {
  notes: "border-navy text-navy",
  photos: "border-amber text-amber",
  texts: "border-sage text-sage",
};

const BUTTON_ACCENT = {
  notes: "bg-navy hover:bg-navy-light",
  photos: "bg-amber hover:bg-amber-light",
  texts: "bg-sage hover:bg-sage-light",
};

export default function UploadModal({ type, tabLabel, onClose, onUploaded }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [form, setForm] = useState({ name: "", description: "", usage: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  const handleFileSelect = (selected) => {
    if (selected && selected.length > 0) {
      setFile(selected[0]);
      setError("");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Choose a file first.");
      return;
    }
    if (!form.name.trim() || !form.description.trim() || !form.usage.trim()) {
      setError("Name, description, and usage are all required.");
      return;
    }

    setSubmitting(true);
    setError("");
    try {
      const saved = await uploadDocument({ file, type, ...form });
      onUploaded(saved);
    } catch (err) {
      setError(
        err?.response?.data?.error || "Something went wrong while uploading."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-ink/40 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label={`Upload a ${tabLabel.slice(0, -1)}`}
    >
      <div className="bg-surface rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-border">
          <h2 className="font-serif text-lg font-semibold text-ink">
            Upload to {tabLabel}
          </h2>
          <button
            onClick={onClose}
            aria-label="Close"
            className="text-muted hover:text-ink text-xl leading-none focus-visible:outline-none"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-5">
          {/* Step 1: file picker / dropzone */}
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            className={[
              "border-2 border-dashed rounded-md px-4 py-8 text-center cursor-pointer transition-colors",
              isDragging ? ACCENT[type] : "border-border text-muted",
            ].join(" ")}
          >
            <input
              ref={inputRef}
              type="file"
              className="hidden"
              onChange={(e) => handleFileSelect(e.target.files)}
            />
            {file ? (
              <p className="text-sm text-ink font-medium">{file.name}</p>
            ) : (
              <>
                <p className="text-sm font-medium">
                  Drag and drop a file here, or click to browse
                </p>
                <p className="text-xs text-muted mt-1">
                  This file will be saved as read-only once uploaded.
                </p>
              </>
            )}
          </div>

          {/* Step 2: metadata form, shown once a file is chosen */}
          {file && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-ink mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="e.g. Chapter 4 formulas"
                  className="w-full px-3 py-2 text-sm rounded-md border border-border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-ink mb-1">
                  Description
                </label>
                <textarea
                  value={form.description}
                  onChange={(e) =>
                    setForm({ ...form, description: e.target.value })
                  }
                  placeholder="What is this file?"
                  rows={2}
                  className="w-full px-3 py-2 text-sm rounded-md border border-border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-ink mb-1">
                  Usage
                </label>
                <textarea
                  value={form.usage}
                  onChange={(e) => setForm({ ...form, usage: e.target.value })}
                  placeholder="When or how should this be used?"
                  rows={2}
                  className="w-full px-3 py-2 text-sm rounded-md border border-border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber"
                />
              </div>
            </div>
          )}

          {error && <p className="text-sm text-red-600">{error}</p>}

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium rounded-md border border-border text-ink hover:bg-paper transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!file || submitting}
              className={`px-4 py-2 text-sm font-medium rounded-md text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${BUTTON_ACCENT[type]}`}
            >
              {submitting ? "Saving..." : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
