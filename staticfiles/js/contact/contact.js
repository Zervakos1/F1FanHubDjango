(() => {
  const contactQuery = (selector, scope = document) => scope.querySelector(selector);
  const contactQueryAll = (selector, scope = document) => [...scope.querySelectorAll(selector)];

  const getForm = () => contactQuery("[data-contact-form]");
  const getSubmitButton = () => contactQuery("[data-submit-button]");
  const getConfirmationBox = () => contactQuery("[data-confirmation-box]");
  const getFields = () => contactQueryAll("input, textarea", getForm());

  const getField = (name) => contactQuery(`[name="${name}"]`, getForm());
  const getFieldValue = (name) => {
    const field = getField(name);
    return field ? field.value.trim() : "";
  };

  const getErrorNode = (name) => contactQuery(`[data-error-for="${name}"]`);
  const getConfirmNode = (name) => contactQuery(`[data-confirm="${name}"]`);

  const setText = (node, text) => {
    if (node) node.textContent = text;
  };

  const isEmailValid = (value) => /\S+@\S+\.\S+/.test(value);
  const isFilled = (value) => value.length > 0;

  const clearError = (fieldName) => setText(getErrorNode(fieldName), "");
  const showError = (fieldName, message) => setText(getErrorNode(fieldName), message);

  const markFieldState = (field, isValid) => {
    if (!field) return;
    field.classList.toggle("invalid-field", !isValid);
  };

  const validateName = () => {
    const field = getField("name");
    const value = getFieldValue("name");
    const valid = isFilled(value);

    if (valid) clearError("name");
    else showError("name", "Please enter your name.");

    markFieldState(field, valid);
    return valid;
  };

  const validateEmail = () => {
    const field = getField("email");
    const value = getFieldValue("email");
    const valid = isEmailValid(value);

    if (valid) clearError("email");
    else showError("email", "Please enter a valid email.");

    markFieldState(field, valid);
    return valid;
  };

  const validateSubject = () => {
    const field = getField("subject");
    const value = getFieldValue("subject");
    const valid = isFilled(value);

    if (valid) clearError("subject");
    else showError("subject", "Subject is required.");

    markFieldState(field, valid);
    return valid;
  };

  const validateMessage = () => {
    const field = getField("message");
    const value = getFieldValue("message");
    const valid = isFilled(value);

    if (valid) clearError("message");
    else showError("message", "Please enter your message.");

    markFieldState(field, valid);
    return valid;
  };

  const validateForm = () => {
    const checks = [
      validateName(),
      validateEmail(),
      validateSubject(),
      validateMessage()
    ];

    return checks.every(Boolean);
  };

const hasValue = (name) => getFieldValue(name).length > 0;

  const updateSubmitState = () => {
    const button = getSubmitButton();
    if (!button) return;

    const ready =
      hasValue("name") &&
      hasValue("email") &&
      hasValue("subject") &&
      hasValue("message") &&
      isEmailValid(getFieldValue("email"));

    button.disabled = !ready;
};

  const fillConfirmation = () => {
    setText(getConfirmNode("name"), getFieldValue("name"));
    setText(getConfirmNode("email"), getFieldValue("email"));
    setText(getConfirmNode("subject"), getFieldValue("subject"));
    setText(getConfirmNode("message"), getFieldValue("message"));
  };

  const showConfirmation = () => {
    const box = getConfirmationBox();
    if (box) box.classList.remove("hidden");
  };

  const resetFormState = () => {
    const form = getForm();
    if (!form) return;

    form.reset();
    getFields().forEach((field) => field.classList.remove("invalid-field"));
    ["name", "email", "subject", "message"].forEach(clearError);
    updateSubmitState();
  };

  const handleInput = () => updateSubmitState();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    fillConfirmation();
    showConfirmation();
    resetFormState();
  };

  const bindFieldEvents = () => {
    getFields().forEach((field) => field.addEventListener("input", handleInput));
  };

  const bindFormSubmit = () => {
    const form = getForm();
    if (!form) return;
    form.addEventListener("submit", handleSubmit);
  };

  const initContactPage = () => {
    if (!getForm()) return;
    bindFieldEvents();
    bindFormSubmit();
    updateSubmitState();
  };

  document.addEventListener("DOMContentLoaded", initContactPage);
})();