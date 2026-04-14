/* profile.js
   Improves the profile page user experience.
   Automatically focuses the first editable profile field when the page loads.
*/

const qs = (selector, scope = document) => scope.querySelector(selector);

const getProfileForm = () => qs(".profile-form");
const getFirstProfileInput = () => qs('input[name="username"]', getProfileForm());

const focusFirstProfileInput = () => {
  const input = getFirstProfileInput();
  if (input) input.focus();
};

document.addEventListener("DOMContentLoaded", focusFirstProfileInput);