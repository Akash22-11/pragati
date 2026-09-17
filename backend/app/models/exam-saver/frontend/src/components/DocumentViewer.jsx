import { useEffect, useState } from "react";
import { getDocument, fileUrl } from "../api";

const TYPE_LABEL = { notes: "Note", photos: "Photo", texts: "Text" };

export default function DocumentViewer({ id, onClose }) {
  const [document, setDocument] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    getDocument(id)
      .then((doc) => {
        if (!cancelled) setDocument(doc);
      })
      .catch(() => {
        if (!cancelled) setError("Could not load this item.");
      });

    return () => {
      cancelled = true;
    };
  }, [id]);

  return (
    <div
      className="fixed inset-0 z-50 bg-ink/40 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-surface rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-border">
          <h2 className="font-serif text-lg font-semibold text-ink">
            {document ? document.name : "Loading..."}
          </h2>
          <button
            onClick={onClose}
            aria-label="Close"
            className="text-muted hover:text-ink text-xl leading-none focus-visible:outline-none"
          >
            &times;
          </button>
        </div>

        <div className="px-6 py-5 space-y-4">
          {error && <p className="text-sm text-red-600">{error}</p>}

          {!error && !document && (
            <p className="text-sm text-muted">Fetching details...</p>
          )}

          {document && (
            <>
              {document.type === "photos" && (
                <img
                  src={fileUrl(document.file_path)}
                  alt={document.name}
                  className="w-full rounded-md border border-border"
                />
              )}

              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="text-xs uppercase tracking-wide text-muted">
                    Type
                  </dt>
                  <dd className="text-ink">{TYPE_LABEL[document.type]}</dd>
                </div>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-muted">
                    Description
                  </dt>
                  <dd className="text-ink whitespace-pre-wrap">
                    {document.description}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-muted">
                    Usage
                  </dt>
                  <dd className="text-ink whitespace-pre-wrap">
                    {document.usage}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs uppercase tracking-wide text-muted">
                    Saved
                  </dt>
                  <dd className="text-ink">
                    {new Date(document.created_at).toLocaleString()}
                  </dd>
                </div>
              </dl>

              <a
                href={fileUrl(document.file_path)}
                target="_blank"
                rel="noreferrer"
                className="inline-block text-sm font-medium text-navy underline underline-offset-2"
              >
                Open original file
              </a>

              <p className="text-xs text-muted pt-2 border-t border-border">
                This item is read-only and cannot be edited or deleted.
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
