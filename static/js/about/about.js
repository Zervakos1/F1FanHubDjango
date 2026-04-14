/* about.js
   Handles the About page image carousel.
   Supports previous/next navigation, dot navigation, and automatic slide rotation.
*/


(() => {
  const aboutQuery = (selector, scope = document) => scope.querySelector(selector);
  const aboutQueryAll = (selector, scope = document) => [...scope.querySelectorAll(selector)];

  const getCarousel = () => aboutQuery("[data-carousel]");
  const getSlides = (carousel) => aboutQueryAll("[data-slide]", carousel);
  const getDots = (carousel) => aboutQueryAll("[data-dot]", carousel);
  const getPrevButton = (carousel) => aboutQuery("[data-carousel-prev]", carousel);
  const getNextButton = (carousel) => aboutQuery("[data-carousel-next]", carousel);

  const getActiveIndex = (slides) => {
    const index = slides.findIndex((slide) => slide.classList.contains("is-active"));
    return index >= 0 ? index : 0;
  };

  const setActiveState = (items, activeIndex) => {
    items.forEach((item, index) => {
      item.classList.toggle("is-active", index === activeIndex);
    });
  };

  const showSlide = (carousel, index) => {
    const slides = getSlides(carousel);
    const dots = getDots(carousel);

    if (!slides.length) return;

    setActiveState(slides, index);
    setActiveState(dots, index);
  };

  const showNextSlide = (carousel) => {
    const slides = getSlides(carousel);
    const currentIndex = getActiveIndex(slides);
    const nextIndex = (currentIndex + 1) % slides.length;
    showSlide(carousel, nextIndex);
  };

  const showPrevSlide = (carousel) => {
    const slides = getSlides(carousel);
    const currentIndex = getActiveIndex(slides);
    const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(carousel, prevIndex);
  };

  const handlePrevClick = (carousel) => {
    showPrevSlide(carousel);
  };

  const handleNextClick = (carousel) => {
    showNextSlide(carousel);
  };

  const handleDotClick = (carousel, dot) => {
    const dots = getDots(carousel);
    const index = dots.indexOf(dot);
    if (index < 0) return;
    showSlide(carousel, index);
  };

  const bindPrevButton = (carousel) => {
    const button = getPrevButton(carousel);
    if (!button) return;
    button.addEventListener("click", () => handlePrevClick(carousel));
  };

  const bindNextButton = (carousel) => {
    const button = getNextButton(carousel);
    if (!button) return;
    button.addEventListener("click", () => handleNextClick(carousel));
  };

  const bindDots = (carousel) => {
    getDots(carousel).forEach((dot) => {
      dot.addEventListener("click", () => handleDotClick(carousel, dot));
    });
  };

  const startCarouselAutoPlay = (carousel) => {
    window.setInterval(() => showNextSlide(carousel), 5000);
  };

  const initAboutPage = () => {
    const carousel = getCarousel();
    if (!carousel) return;

    showSlide(carousel, 0);
    bindPrevButton(carousel);
    bindNextButton(carousel);
    bindDots(carousel);
    startCarouselAutoPlay(carousel);
  };

  document.addEventListener("DOMContentLoaded", initAboutPage);
})();