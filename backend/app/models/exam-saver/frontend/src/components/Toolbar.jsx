export default function Toolbar({ searchTerm, onSearchChange, onUploadClick, tabLabel }) {
  return (
    <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between border border-border bg-surface rounded-b-lg rounded-tr-lg px-4 py-3">
      <div className="relative flex-1 sm:max-w-sm">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z"
          />
        </svg>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder={`Search ${tabLabel.toLowerCase()} by name or description`}
          className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-border bg-paper focus:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber transition-colors"
        />
      </div>

      <button
        onClick={onUploadClick}
        className="inline-flex items-center justify-center gap-2 rounded-md bg-navy text-white text-sm font-medium px-4 py-2 hover:bg-navy-light transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 4v12m0 0l-4-4m4 4l4-4M4 20h16"
          />
        </svg>
        Upload {tabLabel.slice(0, -1)}
      </button>
    </div>
  );
}
