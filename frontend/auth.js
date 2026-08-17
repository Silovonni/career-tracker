// ============================================================
// CAREEROS AUTHENTICATION
// ============================================================


// ============================================================
// ELEMENTS
// ============================================================

const loginSection =
    document.getElementById(
        "login-section"
    );

const registerSection =
    document.getElementById(
        "register-section"
    );

const loginForm =
    document.getElementById(
        "login-form"
    );

const registerForm =
    document.getElementById(
        "register-form"
    );

const showRegister =
    document.getElementById(
        "show-register"
    );

const showLogin =
    document.getElementById(
        "show-login"
    );

const message =
    document.getElementById(
        "auth-message"
    );


// ============================================================
// MESSAGE SYSTEM
// ============================================================

function showMessage(
    text,
    type = "error"
) {

    if (!message) {
        return;
    }

    message.textContent = text;

    message.className =
        "auth-message " + type;
}


function clearMessage() {

    if (!message) {
        return;
    }

    message.textContent = "";

    message.className =
        "auth-message";
}


// ============================================================
// SWITCH TO REGISTER
// ============================================================

if (showRegister) {

    showRegister.addEventListener(
        "click",
        function(event) {

            event.preventDefault();

            clearMessage();

            loginSection.classList.add(
                "hidden"
            );

            registerSection.classList.remove(
                "hidden"
            );

        }
    );

}


// ============================================================
// SWITCH TO LOGIN
// ============================================================

if (showLogin) {

    showLogin.addEventListener(
        "click",
        function(event) {

            event.preventDefault();

            clearMessage();

            registerSection.classList.add(
                "hidden"
            );

            loginSection.classList.remove(
                "hidden"
            );

        }
    );

}


// ============================================================
// REGISTER
// ============================================================

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            clearMessage();


            const name =
                document
                    .getElementById(
                        "register-name"
                    )
                    .value
                    .trim();


            const email =
                document
                    .getElementById(
                        "register-email"
                    )
                    .value
                    .trim()
                    .toLowerCase();


            const password =
                document
                    .getElementById(
                        "register-password"
                    )
                    .value;


            if (name.length < 2) {

                showMessage(
                    "Please enter your full name.",
                    "error"
                );

                return;
            }


            if (password.length < 8) {

                showMessage(
                    "Password must contain at least 8 characters.",
                    "error"
                );

                return;
            }


            showMessage(
                "Creating your CareerOS account...",
                "loading"
            );


            try {

                const response =
                    await fetch(
                        "/api/auth/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                name: name,
                                email: email,
                                password: password
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showMessage(
                        data.detail ||
                        data.error ||
                        "Unable to create your account.",
                        "error"
                    );

                    return;
                }


                if (!data.success) {

                    showMessage(
                        data.error ||
                        "Unable to create your account.",
                        "error"
                    );

                    return;
                }


                localStorage.setItem(
                    "careeros_user",
                    JSON.stringify(
                        data.user
                    )
                );


                showMessage(
                    "Account created successfully.",
                    "success"
                );


                setTimeout(
                    function() {

                        window.location.href =
                            "/";

                    },
                    800
                );

            }

            catch (error) {

                console.error(
                    "Registration error:",
                    error
                );

                showMessage(
                    "CareerOS could not connect to the server.",
                    "error"
                );

            }

        }
    );

}


// ============================================================
// LOGIN
// ============================================================

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            clearMessage();


            const email =
                document
                    .getElementById(
                        "login-email"
                    )
                    .value
                    .trim()
                    .toLowerCase();


            const password =
                document
                    .getElementById(
                        "login-password"
                    )
                    .value;


            showMessage(
                "Signing you in...",
                "loading"
            );


            try {

                const response =
                    await fetch(
                        "/api/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                email: email,
                                password: password
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showMessage(
                        data.detail ||
                        data.error ||
                        "Invalid email or password.",
                        "error"
                    );

                    return;
                }


                if (!data.success) {

                    showMessage(
                        data.error ||
                        "Invalid email or password.",
                        "error"
                    );

                    return;
                }


                localStorage.setItem(
                    "careeros_user",
                    JSON.stringify(
                        data.user
                    )
                );


                showMessage(
                    "Login successful.",
                    "success"
                );


                setTimeout(
                    function() {

                        window.location.href =
                            "/";

                    },
                    600
                );

            }

            catch (error) {

                console.error(
                    "Login error:",
                    error
                );

                showMessage(
                    "CareerOS could not connect to the server.",
                    "error"
                );

            }

        }
    );

}