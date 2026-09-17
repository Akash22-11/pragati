import { fileUrl } from "../api";

const BORDER_ACCENT = {
  notes: "border-l-navy",
  photos: "border-l-amber",
  texts: "border-l-sage",
};

export default function DocumentCard({ document, onOpen }) {
  const formattedDate = new Date(document.created_at).toLocaleDateString(
    undefined,
    { year: "numeric", month: "short", day: "numeric" }
  );

  return (
    <button
      onClick={() => onOpen(document)}
      className={[
        "text-left bg-surface border border-border border-l-4 rounded-md p-4",
        "hover:shadow-md transition-shadow focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber",
        BORDER_ACCENT[document.type],
      ].join(" ")}
    >
      {document.type === "photos" && (
        <img
          src={fileUrl(document.file_path)}
          alt={document.name}
          className="w-full h-32 object-cover rounded mb-3 bg-paper"
        />
      )}
      <h3 className="font-serif font-semibold text-ink truncate">
        {document.name}
      </h3>
      <p className="text-sm text-muted mt-1 line-clamp-2">
        {document.description}
      </p>
      <p className="text-xs text-muted mt-3">Saved {formattedDate}</p>
    </button>
  );
}
