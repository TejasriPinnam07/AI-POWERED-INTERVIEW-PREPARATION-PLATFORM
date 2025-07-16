document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const showLogin = document.getElementById("show-login");
    const showSignup = document.getElementById("show-signup");
    const toggleBtn = document.getElementById("toggle-btn");

    showLogin?.addEventListener("click", (e) => {
        e.preventDefault();
        loginForm.style.display = "block";
        signupForm.style.display = "none";
    });

    showSignup?.addEventListener("click", (e) => {
        e.preventDefault();
        loginForm.style.display = "none";
        signupForm.style.display = "block";
    });

    toggleBtn?.addEventListener("click", () => {
        if (signupForm.style.display === "block") {
            signupForm.style.display = "none";
            loginForm.style.display = "block";
        } else {
            signupForm.style.display = "block";
            loginForm.style.display = "none";
        }
    });
});
