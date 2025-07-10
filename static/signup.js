 document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const password = document.getElementById("signUpPassword");
    const confirmPassword = document.getElementById("signUpPasswordconfirm");

    form.addEventListener("submit", function (event) {
        if (password.value !== confirmPassword.value) {
            event.preventDefault(); // Prevent form submission
            alert("Passwords do not match! Please try again.");
            confirmPassword.style.border = "2px solid red"; // Highlight confirm password field
        } else {
            confirmPassword.style.border = "2px solid green"; // Optional: Indicate success
        }
    });
});