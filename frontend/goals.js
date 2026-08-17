const modal = document.getElementById("goal-modal");

const openButton = document.getElementById("open-goal-modal");

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


let goals = [];



function openModal() {

    modal.classList.remove("hidden");

    document
        .getElementById("goal-title")
        .focus();
}



function closeModal() {

    modal.classList.add("hidden");

    goalForm.reset();

    message.textContent = "";
}



openButton.addEventListener(
    "click",
    openModal
);


emptyCreateButton.addEventListener(
    "click",
    openModal
);


closeButton.addEventListener(
    "click",
    closeModal
);


cancelButton.addEventListener(
    "click",
    closeModal
);



document
    .querySelector(".modal-overlay")
    .addEventListener(
        "click",
        closeModal
    );



async function loadGoals() {

    try {

        const response = await fetch(
            "/api/goals"
        );


        if (!response.ok) {

            throw new Error(
                "Unable to load goals."
            );

        }


        goals = await response.json();

        renderGoals();

    }

    catch (error) {

        goalContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">!</div>

                <h3>
                    Unable to load goals
                </h3>

                <p>
                    ${error.message}
                </p>
            </div>
        `;

    }

}



function renderGoals() {

    const filter =
        goalFilter.value;


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
                    No goals found
                </h3>

                <p>
                    Create a goal to start building your career roadmap.
                </p>

                <button
                    class="primary-button"
                    onclick="openModal()"
                >
                    Create Goal
                </button>

            </div>
        `;

        return;
    }


    goalContainer.innerHTML =
        filteredGoals
            .map(goal => createGoalHTML(goal))
            .join("");

}



function createGoalHTML(goal) {

    const completed =
        goal.status === "completed";


    return `
        <div
            class="goal-card ${completed ? "completed" : ""}"
        >

            <div class="goal-main">

                <button
                    class="goal-check ${completed ? "completed" : ""}"
                    onclick="completeGoal(${goal.id})"
                    ${completed ? "disabled" : ""}
                >
                    ${completed ? "✓" : ""}
                </button>


                <div class="goal-info">

                    <h3>
                        ${escapeHTML(goal.title)}
                    </h3>

                    <p>
                        ${escapeHTML(
                            goal.description || "No description provided."
                        )}
                    </p>

                </div>

            </div>


            <div class="goal-actions">

                <span
                    class="goal-status ${completed ? "completed" : ""}"
                >
                    ${completed ? "Completed" : "Active"}
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



function updateStats() {

    const total =
        goals.length;


    const active =
        goals.filter(
            goal => goal.status === "active"
        ).length;


    const completed =
        goals.filter(
            goal => goal.status === "completed"
        ).length;


    document.getElementById(
        "total-goals"
    ).textContent = total;


    document.getElementById(
        "active-goals"
    ).textContent = active;


    document.getElementById(
        "completed-goals"
    ).textContent = completed;

}



goalForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const title =
            document
                .getElementById("goal-title")
                .value
                .trim();


        const description =
            document
                .getElementById("goal-description")
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

                        body: JSON.stringify({
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



async function completeGoal(
    goalId
) {

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

        alert(error.message);

    }

}



async function deleteGoal(
    goalId
) {

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

        alert(error.message);

    }

}



function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}



goalFilter.addEventListener(
    "change",
    renderGoals
);



loadGoals();