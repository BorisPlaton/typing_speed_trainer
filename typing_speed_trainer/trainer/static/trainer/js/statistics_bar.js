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
    this.createEventListeners();
    this.configureStatisticsBar();
    this.showStatisticsBar();
    this.startTimer().then(() => {
      this.typingTrainerStopped();
    });
  }

  typingTrainerStopped() {
    this.stopTimer();
    this.removeEventListeners();
    this.hideStatisticsBar();
    this.notify("typingTrainerStopped");
  }

  startTimer() {
    return new Promise((resolve, reject) => {
      this.timer = setInterval(() => {
        if (this.leftTime.innerHTML == 0) {
          this.stopTimer();
        }
        this.leftTime.innerHTML--;
      }, 1000);

      this.stopTimer = () => {
        clearInterval(this.timer);
        resolve();
      };
      console.log("After interval");
    });
  }

  configureStatisticsBar() {
    this.leftTime.innerHTML = storage.executionTime;
    this.wordsAmount.innerHTML = storage.correctWordsAmount;
    this.typoAmount.innerHTML = storage.typoAmount;
  }

  showStatisticsBar() {
    this.statisticsBar.style.display = "block";
  }

  hideStatisticsBar() {
    this.statisticsBar.style.display = "none";
  }

  createEvents() {
    this.funcTypingTrainerStopped = () => {
      this.stopTimer();
      this.typingTrainerStopped.call(this);
    };
  }

  createEventListeners() {
    this.stopTypingButton.addEventListener(
      "click",
      this.funcTypingTrainerStopped
    );
  }

  removeEventListeners() {
    this.stopTypingButton.removeEventListener(
      "click",
      this.funcTypingTrainerStopped
    );
  }
}
