import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class StatisticsBar extends Broker {
  constructor() {
    super();

    this.statisticsBar = document.querySelector(".statistics-bar");
    this.stopTypingButton = document.querySelector(".stop-typing-trainer");
    this.leftTime = document.querySelector(".left-time");
    this.hiddenInput = document.querySelector(".input-text");
    this.wordsAmount = document.querySelector(".words-amount");
    this.typoAmount = document.querySelector(".typo-amount");

    this.stopTypingButton.addEventListener("click", () => this.stopTimer());
  }

  setup() {
    this.configureStatisticsBar();
    this.showStatisticsBar();
    this.startTimer().then(() => {
      this.typingTrainerStopped();
    });
  }

  typingTrainerStopped() {
    this.hideStatisticsBar();
    this.notify("typingTrainerStopped");
  }

  startTimer() {
    return new Promise((resolve, reject) => {
      this.timer = setInterval(() => {
        if (this.leftTime.innerHTML == 1) {
          this.stopTimer();
        }
        storage.executionTime++;
        this.leftTime.innerHTML--;
      }, 1000);

      this.stopTimer = () => {
        clearInterval(this.timer);
        resolve();
      };
    });
  }

  configureStatisticsBar() {
    this.leftTime.innerHTML = storage.totalTime;
    this.wordsAmount.innerHTML = storage.correctWordsAmount;
    this.typoAmount.innerHTML = storage.typoAmount;
  }

  increaseCorrectWord() {
    this.wordsAmount.innerHTML++;
  }

  increaseWrongChar() {
    this.typoAmount.innerHTML++;
  }

  showStatisticsBar() {
    this.statisticsBar.style.display = "block";
  }

  hideStatisticsBar() {
    this.statisticsBar.style.display = "none";
  }
}
