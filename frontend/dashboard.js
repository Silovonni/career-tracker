let goals = [];

let currentUser = null;


// ============================================================
// ELEMENTS
// ============================================================

const modal =
    document.getElementById("goal-modal");

const openButton =
    document.getElementById("open-goal-modal");

const emptyCreateButton =
    document.getElementById("empty-create-button");

const closeButton =
    document.getElementById("close-modal");

const cancelButton =
    document.getElementById("cancel-goal");

const goalForm =
    document.getElementById("goal-form");

const goalContainer =
    document.getElementById("goals-container");

const goalFilter =
    document.getElementById("goal-filter");

const message =
    document.getElementById("goal-message");

const logoutButton =
    document.getElementById("logout-button");

const profileEditButton =
    document.querySelector(".profile-panel .secondary-button");


// ============================================================
// GOAL MODAL
// ============================================================

function openModal() {

    modal.classList.remove("hidden");

    const title =
        document.getElementById("goal-title");

    if (title) {
        title.focus();
    }
}


function closeModal() {

    modal.classList.add("hidden");

    goalForm.reset();

    message.textContent = "";
}


if (openButton) {

    openButton.addEventListener(
        "click",
        openModal
    );
}


if (emptyCreateButton) {

    emptyCreateButton.addEventListener(
        "click",
        openModal
    );
}


if (closeButton) {

    closeButton.addEventListener(
        "click",
        closeModal
    );
}


if (cancelButton) {

    cancelButton.addEventListener(
        "click",
        closeModal
    );
}


const modalOverlay =
    document.querySelector(".modal-overlay");


if (modalOverlay) {

    modalOverlay.addEventListener(
        "click",
        closeModal
    );
}


// ============================================================
// LOAD USER
// ============================================================

async function loadCurrentUser() {

    try {

        const response =
            await fetch("/api/auth/me");

        if (!response.ok) {

            if (response.status === 401) {

                window.location.href = "/auth";

                return;
            }

            throw new Error(
                "Unable to load your profile."
            );
        }

        const data =
            await response.json();

        currentUser =
            data.user;

        updateDashboardProfile();

    }

    catch (error) {

        console.error(
            "Profile loading error:",
            error
        );
    }
}


// ============================================================
// UPDATE DASHBOARD PROFILE
// ============================================================

function updateDashboardProfile() {

    if (!currentUser) {
        return;
    }


    const profileName =
        document.getElementById(
            "profile-name"
        );


    const profileAvatar =
        document.getElementById(
            "profile-avatar"
        );


    const targetRole =
        document.getElementById(
            "target-role"
        );


    const education =
        document.getElementById(
            "education"
        );


    const experience =
        document.getElementById(
            "experience-level"
        );


    if (profileName) {

        profileName.textContent =
            currentUser.name ||
            "CareerOS User";
    }


    if (profileAvatar) {

        profileAvatar.textContent =
            getInitials(
                currentUser.name
            );
    }


    if (targetRole) {

        targetRole.textContent =
            currentUser.target_role ||
            "Not set";
    }


    if (education) {

        education.textContent =
            currentUser.education ||
            "Not set";
    }


    if (experience) {

        experience.textContent =
            currentUser.experience_level ||
            "Not set";
    }
}


function getInitials(name) {

    if (!name) {
        return "C";
    }

    const parts =
        name
            .trim()
            .split(/\s+/);

    if (parts.length === 1) {

        return parts[0]
            .charAt(0)
            .toUpperCase();
    }

    return (
        parts[0].charAt(0) +
        parts[parts.length - 1].charAt(0)
    ).toUpperCase();
}


// ============================================================
// CAREER PROFILE EDITOR
// ============================================================

function openProfileEditor() {

    if (!currentUser) {
        return;
    }


    const role =
        prompt(
            "Target Role",
            currentUser.target_role || ""
        );


    if (role === null) {
        return;
    }


    const education =
        prompt(
            "Education",
            currentUser.education || ""
        );


    if (education === null) {
        return;
    }


    const experience =
        prompt(
            "Experience Level",
            currentUser.experience_level || ""
        );


    if (experience === null) {
        return;
    }


    const skills =
        prompt(
            "Skills",
            currentUser.skills || ""
        );


    if (skills === null) {
        return;
    }


    const summary =
        prompt(
            "Career Summary",
            currentUser.career_summary || ""
        );


    if (summary === null) {
        return;
    }


    saveProfile(
        role,
        education,
        experience,
        skills,
        summary
    );
}


async function saveProfile(
    targetRole,
    education,
    experienceLevel,
    skills,
    careerSummary
) {

    try {

        const response =
            await fetch(
                "/api/profile",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        target_role:
                            targetRole,

                        education:
                            education,

                        experience_level:
                            experienceLevel,

                        skills:
                            skills,

                        career_summary:
                            careerSummary
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to save career profile."
            );
        }


        currentUser = {
            ...currentUser,

            target_role:
                data.profile.target_role,

            education:
                data.profile.education,

            experience_level:
                data.profile.experience_level,

            skills:
                data.profile.skills,

            career_summary:
                data.profile.career_summary
        };


        updateDashboardProfile();


        alert(
            "Career profile updated successfully."
        );

    }

    catch (error) {

        alert(
            error.message
        );
    }
}


if (profileEditButton) {

    profileEditButton.addEventListener(
        "click",
        openProfileEditor
    );
}


// ============================================================
// GOALS
// ============================================================

async function loadGoals() {

    try {

        const response =
            await fetch(
                "/api/goals"
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load goals."
            );
        }


        goals =
            await response.json();


        renderGoals();

    }

    catch (error) {

        console.error(
            "Goals loading error:",
            error
        );

        if (goalContainer) {

            goalContainer.innerHTML = `
                <div class="empty-state">

                    <div class="empty-icon">
                        !
                    </div>

                    <h3>
                        Unable to load goals
                    </h3>

                    <p>
                        ${escapeHTML(error.message)}
                    </p>

                </div>
            `;
        }
    }
}


// ============================================================
// RENDER GOALS
// ============================================================

function renderGoals() {

    if (!goalContainer) {
        return;
    }


    const filter =
        goalFilter
            ? goalFilter.value
            : "all";


    const filteredGoals =
        goals.filter(goal => {

            if (filter === "all") {
                return true;
            }

            return goal.status === filter;

        });


    updateStats();


    if (filteredGoals.length === 0) {

        goalContainer.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    ◎
                </div>

                <h3>
                    Your roadmap starts here
                </h3>

                <p>
                    Create your first career goal and start turning your plans into progress.
                </p>

                <button
                    class="primary-button"
                    onclick="openModal()"
                >
                    ＋ Create Your First Goal
                </button>

            </div>
        `;

        return;
    }


    goalContainer.innerHTML =
        filteredGoals
            .map(
                goal =>
                    createGoalHTML(goal)
            )
            .join("");
}


// ============================================================
// GOAL HTML
// ============================================================

function createGoalHTML(goal) {

    const completed =
        goal.status === "completed";


    return `

        <div
            class="goal-card ${
                completed
                    ? "completed"
                    : ""
            }"
        >

            <div class="goal-main">

                <button
                    class="goal-check ${
                        completed
                            ? "completed"
                            : ""
                    }"
                    onclick="completeGoal(${goal.id})"
                    ${
                        completed
                            ? "disabled"
                            : ""
                    }
                >
                    ${
                        completed
                            ? "✓"
                            : ""
                    }
                </button>


                <div class="goal-info">

                    <h3>
                        ${escapeHTML(
                            goal.title
                        )}
                    </h3>

                    <p>
                        ${escapeHTML(
                            goal.description ||
                            "No description provided."
                        )}
                    </p>

                </div>

            </div>


            <div class="goal-actions">

                <span
                    class="goal-status ${
                        completed
                            ? "completed"
                            : ""
                    }"
                >
                    ${
                        completed
                            ? "Completed"
                            : "Active"
                    }
                </span>


                <button
                    class="delete-goal"
                    onclick="deleteGoal(${goal.id})"
                    title="Delete goal"
                >
                    ×
                </button>

            </div>

        </div>
    `;
}


// ============================================================
// STATS
// ============================================================

function updateStats() {

    const total =
        goals.length;


    const active =
        goals.filter(
            goal =>
                goal.status === "active"
        ).length;


    const completed =
        goals.filter(
            goal =>
                goal.status === "completed"
        ).length;


    const totalElement =
        document.getElementById(
            "total-goals"
        );


    const activeElement =
        document.getElementById(
            "active-goals"
        );


    const completedElement =
        document.getElementById(
            "completed-goals"
        );


    if (totalElement) {
        totalElement.textContent =
            total;
    }


    if (activeElement) {
        activeElement.textContent =
            active;
    }


    if (completedElement) {
        completedElement.textContent =
            completed;
    }
}


// ============================================================
// CREATE GOAL
// ============================================================

if (goalForm) {

    goalForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const title =
                document
                    .getElementById(
                        "goal-title"
                    )
                    .value
                    .trim();


            const description =
                document
                    .getElementById(
                        "goal-description"
                    )
                    .value
                    .trim();


            try {

                const response =
                    await fetch(
                        "/api/goals",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    title,
                                    description
                                })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        data.error ||
                        "Unable to create goal."
                    );
                }


                closeModal();

                await loadGoals();

            }

            catch (error) {

                message.textContent =
                    error.message;
            }
        }
    );
}


// ============================================================
// COMPLETE GOAL
// ============================================================

async function completeGoal(goalId) {

    try {

        const response =
            await fetch(
                `/api/goals/${goalId}/complete`,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to complete goal."
            );
        }


        await loadGoals();

    }

    catch (error) {

        alert(
            error.message
        );
    }
}


// ============================================================
// DELETE GOAL
// ============================================================

async function deleteGoal(goalId) {

    if (
        !confirm(
            "Delete this career goal?"
        )
    ) {
        return;
    }


    try {

        const response =
            await fetch(
                `/api/goals/${goalId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Unable to delete goal."
            );
        }


        await loadGoals();

    }

    catch (error) {

        alert(
            error.message
        );
    }
}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(value) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


// ============================================================
// FILTER
// ============================================================

if (goalFilter) {

    goalFilter.addEventListener(
        "change",
        renderGoals
    );
}


// ============================================================
// LOGOUT
// ============================================================

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        async () => {

            try {

                await fetch(
                    "/api/auth/logout",
                    {
                        method: "POST"
                    }
                );

            }

            finally {

                window.location.href =
                    "/auth";
            }
        }
    );
}


// ============================================================
// INITIALIZE
// ============================================================

async function initializeDashboard() {

    await loadCurrentUser();

    await loadGoals();
}


initializeDashboard();