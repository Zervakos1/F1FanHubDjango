(() => {
  const pageQuery = (selector, scope = document) => scope.querySelector(selector);
  const pageQueryAll = (selector, scope = document) => [...scope.querySelectorAll(selector)];

  const getWidget = () => pageQuery("[data-race-widget]");
  const getLoading = () => pageQuery("[data-race-loading]");
  const getContent = () => pageQuery("[data-race-content]");
  const getError = () => pageQuery("[data-race-error]");

  const getRaceNameNode = () => pageQuery("[data-race-name]");
  const getRaceCircuitNode = () => pageQuery("[data-race-circuit]");
  const getRaceLocationNode = () => pageQuery("[data-race-location]");
  const getRaceDateNode = () => pageQuery("[data-race-date]");
  const getRaceTimeNode = () => pageQuery("[data-race-time]");

  const getCarousels = () => pageQueryAll("[data-home-carousel]");
  const getTrack = (carousel) => pageQuery("[data-carousel-track]", carousel);
  const getPrevButton = (carousel) => pageQuery("[data-carousel-prev]", carousel);
  const getNextButton = (carousel) => pageQuery("[data-carousel-next]", carousel);

  const setText = (node, text) => {
    if (node) node.textContent = text;
  };

  const showNode = (node) => {
    if (node) node.classList.remove("hidden");
  };

  const hideNode = (node) => {
    if (node) node.classList.add("hidden");
  };

  const getRaceApiUrl = () => "https://api.jolpi.ca/ergast/f1/current/next.json";

  const getRaceObject = (data) => {
    const raceTable = data?.MRData?.RaceTable;
    const races = raceTable?.Races || [];
    return races.length ? races[0] : null;
  };

  const formatLocation = (race) => {
    const locality = race?.Circuit?.Location?.locality || "Unknown city";
    const country = race?.Circuit?.Location?.country || "Unknown country";
    return `${locality}, ${country}`;
  };

  const formatTime = (time) => {
    if (!time) return "TBA";
    return time.replace("Z", " UTC");
  };

  const fillRaceCard = (race) => {
    setText(getRaceNameNode(), race?.raceName || "Next Race");
    setText(getRaceCircuitNode(), race?.Circuit?.circuitName || "Unknown circuit");
    setText(getRaceLocationNode(), formatLocation(race));
    setText(getRaceDateNode(), race?.date || "TBA");
    setText(getRaceTimeNode(), formatTime(race?.time));
  };

  const showRaceSuccess = (race) => {
    fillRaceCard(race);
    hideNode(getLoading());
    hideNode(getError());
    showNode(getContent());
  };

  const showRaceError = () => {
    hideNode(getLoading());
    hideNode(getContent());
    showNode(getError());
  };

  const fetchNextRace = async () => {
    try {
      const response = await fetch(getRaceApiUrl());
      if (!response.ok) {
        showRaceError();
        return;
      }

      const data = await response.json();
      const race = getRaceObject(data);

      if (!race) {
        showRaceError();
        return;
      }

      showRaceSuccess(race);
    } catch (error) {
      showRaceError();
    }
  };

  const getScrollAmount = (track) => Math.max(track.clientWidth * 0.8, 260);

  const scrollTrackNext = (carousel) => {
    const track = getTrack(carousel);
    if (!track) return;
    track.scrollBy({ left: getScrollAmount(track), behavior: "smooth" });
  };

  const scrollTrackPrev = (carousel) => {
    const track = getTrack(carousel);
    if (!track) return;
    track.scrollBy({ left: -getScrollAmount(track), behavior: "smooth" });
  };

  const bindCarousel = (carousel) => {
    const track = getTrack(carousel);
    const prevButton = getPrevButton(carousel);
    const nextButton = getNextButton(carousel);

    if (!track || !prevButton || !nextButton) return;

    prevButton.addEventListener("click", () => scrollTrackPrev(carousel));
    nextButton.addEventListener("click", () => scrollTrackNext(carousel));
  };

  const bindCarousels = () => {
    getCarousels().forEach(bindCarousel);
  };

  const initVisitorDashboard = () => {
    if (getWidget()) fetchNextRace();
    bindCarousels();
  };

  document.addEventListener("DOMContentLoaded", initVisitorDashboard);
})();