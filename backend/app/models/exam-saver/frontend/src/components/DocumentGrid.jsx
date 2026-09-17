import DocumentCard from "./DocumentCard";
import EmptyState from "./EmptyState";

export default function DocumentGrid({ documents, tabLabel, hasSearch, onOpen }) {
  if (documents.length === 0) {
    return <EmptyState tabLabel={tabLabel} hasSearch={hasSearch} />;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 py-5">
      {documents.map((doc) => (
        <DocumentCard key={doc.id} document={doc} onOpen={onOpen} />
      ))}
    </div>
  );
}
