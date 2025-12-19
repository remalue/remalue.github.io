const toggleButton = document.getElementById("theme-toggle");
const sunIcon = document.getElementById("sun");
const moonIcon = document.getElementById("moon");

// 1. Check local storage or system preference on load
const currentTheme = localStorage.getItem("theme");
const systemPreference = window.matchMedia("(prefers-color-scheme: dark)").matches;

if (currentTheme === "dark" || (!currentTheme && systemPreference)) {
    document.documentElement.setAttribute("data-theme", "dark");
    sunIcon.style.display = "block";
    moonIcon.style.display = "none";
} else {
    document.documentElement.setAttribute("data-theme", "light");
    sunIcon.style.display = "none";
    moonIcon.style.display = "block";
}

// 2. Handle click event
toggleButton.addEventListener("click", () => {
    const theme = document.documentElement.getAttribute("data-theme");
    console.log(theme);
    
    if (theme === "light") {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
        sunIcon.style.display = "block";
        moonIcon.style.display = "none";
    } else {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
        sunIcon.style.display = "none";
        moonIcon.style.display = "block";
    }
});