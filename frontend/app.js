// ==========================================
// CAREEROS DASHBOARD
// ==========================================

const storedUser =
    localStorage.getItem("careeros_user");


if (!storedUser) {

    window.location.href = "/auth";

}


const user = JSON.parse(storedUser);

const userId = user.id;


// ==========================================
// ELEMENTS
// ==========================================

const userName =
    document.getElementById("userName");

const userUsername =
    document.getElementById("userUsername");

const userInitial =
    document.getElementById("userInitial");

const careerGoal =
    document.getElementById("careerGoal");

const careerScore =
    document.getElementById("careerScore");

const projectCount =
    document.getElementById("projectCount");

const skillCount =
    document.getElementById("skillCount");

const studyHours =
    document.getElementById("studyHours");

const projectList =
    document.getElementById("projectList");

const skillList =
    document.getElementById("skillList");

const activityList =
    document.getElementById("activityList");


// ==========================================
// USER HEADER
// ==========================================

userName.textContent =
    user.name || "Career Builder";


userUsername.textContent =
    user.username || "User";


userInitial.textContent =
    (user.name || "C")
        .charAt(0)
        .toUpperCase();


// ==========================================
// LOAD DASHBOARD
// ==========================================

async function loadDashboard() {

    try {

        const response =
            await fetch(
                `/api/dashboard/${userId}`
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load dashboard."
            );

        }


        const data =
            await response.json();


        renderDashboard(data);

    }

    catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


// ==========================================
// RENDER DASHBOARD
// ==========================================

function renderDashboard(data) {

    const profile =
        data.profile;


    careerGoal.textContent =
        profile.career_goal ||
        "Define your career goal.";


    careerScore.textContent =
        profile.career_score || 0;


    projectCount.textContent =
        data.projects.length;


    skillCount.textContent =
        data.skills.length;


    studyHours.textContent =
        profile.study_hours || 0;


    renderProjects(
        data.projects
    );


    renderSkills(
        data.skills
    );


    renderActivity(
        data.activity
    );

}


// ==========================================
// PROJECTS
// ==========================================

function renderProjects(projects) {

    if (!projects.length) {

        projectList.innerHTML = `
            <div class="empty-state">
                No projects yet.
                Add your first project.
            </div>
        `;

        return;

    }


    projectList.innerHTML =
        projects
            .map(
                project => `

                <div class="project-item">

                    <strong>
                        ${escapeHtml(
                            project.name
                        )}
                    </strong>

                    <p>
                        ${escapeHtml(
                            project.description || ""
                        )}
                    </p>

                    <div class="progress-bar">

                        <div
                            class="progress-fill"
                            style="width: ${project.progress}%"
                        ></div>

                    </div>

                </div>

            `
            )
            .join("");

}


// ==========================================
// SKILLS
// ==========================================

function renderSkills(skills) {

    if (!skills.length) {

        skillList.innerHTML = `
            <div class="empty-state">
                No skills tracked yet.
                Add your first skill.
            </div>
        `;

        return;

    }


    skillList.innerHTML =
        skills
            .map(
                skill => `

                <div class="skill-item">

                    <div class="skill-top">

                        <strong>
                            ${escapeHtml(
                                skill.name
                            )}
                        </strong>

                        <span class="skill-level">
                            ${escapeHtml(
                                skill.level
                            )}
                            ·
                            ${skill.progress}%
                        </span>

                    </div>

                    <div class="progress-bar">

                        <div
                            class="progress-fill"
                            style="width: ${skill.progress}%"
                        ></div>

                    </div>

                </div>

            `
            )
            .join("");

}


// ==========================================
// ACTIVITY
// ==========================================

function renderActivity(activity) {

    if (!activity.length) {

        activityList.innerHTML = `
            <div class="empty-state">
                No learning activity yet.
                Log your first study session.
            </div>
        `;

        return;

    }


    activityList.innerHTML =
        activity
            .map(
                item => `

                <div class="activity-item">

                    <div>

                        <strong>
                            ${escapeHtml(
                                item.topic ||
                                "Learning session"
                            )}
                        </strong>

                        <span>
                            ${item.activity_date}
                        </span>

                    </div>

                    <div class="activity-hours">
                        ${item.hours} hrs
                    </div>

                </div>

            `
            )
            .join("");

}


// ==========================================
// PROFILE
// ==========================================

const profileModal =
    document.getElementById(
        "profileModal"
    );


document
    .getElementById(
        "profileButton"
    )
    .addEventListener(
        "click",
        function() {

            profileModal.classList.remove(
                "hidden"
            );

        }
    );


document
    .getElementById(
        "profileForm"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const goal =
                document
                    .getElementById(
                        "careerGoalInput"
                    )
                    .value
                    .trim();


            const hours =
                Number(
                    document
                        .getElementById(
                            "studyHoursInput"
                        )
                        .value
                );


            const response =
                await fetch(
                    "/api/profile",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            user_id: userId,

                            career_goal: goal,

                            study_hours: hours

                        })
                    }
                );


            if (response.ok) {

                profileModal.classList.add(
                    "hidden"
                );

                await loadDashboard();

            }

        }
    );


// ==========================================
// PROJECT MODAL
// ==========================================

const projectModal =
    document.getElementById(
        "projectModal"
    );


document
    .getElementById(
        "addProjectButton"
    )
    .addEventListener(
        "click",
        function() {

            projectModal.classList.remove(
                "hidden"
            );

        }
    );


document
    .getElementById(
        "projectForm"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const name =
                document
                    .getElementById(
                        "projectName"
                    )
                    .value
                    .trim();


            const description =
                document
                    .getElementById(
                        "projectDescription"
                    )
                    .value
                    .trim();


            const response =
                await fetch(
                    "/api/projects",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            user_id: userId,

                            name: name,

                            description:
                                description,

                            status: "planned",

                            progress: 0

                        })
                    }
                );


            if (response.ok) {

                document
                    .getElementById(
                        "projectForm"
                    )
                    .reset();

                projectModal.classList.add(
                    "hidden"
                );

                await loadDashboard();

            }

        }
    );


// ==========================================
// SKILL MODAL
// ==========================================

const skillModal =
    document.getElementById(
        "skillModal"
    );


document
    .getElementById(
        "addSkillButton"
    )
    .addEventListener(
        "click",
        function() {

            skillModal.classList.remove(
                "hidden"
            );

        }
    );


document
    .getElementById(
        "skillForm"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const name =
                document
                    .getElementById(
                        "skillName"
                    )
                    .value
                    .trim();


            const level =
                document
                    .getElementById(
                        "skillLevel"
                    )
                    .value;


            const progress =
                Number(
                    document
                        .getElementById(
                            "skillProgress"
                        )
                        .value
                );


            const response =
                await fetch(
                    "/api/skills",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            user_id: userId,

                            name: name,

                            level: level,

                            progress: progress

                        })
                    }
                );


            if (response.ok) {

                document
                    .getElementById(
                        "skillForm"
                    )
                    .reset();

                skillModal.classList.add(
                    "hidden"
                );

                await loadDashboard();

            }

        }
    );


// ==========================================
// ACTIVITY MODAL
// ==========================================

const activityModal =
    document.getElementById(
        "activityModal"
    );


document
    .getElementById(
        "addActivityButton"
    )
    .addEventListener(
        "click",
        function() {

            activityModal.classList.remove(
                "hidden"
            );

        }
    );


document
    .getElementById(
        "activityForm"
    )
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const hours =
                Number(
                    document
                        .getElementById(
                            "activityHours"
                        )
                        .value
                );


            const topic =
                document
                    .getElementById(
                        "activityTopic"
                    )
                    .value
                    .trim();


            const notes =
                document
                    .getElementById(
                        "activityNotes"
                    )
                    .value
                    .trim();


            const response =
                await fetch(
                    "/api/activity",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            user_id: userId,

                            hours: hours,

                            topic: topic,

                            notes: notes

                        })
                    }
                );


            if (response.ok) {

                document
                    .getElementById(
                        "activityForm"
                    )
                    .reset();

                activityModal.classList.add(
                    "hidden"
                );

                await loadDashboard();

            }

        }
    );


// ==========================================
// CLOSE MODALS
// ==========================================

document
    .querySelectorAll(
        "[data-close]"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                function() {

                    const modalId =
                        button.dataset.close;

                    document
                        .getElementById(
                            modalId
                        )
                        .classList.add(
                            "hidden"
                        );

                }
            );

        }
    );


// ==========================================
// LOGOUT
// ==========================================

document
    .getElementById(
        "logoutButton"
    )
    .addEventListener(
        "click",
        function() {

            localStorage.removeItem(
                "careeros_user"
            );

            window.location.href =
                "/auth";

        }
    );


// ==========================================
// HTML SAFETY
// ==========================================

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;

}


// ==========================================
// START
// ==========================================

loadDashboard();