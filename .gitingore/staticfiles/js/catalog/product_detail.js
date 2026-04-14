(() => {
  const pageQuery = (selector, scope = document) => scope.querySelector(selector);

  const getReviewForm = () => pageQuery("#reviewForm");
  const getProductId = (form) => form.dataset.productId;
  const getRatingField = () => pageQuery('[name="rating"]');
  const getCommentField = () => pageQuery('[name="comment"]');
  const getCsrfToken = () => pageQuery('[name="csrfmiddlewaretoken"]').value;

  const getMessageBox = () => pageQuery("#reviewMessage");
  const getAvgRating = () => pageQuery("#avgRating");
  const getReviewCount = () => pageQuery("#reviewCount");
  const getReviewsList = () => pageQuery("#reviewsList");
  const getNoReviewsText = () => pageQuery("#noReviewsText");

  const getReviewCard = (userId) => pageQuery(`#review-${userId}`);

  const setText = (node, text) => {
    if (node) node.textContent = text;
  };

  const buildPayload = () => ({
    rating: getRatingField().value,
    comment: getCommentField().value.trim()
  });

  const buildHeaders = () => ({
    "Content-Type": "application/json",
    "X-CSRFToken": getCsrfToken()
  });

  const setMessage = (text) => {
    setText(getMessageBox(), text);
  };

  const updateSummary = (data) => {
    setText(getAvgRating(), data.average_rating);
    setText(getReviewCount(), data.review_count);
  };

  const removeNoReviewsText = () => {
    const node = getNoReviewsText();
    if (node) node.remove();
  };

  const createElement = (tag, text = "", className = "") => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (className) el.className = className;
    return el;
  };

  const createReviewCard = (data) => {
    const card = createElement("article", "", "review-card content-card");
    card.id = `review-${data.user_id}`;

    const userLine = createElement("p");
    const strong = createElement("strong", data.username);
    userLine.appendChild(strong);

    const ratingLine = createElement("p");
    ratingLine.appendChild(document.createTextNode("Rating: "));
    ratingLine.appendChild(createElement("span", String(data.your_rating), "review-rating"));
    ratingLine.appendChild(document.createTextNode("/5"));

    const commentLine = createElement("p", data.your_comment, "review-comment");
    const timeLine = createElement("p");
    timeLine.appendChild(createElement("small", "Just now"));

    card.appendChild(userLine);
    card.appendChild(ratingLine);
    card.appendChild(commentLine);
    card.appendChild(timeLine);

    return card;
  };

  const updateReviewCard = (card, data) => {
    setText(pageQuery(".review-rating", card), data.your_rating);
    setText(pageQuery(".review-comment", card), data.your_comment);
  };

  const insertOrUpdateReviewCard = (data) => {
  const existingCard = getReviewCard(data.user_id);
  const reviewsList = getReviewsList();

  if (existingCard) {
    updateReviewCard(existingCard, data);
    reviewsList.prepend(existingCard);
    return;
  }

  const newCard = createReviewCard(data);
  reviewsList.prepend(newCard);
};

  const resetReviewForm = () => {
    const form = getReviewForm();
    if (!form) return;
    form.reset();
    getRatingField().value = "";
    getCommentField().value = "";
  };

  const handleSuccess = (data) => {
    updateSummary(data);
    setMessage(data.message);
    removeNoReviewsText();
    insertOrUpdateReviewCard(data);
    resetReviewForm();
  };

  const handleError = (data) => {
    setMessage(data.message || "Something went wrong.");
  };

  const postReview = async (productId) => {
    const response = await fetch(`/reviews/ajax/${productId}/`, {
      method: "POST",
      headers: buildHeaders(),
      body: JSON.stringify(buildPayload())
    });

    return response.json();
  };

  const submitReview = async (event) => {
    event.preventDefault();

    try {
      const form = getReviewForm();
      const data = await postReview(getProductId(form));
      if (!data.success) return handleError(data);
      handleSuccess(data);
    } catch (error) {
      setMessage("Error submitting review.");
    }
  };

  const bindReviewForm = () => {
    const form = getReviewForm();
    if (!form) return;
    form.addEventListener("submit", submitReview);
  };

  document.addEventListener("DOMContentLoaded", bindReviewForm);
})();