import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class TypingTrainer extends Broker {
  constructor() {
    super();

    this.statisticsBar = document.querySelector(".statistics-bar");
    this.stopTypingButton = document.querySelector(".stop-typing-trainer");
    this.leftTime = document.querySelector(".left-time");
    this.hiddenInput = document.querySelector(".input-text");
    this.wordsAmount = document.querySelector(".words-amount");
    this.typoAmount = document.querySelector(".typo-amount");

    this.createEvents();
  }

  setup() {
    this.configureStatisticsBar();
    this.showStatisticsBar();
    this.createEventListeners();
  }

  typingTrainerStopped() {
    this.removeEventListeners();
    this.hideStatisticsBar();
    this.notify("typingTrainerStopped");
  }

  configureStatisticsBar() {
    this.leftTime.innerHTML = storage.executionTime;
    this.wordsAmount.innerHTML = storage.correctWordsAmount;
    this.typoAmount.innerHTML = storage.typoAmount;
  }

  analyzeInputChar() {}

  showStatisticsBar() {
    this.statisticsBar.style.display = "block";
  }

  hideStatisticsBar() {
    this.statisticsBar.style.display = "none";
  }

  createEvents() {
    this.funcTypingTrainerStopped = () => this.typingTrainerStopped.call(this);
    this.funcAnalyzeInputChar = () => this.analyzeInputChar.call(this);
  }

  createEventListeners() {
    this.stopTypingButton.addEventListener(
      "click",
      this.funcTypingTrainerStopped
    );
    this.hiddenInput.addEventListener("keyup", this.funcAnalyzeInputChar);
  }

  removeEventListeners() {
    this.stopTypingButton.removeEventListener(
      "click",
      this.funcTypingTrainerStopped
    );
  }
}
