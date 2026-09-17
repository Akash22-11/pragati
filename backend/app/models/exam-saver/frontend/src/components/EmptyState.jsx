export default function EmptyState({ tabLabel, hasSearch }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 text-muted">
      <p className="text-sm">
        {hasSearch
          ? `No ${tabLabel.toLowerCase()} match your search.`
          : `No ${tabLabel.toLowerCase()} saved yet. Upload one to get started.`}
      </p>
    </div>
  );
}
