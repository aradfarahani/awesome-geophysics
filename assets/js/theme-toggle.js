function toggleTheme() {
  document.body.classList.toggle("dark-mode");
  const button = document.querySelector(".theme-toggle");
  button.textContent = document.body.classList.contains("dark-mode")
    ? "Switch to Light Mode"
    : "Switch to Dark Mode";
}

// Detect user's preferred color scheme on load
if (
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches
) {
  document.body.classList.add("dark-mode");
  document.querySelector(".theme-toggle").textContent = "Switch to Light Mode";
}
