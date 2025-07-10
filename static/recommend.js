function generateRecommendations() {
        const healthTips = [
            "Stay hydrated! Drink at least 8 glasses of water a day.",
            "Take short breaks while working to reduce stress.",
            "Avoid processed foods and eat more fresh vegetables."
        ];

        const dietRecommendations = [
            "Eat a balanced diet rich in proteins, carbs, and healthy fats.",
            "If diabetic, focus on whole grains and avoid sugary drinks.",
            "Incorporate fiber-rich foods like lentils and oats into your meals."
        ];

        const exerciseSuggestions = [
            "Try 30 minutes of walking daily for cardiovascular health.",
            "For joint pain, opt for swimming or yoga exercises.",
            "Strength training 2-3 times a week helps maintain muscle mass."
        ];

        document.getElementById("daily-tip-text").innerText = healthTips[Math.floor(Math.random() * healthTips.length)];
        document.getElementById("diet-text").innerText = dietRecommendations[Math.floor(Math.random() * dietRecommendations.length)];
        document.getElementById("exercise-text").innerText = exerciseSuggestions[Math.floor(Math.random() * exerciseSuggestions.length)];
    }
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