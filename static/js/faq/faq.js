/* faq.js
   Handles FAQ accordion behavior.
   Expands one answer at a time and updates ARIA state for accessibility.
*/

(() => {
  const faqQuery = (selector, scope = document) => scope.querySelector(selector);
  const faqQueryAll = (selector, scope = document) => [...scope.querySelectorAll(selector)];

  const getFaqItems = () => faqQueryAll(".faq-item");
  const getQuestion = (item) => faqQuery("[data-faq-toggle]", item);
  const getAnswer = (item) => faqQuery("[data-faq-answer]", item);

  const setExpandedState = (button, expanded) => {
    if (!button) return;
    button.setAttribute("aria-expanded", String(expanded));
  };

  const showAnswer = (answer) => {
    if (answer) answer.classList.remove("hidden");
  };

  const hideAnswer = (answer) => {
    if (answer) answer.classList.add("hidden");
  };

  const closeItem = (item) => {
    const button = getQuestion(item);
    const answer = getAnswer(item);
    setExpandedState(button, false);
    hideAnswer(answer);
  };

  const openItem = (item) => {
    const button = getQuestion(item);
    const answer = getAnswer(item);
    setExpandedState(button, true);
    showAnswer(answer);
  };

  const isOpen = (item) => {
    const button = getQuestion(item);
    return button ? button.getAttribute("aria-expanded") === "true" : false;
  };

  const closeOtherItems = (currentItem) => {
    getFaqItems().forEach((item) => {
      if (item !== currentItem) closeItem(item);
    });
  };

  const toggleItem = (item) => {
    if (isOpen(item)) {
      closeItem(item);
      return;
    }

    closeOtherItems(item);
    openItem(item);
  };

  const handleQuestionClick = (event) => {
    const item = event.currentTarget.closest(".faq-item");
    if (!item) return;
    toggleItem(item);
  };

  const bindQuestion = (item) => {
    const button = getQuestion(item);
    if (!button) return;
    button.addEventListener("click", handleQuestionClick);
  };

  const bindQuestions = () => {
    getFaqItems().forEach(bindQuestion);
  };

  document.addEventListener("DOMContentLoaded", bindQuestions);
})();