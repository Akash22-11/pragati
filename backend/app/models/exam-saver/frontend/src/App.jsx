import { useEffect, useMemo, useState } from "react";
import FolderTabs, { TABS } from "./components/FolderTabs";
import Toolbar from "./components/Toolbar";
import DocumentGrid from "./components/DocumentGrid";
import UploadModal from "./components/UploadModal";
import DocumentViewer from "./components/DocumentViewer";
import { getDocuments } from "./api";

export default function App() {
  const [activeTab, setActiveTab] = useState("notes");
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [viewingId, setViewingId] = useState(null);

  const activeTabMeta = TABS.find((t) => t.key === activeTab);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setLoadError("");
    setSearchTerm("");

    getDocuments(activeTab)
      .then((docs) => {
        if (!cancelled) setDocuments(docs);
      })
      .catch(() => {
        if (!cancelled) setLoadError("Could not load documents.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [activeTab]);

  const filteredDocuments = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    if (!term) return documents;

    return documents.filter((doc) =>
      [doc.name, doc.description, doc.type].some((field) =>
        field.toLowerCase().includes(term)
      )
    );
  }, [documents, searchTerm]);

  const handleUploaded = (saved) => {
    setDocuments((prev) => [saved, ...prev]);
    setIsUploadOpen(false);
  };

  return (
    <div className="min-h-screen bg-paper">
      <header className="border-b border-border bg-surface">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <h1 className="font-serif text-2xl font-semibold text-ink">
            Exam Saver
          </h1>
          <p className="text-sm text-muted mt-1">
            Keep your notes, photos, and texts organized before exam day.
          </p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 pb-16">
        <div className="mt-6">
          <FolderTabs activeTab={activeTab} onChange={setActiveTab} />
          <Toolbar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            onUploadClick={() => setIsUploadOpen(true)}
            tabLabel={activeTabMeta.label}
          />
        </div>

        {loading && <p className="text-sm text-muted py-10">Loading...</p>}
        {loadError && <p className="text-sm text-red-600 py-10">{loadError}</p>}

        {!loading && !loadError && (
          <DocumentGrid
            documents={filteredDocuments}
            tabLabel={activeTabMeta.label}
            hasSearch={searchTerm.trim().length > 0}
            onOpen={(doc) => setViewingId(doc.id)}
          />
        )}
      </main>

      {isUploadOpen && (
        <UploadModal
          type={activeTab}
          tabLabel={activeTabMeta.label}
          onClose={() => setIsUploadOpen(false)}
          onUploaded={handleUploaded}
        />
      )}

      {viewingId && (
        <DocumentViewer id={viewingId} onClose={() => setViewingId(null)} />
      )}
    </div>
  );
}
