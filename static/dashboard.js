// Add click event to update the active class
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach((link) => {
        link.addEventListener("click", function () {
            // Remove active class from all links
            navLinks.forEach((nav) => nav.classList.remove("active"));
            // Add active class to the clicked link
            this.classList.add("active");
        });
    });
});