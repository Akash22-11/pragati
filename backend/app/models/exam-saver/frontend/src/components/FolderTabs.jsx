const TABS = [
  { key: "notes", label: "Notes", accent: "bg-navy", ring: "ring-navy" },
  { key: "photos", label: "Photos", accent: "bg-amber", ring: "ring-amber" },
  { key: "texts", label: "Texts", accent: "bg-sage", ring: "ring-sage" },
];

export default function FolderTabs({ activeTab, onChange }) {
  return (
    <div className="flex gap-1" role="tablist" aria-label="Document category">
      {TABS.map((tab) => {
        const isActive = tab.key === activeTab;
        return (
          <button
            key={tab.key}
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(tab.key)}
            className={[
              "relative px-6 py-2.5 rounded-t-lg font-serif text-[15px] font-semibold transition-colors",
              "focus-visible:outline-none",
              isActive
                ? "bg-surface text-ink z-10"
                : "bg-paper text-muted hover:text-ink",
            ].join(" ")}
            style={{
              marginBottom: isActive ? "-1px" : "0",
              boxShadow: isActive ? "0 -1px 0 0 #DCE1D8 inset" : "none",
            }}
          >
            <span
              className={`absolute left-0 right-0 top-0 h-[3px] rounded-t-lg ${
                isActive ? tab.accent : "bg-transparent"
              }`}
            />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}

export { TABS };
