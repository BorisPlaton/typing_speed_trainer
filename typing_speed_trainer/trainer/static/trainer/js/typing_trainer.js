import EventListener from "./broker";

export default class TypingTrainer extends EventListener {
  constructor() {
    this.statisticsBar = document.querySelector(".statistics-bar");
    this.stopTyppingButton = document.querySelector(".stop-typping-trainer");
    this.leftTime = document.querySelector(".left-time");
    this.wordsAmount = document.querySelector(".words-amount");
    this.typoAmount = document.querySelector(".typo-amount");
  }

  setup() {
    this.showStatisticsBar();
    this.createEventListeners();
  }

  createEventListeners() {
    this.stopTyppingButton.addEventListener("click", this.typingTrainerStopped);
  }

  removeEventListeners() {
    this.stopTyppingButton.removeEventListener(
      "click",
      this.typingTrainerStopped
    );
  }

  typingTrainerStopped() {
    this.removeEventListeners();
  }

  showStatisticsBar() {
    this.statisticsBar.display = "block";
  }

  hideStatisticsBar() {
    this.statisticsBar.display = "none";
  }
}
