const qs = (selector, scope = document) => scope.querySelector(selector);

const focusLoginInput = () => {
  const input = qs('input[name="username"]');
  if (input) input.focus();
};

document.addEventListener("DOMContentLoaded", focusLoginInput);