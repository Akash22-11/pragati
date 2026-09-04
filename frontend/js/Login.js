/* =====================================================
   LOGIN FORM
===================================================== */
/* =====================================================
   ELEMENTS
===================================================== */

const loginContainer =
    document.getElementById(
        "loginFormContainer"
    );

const signupContainer =
    document.getElementById(
        "signupFormContainer"
    );


const showSignup =
    document.getElementById(
        "showSignup"
    );

const showLogin =
    document.getElementById(
        "showLogin"
    );


const loginForm =
    document.getElementById(
        "loginForm"
    );

const signupForm =
    document.getElementById(
        "signupForm"
    );


const toast =
    document.getElementById(
        "toast"
    );


/* =====================================================
   SWITCH LOGIN / SIGNUP
===================================================== */

showSignup.addEventListener(
    "click",
    () => {

        loginContainer.classList.remove(
            "active"
        );

        signupContainer.classList.add(
            "active"
        );

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


showLogin.addEventListener(
    "click",
    () => {

        signupContainer.classList.remove(
            "active"
        );

        loginContainer.classList.add(
            "active"
        );

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


/* =====================================================
   PASSWORD SHOW / HIDE
===================================================== */

const passwordButtons =
    document.querySelectorAll(
        ".password-toggle"
    );


passwordButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            const targetID =
                button.dataset.target;

            const password =
                document.getElementById(
                    targetID
                );


            if (
                password.type ===
                "password"
            ) {

                password.type =
                    "text";

                button.textContent =
                    "Hide";

            } else {

                password.type =
                    "password";

                button.textContent =
                    "Show";

            }

        }
    );

});


/* =====================================================
   TOAST FUNCTION
===================================================== */

function showToast(message) {

    toast.textContent =
        message;

    toast.classList.add(
        "show"
    );


    setTimeout(() => {

        toast.classList.remove(
            "show"
        );

    }, 2500);

}


/* =====================================================
   ERROR FUNCTION
===================================================== */

function setError(
    elementID,
    message
) {

    const element =
        document.getElementById(
            elementID
        );

    element.textContent =
        message;

}


/* =====================================================
   CLEAR ERRORS
===================================================== */

function clearErrors() {

    document
        .querySelectorAll(".error")
        .forEach(element => {

            element.textContent = "";

        });

}


/* =====================================================
   EMAIL VALIDATION
===================================================== */

function validEmail(email) {

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        .test(email);

}


/* =====================================================
   LOGIN FORM
===================================================== */

loginForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        clearErrors();


        const email =
            document.getElementById(
                "loginEmail"
            ).value.trim();


        const password =
            document.getElementById(
                "loginPassword"
            ).value;


        let valid = true;


        /* Email */

        if (!email) {

            setError(
                "loginEmailError",
                "Please enter your email address."
            );

            valid = false;

        }

        else if (
            !validEmail(email)
        ) {

            setError(
                "loginEmailError",
                "Please enter a valid email address."
            );

            valid = false;

        }


        /* Password */

        if (!password) {

            setError(
                "loginPasswordError",
                "Please enter your password."
            );

            valid = false;

        }

        else if (
            password.length < 6
        ) {

            setError(
                "loginPasswordError",
                "Password must contain at least 6 characters."
            );

            valid = false;

        }


        if (!valid) {

            return;

        }


        /*
           FRONTEND DEMO ONLY

           In a real project,
           send credentials to your backend.
        */

        showToast(
            "Signing in..."
        );


        setTimeout(() => {

            showToast(
                "Login successful!"
            );

        }, 900);

    }
);


/* =====================================================
   PASSWORD STRENGTH
===================================================== */

const signupPassword =
    document.getElementById(
        "signupPassword"
    );


const strengthBars =
    document.querySelectorAll(
        ".strength-bars span"
    );


const strengthText =
    document.getElementById(
        "strengthText"
    );


signupPassword.addEventListener(
    "input",
    () => {

        const password =
            signupPassword.value;


        let strength = 0;


        if (
            password.length >= 8
        ) {

            strength++;

        }


        if (
            /[A-Z]/.test(password)
        ) {

            strength++;

        }


        if (
            /[0-9]/.test(password)
        ) {

            strength++;

        }


        if (
            /[^A-Za-z0-9]/.test(password)
        ) {

            strength++;

        }


        strengthBars.forEach(
            bar => {

                bar.style.background =
                    "#ddd7ce";

            }
        );


        if (password.length === 0) {

            strengthText.textContent =
                "Use 8+ characters";

            return;

        }


        if (strength === 1) {

            strengthBars[0].style.background =
                "#d95b5b";

            strengthText.textContent =
                "Weak password";

        }


        else if (strength === 2) {

            strengthBars[0].style.background =
                "#e0a23c";

            strengthBars[1].style.background =
                "#e0a23c";

            strengthText.textContent =
                "Fair password";

        }


        else if (strength === 3) {

            strengthBars[0].style.background =
                "#08a89e";

            strengthBars[1].style.background =
                "#08a89e";

            strengthBars[2].style.background =
                "#08a89e";

            strengthText.textContent =
                "Good password";

        }


        else if (strength === 4) {

            strengthBars.forEach(
                bar => {

                    bar.style.background =
                        "#08a957";

                }
            );

            strengthText.textContent =
                "Strong password";

        }

    }
);


/* =====================================================
   SIGNUP FORM
===================================================== */

signupForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        clearErrors();


        const name =
            document.getElementById(
                "signupName"
            ).value.trim();


        const email =
            document.getElementById(
                "signupEmail"
            ).value.trim();


        const rollNumber =
            document.getElementById(
                "rollNumber"
            ).value.trim();


        const password =
            document.getElementById(
                "signupPassword"
            ).value;


        const confirmPassword =
            document.getElementById(
                "confirmPassword"
            ).value;


        const terms =
            document.getElementById(
                "terms"
            ).checked;


        let valid = true;


        /* Name */

        if (!name) {

            setError(
                "signupNameError",
                "Please enter your full name."
            );

            valid = false;

        }

        else if (
            name.length < 3
        ) {

            setError(
                "signupNameError",
                "Name must contain at least 3 characters."
            );

            valid = false;

        }


        /* Email */

        if (!email) {

            setError(
                "signupEmailError",
                "Please enter your student email."
            );

            valid = false;

        }

        else if (
            !validEmail(email)
        ) {

            setError(
                "signupEmailError",
                "Please enter a valid email address."
            );

            valid = false;

        }


        /* Roll Number */

        if (!rollNumber) {

            setError(
                "rollNumberError",
                "Please enter your roll number."
            );

            valid = false;

        }


        /* Password */

        if (!password) {

            setError(
                "signupPasswordError",
                "Please create a password."
            );

            valid = false;

        }

        else if (
            password.length < 8
        ) {

            setError(
                "signupPasswordError",
                "Password must contain at least 8 characters."
            );

            valid = false;

        }


        /* Confirm password */

        if (!confirmPassword) {

            setError(
                "confirmPasswordError",
                "Please confirm your password."
            );

            valid = false;

        }

        else if (
            password !==
            confirmPassword
        ) {

            setError(
                "confirmPasswordError",
                "Passwords do not match."
            );

            valid = false;

        }


        /* Terms */

        if (!terms) {

            setError(
                "termsError",
                "You must agree to continue."
            );

            valid = false;

        }


        if (!valid) {

            return;

        }


        /*
           FRONTEND DEMO

           Normally this data should be
           sent to your backend API.
        */


        document
            .getElementById(
                "successModal"
            )
            .classList.add(
                "show"
            );

    }
);


/* =====================================================
   CONTINUE AFTER SIGNUP
===================================================== */

document
    .getElementById(
        "continueButton"
    )
    .addEventListener(
        "click",
        () => {

            document
                .getElementById(
                    "successModal"
                )
                .classList.remove(
                    "show"
                );


            signupForm.reset();


            signupContainer.classList.remove(
                "active"
            );

            loginContainer.classList.add(
                "active"
            );


            showToast(
                "You can now sign in."
            );

        }
    );


/* =====================================================
   DEMO LOGIN
===================================================== */

document
    .getElementById(
        "demoLogin"
    )
    .addEventListener(
        "click",
        () => {

            document
                .getElementById(
                    "loginEmail"
                )
                .value =
                "arjun.sharma@webpragati.edu.in";


            document
                .getElementById(
                    "loginPassword"
                )
                .value =
                "Demo@123";


            showToast(
                "Demo credentials filled."
            );

        }
    );


/* =====================================================
   FORGOT PASSWORD
===================================================== */

document
    .getElementById(
        "forgotPassword"
    )
    .addEventListener(
        "click",
        event => {

            event.preventDefault();

            showToast(
                "Password reset link would be sent to your email."
            );

        }
    );

loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    clearErrors();

    const email = document
        .getElementById("loginEmail")
        .value
        .trim()
        .toLowerCase();

    const password = document
        .getElementById("loginPassword")
        .value;

    const rememberMe = document
        .getElementById("rememberMe")
        .checked;

    let valid = true;


    /* =========================
       EMAIL VALIDATION
    ========================= */

    if (!email) {

        setError(
            "loginEmailError",
            "Please enter your email address."
        );

        valid = false;

    } else if (!validEmail(email)) {

        setError(
            "loginEmailError",
            "Please enter a valid email address."
        );

        valid = false;
    }


    /* =========================
       PASSWORD VALIDATION
    ========================= */

    if (!password) {

        setError(
            "loginPasswordError",
            "Please enter your password."
        );

        valid = false;

    } else if (password.length < 6) {

        setError(
            "loginPasswordError",
            "Password must contain at least 6 characters."
        );

        valid = false;
    }


    if (!valid) {
        return;
    }


    /* =================================================
       DEMO ACCOUNT
       Replace this later with your backend/database
    ================================================= */

    const demoAccount = {

        name: "Arjun Sharma",

        email: "arjun.sharma@webpragati.edu.in",

        password: "Demo@123",

        rollNo: "CS22B047",

        semester: "6th Semester",

        batch: "2022–2026",

        cgpa: "9.12",

        rank: "#3",

        credits: "114"

    };


    /* =========================
       CHECK LOGIN
    ========================= */

    if (
        email !== demoAccount.email ||
        password !== demoAccount.password
    ) {

        setError(
            "loginPasswordError",
            "Incorrect email or password."
        );

        return;
    }


    /* =========================
       SAVE USER ACCOUNT
    ========================= */

    const loggedInUser = {

        name: demoAccount.name,

        email: demoAccount.email,

        rollNo: demoAccount.rollNo,

        semester: demoAccount.semester,

        batch: demoAccount.batch,

        cgpa: demoAccount.cgpa,

        rank: demoAccount.rank,

        credits: demoAccount.credits

    };


    /*
       Save account information in browser
    */

    localStorage.setItem(
        "webPragatiUser",
        JSON.stringify(loggedInUser)
    );


    /* =========================
       REMEMBER LOGIN
    ========================= */

    if (rememberMe) {

        localStorage.setItem(
            "webPragatiLoggedIn",
            "true"
        );

    } else {

        sessionStorage.setItem(
            "webPragatiLoggedIn",
            "true"
        );

    }


    /* =========================
       REDIRECT TO DASHBOARD
    ========================= */

    showToast("Login successful!");


    setTimeout(() => {

        window.location.href = "index.html";

    }, 500);

});