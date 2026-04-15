const qs = (selector, scope = document) => scope.querySelector(selector);

const focusRegisterInput = () => {
  const input = qs('input[name="username"]');
  if (input) input.focus();
};

document.addEventListener("DOMContentLoaded", focusRegisterInput);