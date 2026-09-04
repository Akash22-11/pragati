// ===== Data source (swap this with real data / API later) =====
const submissions = [
  {
    id: "VQ-001",
    student: "Arjun Sharma",
    roll: "CS22B047",
    program: "B.Tech CSE",
    achievement: "Smart India Hackathon 2024 — Winner",
    org: "Ministry of Education, GoI",
    category: "Hackathon",
    queue: "hod",
    queueLabel: "HOD Queue",
    submitted: "2025-08-01",
    status: "pending",
    files: [
      { name: "SIH_Winner_Certificate.pdf", size: "1.2 MB", type: "pdf" },
      { name: "Team_Photograph.jpg", size: "640 KB", type: "image" }
    ]
  },
  {
    id: "VQ-002",
    student: "Priya Nambiar",
    roll: "EC22B031",
    program: "B.Tech ECE",
    achievement: "ACM ICPC 2024 — Regionals Rank 12",
    org: "ACM",
    category: "Competitive Programming",
    queue: "mentor",
    queueLabel: "Mentor Queue",
    submitted: "2025-07-29",
    status: "pending",
    files: [{ name: "ICPC_Rank_Certificate.pdf", size: "890 KB", type: "pdf" }]
  },
  {
    id: "VQ-003",
    student: "Rohan Desai",
    roll: "ME22B018",
    program: "B.Tech Mech",
    achievement: "IEEE Technical Paper Presentation — 2nd Prize",
    org: "IEEE Student Branch, WPIT",
    category: "Research",
    queue: "hod",
    queueLabel: "HOD Queue",
    submitted: "2025-07-25",
    status: "approved",
    files: [{ name: "IEEE_Prize_Certificate.pdf", size: "1.0 MB", type: "pdf" }]
  },
  {
    id: "VQ-004",
    student: "Sneha Iyer",
    roll: "CS22B062",
    program: "B.Tech CSE",
    achievement: "Google Summer of Code 2024 — Contributor",
    org: "Google LLC",
    category: "Open Source",
    queue: "mentor",
    queueLabel: "Mentor Queue",
    submitted: "2025-07-22",
    status: "pending",
    files: [{ name: "GSoC_Contributor_Certificate.pdf", size: "780 KB", type: "pdf" }]
  },
  {
    id: "VQ-005",
    student: "Amit Kulkarni",
    roll: "IT22B009",
    program: "B.Tech IT",
    achievement: "Codathon 2024 Club Winner — Intra",
    org: "CodeCraft Club, WPIT",
    category: "Club Activity",
    queue: "club",
    queueLabel: "Club Co-ord",
    submitted: "2025-07-20",
    status: "rejected",
    files: [{ name: "Codathon_Winner_Certificate.pdf", size: "510 KB", type: "pdf" }]
  },
  {
    id: "VQ-006",
    student: "Divya Menon",
    roll: "CS22B074",
    program: "B.Tech CSE",
    achievement: "AWS Solutions Architect — Associate",
    org: "Amazon Web Services",
    category: "Certification",
    queue: "hod",
    queueLabel: "HOD Queue",
    submitted: "2025-08-03",
    status: "pending",
    files: [{ name: "AWS_SAA_Certificate.pdf", size: "1.1 MB", type: "pdf" }]
  },
  {
    id: "VQ-007",
    student: "Karan Tiwari",
    roll: "CS22B091",
    program: "B.Tech CSE",
    achievement: "Flipkart GRiD 5.0 — Finalist",
    org: "Flipkart",
    category: "Hackathon",
    queue: "club",
    queueLabel: "Club Co-ord",
    submitted: "2025-08-05",
    status: "pending",
    files: [
      { name: "GRID5_Finalist_Certificate.pdf", size: "910 KB", type: "pdf" },
      { name: "Result_Email_Screenshot.jpg", size: "220 KB", type: "image" }
    ]
  }
];

// ===== State =====
let activeQueue = "all";
let activeStatus = "all";
let selectedId = null;
let activeFileIndex = 0;

// ===== Elements =====
const statsBar = document.getElementById("statsBar");
const submissionList = document.getElementById("submissionList");
const detailPanel = document.getElementById("detailPanel");
const queueTabs = document.getElementById("queueTabs");
const statusTabs = document.getElementById("statusTabs");

// ===== Helpers =====
function countByStatus(status) {
  return submissions.filter((s) => s.status === status).length;
}

function statusLabel(status) {
  return { pending: "Pending", approved: "Approved", rejected: "Rejected", sentback: "Sent Back" }[status];
}

function renderStats() {
  const counts = [
    { status: "pending", label: "Pending" },
    { status: "approved", label: "Approved" },
    { status: "rejected", label: "Rejected" },
    { status: "sentback", label: "Sent Back" }
  ];
  statsBar.innerHTML = counts
    .map(
      (c) => `
      <span class="stat-pill">
        <span class="dot ${c.status}"></span>
        ${countByStatus(c.status)} ${c.label}
      </span>`
    )
    .join("");
}

function getFilteredSubmissions() {
  return submissions.filter((s) => {
    const queueMatch = activeQueue === "all" || s.queue === activeQueue;
    const statusMatch = activeStatus === "all" || s.status === activeStatus;
    return queueMatch && statusMatch;
  });
}

function renderList() {
  const filtered = getFilteredSubmissions();

  if (filtered.length === 0) {
    submissionList.innerHTML = `<div class="detail-empty">No submissions match this filter.</div>`;
    return;
  }

  submissionList.innerHTML = filtered
    .map(
      (s) => `
      <div class="list-row ${s.id === selectedId ? "selected" : ""}" data-id="${s.id}">
        <div>
          <span class="student-name">${s.student}</span>
          <span class="student-meta">${s.roll} · ${s.program}</span>
        </div>
        <div>
          ${s.achievement}
          <span class="achv-org">${s.org}</span>
        </div>
        <div><span class="badge">${s.category}</span></div>
        <div>${s.queueLabel}</div>
        <div>${s.submitted}</div>
        <div>
          <span class="status-tag ${s.status}">
            <span class="dot ${s.status}"></span>
            ${statusLabel(s.status)}
          </span>
        </div>
      </div>`
    )
    .join("");

  // attach row click handlers
  document.querySelectorAll(".list-row").forEach((row) => {
    row.addEventListener("click", () => {
      selectedId = row.dataset.id;
      activeFileIndex = 0;
      renderList();
      renderDetail();
    });
  });
}

function renderDetail() {
  const record = submissions.find((s) => s.id === selectedId);

  if (!record) {
    detailPanel.innerHTML = `<div class="detail-empty">Select a submission from the list to review it.</div>`;
    return;
  }

  const file = record.files[activeFileIndex];

  detailPanel.innerHTML = `
    <div class="detail-top">
      <div class="detail-top-row">
        <div>
          <div class="detail-id">${record.id} · ${record.queueLabel}</div>
          <h2 class="detail-title">${record.achievement}</h2>
        </div>
        <span class="status-pill ${record.status}">${statusLabel(record.status)}</span>
      </div>
      <div class="detail-meta">
        <div><label>Student</label><span>${record.student}</span></div>
        <div><label>Roll No</label><span>${record.roll}</span></div>
        <div><label>Program</label><span>${record.program}</span></div>
      </div>
    </div>

    <div class="file-tabs">
      ${record.files
        .map(
          (f, i) => `
        <button class="file-tab ${i === activeFileIndex ? "active" : ""}" data-index="${i}">
          ${f.type === "pdf" ? "📄" : "🖼"} ${f.name.length > 22 ? f.name.slice(0, 20) + "…" : f.name}
        </button>`
        )
        .join("")}
    </div>

    <div class="preview-wrap">
      <div class="file-row">
        <span class="file-icon">${file.type.toUpperCase()}</span>
        ${file.name}
        <span class="file-size">${file.size}</span>
      </div>
      <div class="cert-card">
        <div class="cert-check">✓</div>
        <div class="cert-eyebrow">Certificate of Achievement</div>
        <h3 class="cert-title">Official Certificate</h3>
        <div class="cert-sub">Document verified · Web Pragati</div>
      </div>
    </div>

    <div class="actions">
      <button class="btn btn-approve" data-action="approved">✓ Approve</button>
      <button class="btn btn-reject" data-action="rejected">✕ Reject</button>
      <button class="btn btn-sendback" data-action="sentback">↺ Send Back with Reason</button>
    </div>
  `;

  // file tab switching
  document.querySelectorAll(".file-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      activeFileIndex = Number(tab.dataset.index);
      renderDetail();
    });
  });

  // approve / reject / send back
  document.querySelectorAll(".actions .btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      record.status = btn.dataset.action;
      renderStats();
      renderList();
      renderDetail();
    });
  });
}

// ===== Filter tab wiring =====
queueTabs.addEventListener("click", (e) => {
  const btn = e.target.closest(".tab");
  if (!btn) return;
  activeQueue = btn.dataset.queue;
  [...queueTabs.children].forEach((t) => t.classList.remove("active"));
  btn.classList.add("active");
  renderList();
});

statusTabs.addEventListener("click", (e) => {
  const btn = e.target.closest(".tab");
  if (!btn) return;
  activeStatus = btn.dataset.status;
  [...statusTabs.children].forEach((t) => t.classList.remove("active"));
  btn.classList.add("active");
  renderList();
});

// ===== Top nav active state (just visual for now — page 2 not built yet) =====
document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll(".nav-link").forEach((l) => l.classList.remove("active"));
    link.classList.add("active");
  });
});

// ===== Dark mode toggle =====
const themeToggle = document.getElementById("themeToggle");
const root = document.documentElement;

function applyTheme(theme) {
  if (theme === "dark") {
    root.setAttribute("data-theme", "dark");
    themeToggle.textContent = "☀️";
  } else {
    root.removeAttribute("data-theme");
    themeToggle.textContent = "🌙";
  }
}

// load saved preference (defaults to light)
applyTheme(localStorage.getItem("theme") || "light");

themeToggle.addEventListener("click", () => {
  const isDark = root.getAttribute("data-theme") === "dark";
  const next = isDark ? "light" : "dark";
  applyTheme(next);
  localStorage.setItem("theme", next);
});

// ===== Initial render =====
renderStats();
renderList();
// auto-select the first pending item so the panel isn't empty on load
selectedId = submissions.find((s) => s.status === "pending")?.id || submissions[0].id;
renderDetail();
renderList();
