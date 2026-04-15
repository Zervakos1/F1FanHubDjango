const qs = (selector, scope = document) => scope.querySelector(selector);
const qsa = (selector, scope = document) => [...scope.querySelectorAll(selector)];

const getRoot = () => document.documentElement;
const getThemeToggle = () => qs("[data-theme-toggle]");
const getDropdowns = () => qsa("[data-dropdown]");

const readStoredTheme = () => {
  try {
    return localStorage.getItem("theme");
  } catch (error) {
    return null;
  }
};

const saveTheme = (theme) => {
  try {
    localStorage.setItem("theme", theme);
  } catch (error) {
    return;
  }
};

const getSystemTheme = () => {
  const supportsMatchMedia = typeof window.matchMedia === "function";
  if (!supportsMatchMedia) return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

const getCurrentTheme = () => getRoot().getAttribute("data-theme") || "light";
const getNextTheme = () => getCurrentTheme() === "dark" ? "light" : "dark";

const updateToggleText = () => {
  const toggle = getThemeToggle();
  if (!toggle) return;
  toggle.textContent = getCurrentTheme() === "dark" ? "Light Mode" : "Dark Mode";
};

const applyTheme = (theme) => {
  getRoot().setAttribute("data-theme", theme);
  saveTheme(theme);
  updateToggleText();
};

const setInitialTheme = () => {
  const storedTheme = readStoredTheme();
  const initialTheme = storedTheme || getSystemTheme();
  getRoot().setAttribute("data-theme", initialTheme);
  updateToggleText();
};

const handleThemeToggle = () => {
  applyTheme(getNextTheme());
};

const bindThemeToggle = () => {
  const toggle = getThemeToggle();
  if (!toggle) return;
  toggle.addEventListener("click", handleThemeToggle);
};

const closeDropdown = (dropdown) => {
  dropdown.classList.remove("is-open");
};

const openDropdown = (dropdown) => {
  dropdown.classList.add("is-open");
};

const toggleDropdown = (dropdown) => {
  const isOpen = dropdown.classList.contains("is-open");
  if (isOpen) return closeDropdown(dropdown);
  closeAllDropdowns();
  openDropdown(dropdown);
};

const closeAllDropdowns = () => {
  getDropdowns().forEach(closeDropdown);
};

const handleDropdownToggle = (dropdown) => {
  toggleDropdown(dropdown);
};

const bindDropdown = (dropdown) => {
  const button = qs("[data-dropdown-toggle]", dropdown);
  if (!button) return;
  button.addEventListener("click", () => handleDropdownToggle(dropdown));
};

const bindDropdowns = () => {
  getDropdowns().forEach(bindDropdown);
};

const handleDocumentClick = (event) => {
  const clickedInsideDropdown = event.target.closest("[data-dropdown]");
  if (clickedInsideDropdown) return;
  closeAllDropdowns();
};

const bindDocumentClick = () => {
  document.addEventListener("click", handleDocumentClick);
};

const initBase = () => {
  setInitialTheme();
  bindThemeToggle();
  bindDropdowns();
  bindDocumentClick();
};

document.addEventListener("DOMContentLoaded", initBase);