/* base.js
   Global site script.
   Handles theme persistence, dark/light mode toggle,
   navbar dropdown behavior, and mobile navigation.
*/

const qs = (selector, scope = document) => scope.querySelector(selector);
const qsa = (selector, scope = document) => [...scope.querySelectorAll(selector)];

const MOBILE_BREAKPOINT = 900;

const getRoot = () => document.documentElement;
const getThemeToggle = () => qs("[data-theme-toggle]");
const getNavToggle = () => qs("[data-nav-toggle]");
const getNavMenu = () => qs("[data-nav-menu]");
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
    return null;
  }
};

const getSystemTheme = () => {
  if (typeof window.matchMedia !== "function") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

const getCurrentTheme = () => getRoot().getAttribute("data-theme") || "light";
const getNextTheme = () => (getCurrentTheme() === "dark" ? "light" : "dark");

const updateToggleText = () => {
  const toggle = getThemeToggle();
  if (!toggle) return;
  toggle.textContent = getCurrentTheme() === "dark" ? "Light Mode" : "Dark Mode";
};

const applyTheme = (theme, shouldPersist = true) => {
  getRoot().setAttribute("data-theme", theme);
  if (shouldPersist) saveTheme(theme);
  updateToggleText();
};

const setInitialTheme = () => {
  const storedTheme = readStoredTheme();
  applyTheme(storedTheme || getSystemTheme(), false);
};

const handleThemeToggle = () => {
  applyTheme(getNextTheme());
};

const closeDropdown = (dropdown) => {
  dropdown.classList.remove("is-open");
};

const openDropdown = (dropdown) => {
  dropdown.classList.add("is-open");
};

const closeAllDropdowns = (exceptDropdown = null) => {
  getDropdowns().forEach((dropdown) => {
    if (dropdown === exceptDropdown) return;
    closeDropdown(dropdown);
  });
};

const toggleDropdown = (dropdown) => {
  const willOpen = !dropdown.classList.contains("is-open");
  closeAllDropdowns(dropdown);
  if (!willOpen) return closeDropdown(dropdown);
  openDropdown(dropdown);
};

const closeMobileMenu = () => {
  const navMenu = getNavMenu();
  const navToggle = getNavToggle();

  if (!navMenu || !navToggle) return;

  navMenu.classList.remove("is-open");
  navToggle.classList.remove("is-open");
  navToggle.setAttribute("aria-expanded", "false");
};

const toggleMobileMenu = () => {
  const navMenu = getNavMenu();
  const navToggle = getNavToggle();

  if (!navMenu || !navToggle) return;

  const isOpen = navMenu.classList.toggle("is-open");
  navToggle.classList.toggle("is-open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));

  if (!isOpen) closeAllDropdowns();
};

const handleDropdownToggle = (event, dropdown) => {
  event.preventDefault();
  event.stopPropagation();
  toggleDropdown(dropdown);
};

const handleDocumentClick = (event) => {
  const clickedInsideDropdown = event.target.closest("[data-dropdown]");
  const clickedNavToggle = event.target.closest("[data-nav-toggle]");
  const clickedInsideMenu = event.target.closest("[data-nav-menu]");

  if (!clickedInsideDropdown) closeAllDropdowns();

  if (window.innerWidth > MOBILE_BREAKPOINT) return;
  if (clickedNavToggle || clickedInsideMenu) return;
  closeMobileMenu();
};

const handleWindowResize = () => {
  if (window.innerWidth > MOBILE_BREAKPOINT) {
    closeMobileMenu();
    closeAllDropdowns();
  }
};

const handleDocumentKeydown = (event) => {
  if (event.key !== "Escape") return;
  closeAllDropdowns();
  closeMobileMenu();
};

const bindThemeToggle = () => {
  const toggle = getThemeToggle();
  if (!toggle) return;
  toggle.addEventListener("click", handleThemeToggle);
};

const bindNavToggle = () => {
  const navToggle = getNavToggle();
  if (!navToggle) return;
  navToggle.addEventListener("click", toggleMobileMenu);
};

const bindDropdown = (dropdown) => {
  const button = qs("[data-dropdown-toggle]", dropdown);
  if (!button) return;

  button.addEventListener("click", (event) => {
    handleDropdownToggle(event, dropdown);
  });
};

const bindDropdowns = () => {
  getDropdowns().forEach(bindDropdown);
};

const bindDocumentEvents = () => {
  document.addEventListener("click", handleDocumentClick);
  document.addEventListener("keydown", handleDocumentKeydown);
};

const bindWindowEvents = () => {
  window.addEventListener("resize", handleWindowResize);
};

const initBase = () => {
  setInitialTheme();
  bindThemeToggle();
  bindNavToggle();
  bindDropdowns();
  bindDocumentEvents();
  bindWindowEvents();
};

document.addEventListener("DOMContentLoaded", initBase);