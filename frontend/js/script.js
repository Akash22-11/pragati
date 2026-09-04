/* =====================================================
   PAGE DATA
===================================================== */

const pages = {

    /* =================================================
       ACHIEVEMENTS
    ================================================= */

    achievements: `

        <div class="page-heading">

            <h2>
                Verified Achievements
            </h2>

            <p>
                5 verified · 1 pending verification
            </p>

        </div>


        <div class="achievement-grid">


            <!-- 1 -->

            ${achievementCard(
                "HACKATHON",
                "Smart India Hackathon 2024",
                "Winner",
                "Issued by Ministry of Education, GoI",
                "Dec 2024",
                "National",
                "tag-hackathon",
                "level-national",
                "verified"
            )}


            <!-- 2 -->

            ${achievementCard(
                "COMPETITIVE PROGRAMMING",
                "ACM ICPC 2024 — Regionals",
                "Rank 18",
                "Issued by ACM",
                "Nov 2024",
                "International",
                "tag-programming",
                "level-international",
                "verified"
            )}


            <!-- 3 -->

            ${achievementCard(
                "CERTIFICATION",
                "AWS Certified Solutions Architect",
                "Certified",
                "Issued by Amazon Web Services",
                "Sep 2026",
                "Professional",
                "tag-certification",
                "level-professional",
                "verified"
            )}


            <!-- 4 -->

            ${achievementCard(
                "OPEN SOURCE",
                "Google Summer of Code 2024",
                "Selected Contributor",
                "Issued by Google LLC",
                "May 2026",
                "International",
                "tag-open-source",
                "level-international",
                "verified"
            )}


            <!-- 5 -->

            ${achievementCard(
                "RESEARCH",
                "Best Research Paper — TechSymp 2026",
                "1st Place",
                "Issued by Pragati Institute",
                "Mar 2026",
                "University",
                "tag-research",
                "level-university",
                "verified"
            )}


            <!-- 6 -->

            ${achievementCard(
                "OPEN SOURCE",
                "GitHub Arctic Code Vault Contributor",
                "Contributor",
                "Issued by GitHub Inc.",
                "Jan 2026",
                "International",
                "tag-open-source",
                "level-international",
                "pending"
            )}

        </div>

    `,


    /* =================================================
       TIMELINE
    ================================================= */

    timeline: `

        <div class="page-heading">

            <h2>
                Activity Timeline
            </h2>

            <p>
                Academic milestones and achievements across your journey
            </p>

        </div>


        <div class="timeline">


            ${timelineItem(
                "3rd Semester commenced",
                "Enrolled in 6 courses — 16 credits this semester.",
                "ACADEMIC",
                "Aug 2025",
                ""
            )}


            ${timelineItem(
                "Research paper accepted at IEEE COMSNETS",
                // '"Federated Learning for Edge Inference" co-authored with Prof. Meera Nair.',
                "ACHIEVEMENT",
                "Jul 2025",
                "achievement"
            )}


            ${timelineItem(
                "Internship at Flipkart — SDE Intern",
                // "Worked on recommendation system microservices using Go and Kafka.",
                // "ACHIEVEMENT",
                // "May 2025",
                // "achievement"
            )}


            ${timelineItem(
                "Won Smart India Hackathon 2026",
                "Team of 6 built an AI-powered crop disease detection system.",
                "ACHIEVEMENT",
                "Dec 2025",
                "achievement"
            )}

        </div>

    `,


    /* =================================================
       OVERVIEW
    ================================================= */

    overview: `

        <div class="page-heading">

            <h2>
                Student Overview
            </h2>

            <p>
                Your academic profile at a glance
            </p>

        </div>


        <div class="generic-grid">


            <div class="generic-card">

                <h3>
                    Academic Performance
                </h3>

                <p>

                    Current CGPA:
                    <strong>
                        9.12 / 10.0
                    </strong>

                    <br>

                    Class Rank:
                    <strong>
                        #3 / 120
                    </strong>

                    <br>

                    Credits Completed:
                    <strong>
                        114 / 160
                    </strong>

                </p>

            </div>


            <div class="generic-card">

                <h3>
                    Current Semester
                </h3>

                <p>

                    3rd Semester

                    <br>

                    6 Courses · 16 Credits

                    <br>

                    Advisor:
                    Prof. Dr. Sudakshina Dasgupta

                </p>

            </div>


            <div class="generic-card">

                <h3>
                    Highlights
                </h3>

                <p>

                    5 verified achievements,
                    research publication,
                    internship experience
                    and competitive programming
                    recognition.

                </p>

            </div>

        </div>

    `,


    /* =================================================
       COURSES
    ================================================= */

    courses: `

        <div class="page-heading">

            <h2>
                Current Courses
            </h2>

            <p>
                Courses enrolled in the 6th semester
            </p>

        </div>


        <div class="generic-grid">


            ${courseCard(
                "Advanced Algorithms",
                "4 Credits",
                "Core"
            )}


            ${courseCard(
                "Distributed Systems",
                "4 Credits",
                "Core"
            )}


            ${courseCard(
                "Machine Learning",
                "3 Credits",
                "Core"
            )}


            ${courseCard(
                "Cloud Computing",
                "3 Credits",
                "Elective"
            )}


            ${courseCard(
                "Technical Communication",
                "2 Credits",
                "Elective"
            )}

        </div>

    `

};


/* =====================================================
   ACHIEVEMENT CARD FUNCTION
===================================================== */

function achievementCard(
    tag,
    title,
    result,
    issuer,
    date,
    level,
    tagClass,
    levelClass,
    status
) {

    let statusHTML = "";

    if (status === "verified") {

        statusHTML = `
            <span class="verified">
                ◉ VERIFIED
            </span>
        `;

    } else {

        statusHTML = `
            <span class="pending">
                PENDING
            </span>
        `;

    }


    return `

        <article class="achievement-card">


            <div class="card-top">

                <span class="tag ${tagClass}">
                    ${tag}
                </span>

                <span class="level ${levelClass}">
                    ${level}
                </span>

            </div>


            <h3>
                ${title}
            </h3>


            <p class="achievement-description">

                <strong>
                    ${result}
                </strong>

                ·

                ${issuer}

            </p>


            <div class="card-bottom">

                <span>
                    ${date}
                </span>

                ${statusHTML}

            </div>

        </article>

    `;

}


/* =====================================================
   TIMELINE ITEM
===================================================== */

function timelineItem(
    title,
    description,
    type,
    date,
    typeClass
) {

    return `

        <article class="timeline-item">


            <div class="timeline-dot">
            </div>


            <div class="timeline-card">


                <div class="timeline-card-top">


                    <div>

                        <h3>
                            ${title}
                        </h3>

                        <p>
                            ${description}
                        </p>

                    </div>


                    <div class="timeline-meta">

                        <span
                            class="timeline-type ${typeClass}">

                            ${type}

                        </span>


                        <span class="timeline-date">

                            ${date}

                        </span>

                    </div>


                </div>

            </div>

        </article>

    `;

}


/* =====================================================
   COURSE CARD
===================================================== */

function courseCard(
    name,
    credits,
    type
) {

    const tagClass =
        type === "Core"
            ? "tag-programming"
            : "tag-open-source";


    return `

        <div class="generic-card">


            <span class="tag ${tagClass}">

                ${type}

            </span>


            <h3>

                ${name}

            </h3>


            <p>

                ${credits}

                <br>

                Instructor:
                Prof. Meera Nair

            </p>


        </div>

    `;

}


/* =====================================================
   PAGE ELEMENT
===================================================== */

const pageContent =
    document.getElementById(
        "pageContent"
    );


const tabs =
    document.querySelectorAll(
        ".tab"
    );


/* =====================================================
   SHOW PAGE
===================================================== */

function showPage(page) {

    if (!pages[page]) {

        page = "achievements";

    }


    pageContent.innerHTML =
        pages[page];


    tabs.forEach(tab => {

        tab.classList.toggle(
            "active",
            tab.dataset.page === page
        );

    });


    /*
       Store current page in URL
    */

    history.replaceState(
        null,
        "",
        "#" + page
    );


    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}


/* =====================================================
   TAB CLICK
===================================================== */

tabs.forEach(tab => {

    tab.addEventListener(
        "click",
        () => {

            showPage(
                tab.dataset.page
            );

        }
    );

});


/* =====================================================
   INITIAL PAGE
===================================================== */

const currentHash =
    window.location.hash
        .replace("#", "");


if (pages[currentHash]) {

    showPage(currentHash);

} else {

    showPage("achievements");

}


/* =====================================================
   COPY TRANSCRIPT LINK
===================================================== */

const copyButton =
    document.getElementById(
        "copyButton"
    );


copyButton.addEventListener(
    "click",
    async () => {

        const transcriptURL =
            "https://transcript.webpragati.edu.in/verify/WP-CS22B047-2024";


        try {

            await navigator.clipboard.writeText(
                transcriptURL
            );

        } catch (error) {

            console.log(
                "Clipboard access unavailable."
            );

        }


        showToast(
            "Transcript link copied!"
        );

    }
);


/* =====================================================
   VIEW TRANSCRIPT
===================================================== */

const viewTranscript =
    document.getElementById(
        "viewTranscript"
    );


viewTranscript.addEventListener(
    "click",
    () => {

        window.open(
            "https://transcript.webpragati.edu.in/verify/WP-CS22B047-2024",
            "_blank"
        );

    }
);


/* =====================================================
   TOAST
===================================================== */

function showToast(message) {

    const toast =
        document.getElementById(
            "toast"
        );


    toast.textContent =
        message;


    toast.classList.add(
        "show"
    );


    setTimeout(
        () => {

            toast.classList.remove(
                "show"
            );

        },
        1800
    );

}


/* =====================================================
   HELP BUTTON
===================================================== */

const helpButton =
    document.getElementById(
        "helpButton"
    );


helpButton.addEventListener(
    "click",
    () => {

        alert(
            "Web Pragati Student Portal\n\n" +
            "Use Overview, Courses, Achievements and Timeline to navigate through the student profile."
        );

    }
);