import { Subscriber, Publisher } from "./publisher.js";
import storage from "./data_storage.js";

export default class StatisticsBar extends Subscriber {
  /**
   * @param {Publisher} publisher
   */
  constructor(publisher) {
    super(publisher);

    this.statisticsBar = document.querySelector(".statistics-bar");
    this.stopTypingButton = document.querySelector(".stop-typing-trainer");
    this.leftTime = document.querySelector(".left-time");
    this.hiddenInput = document.querySelector(".input-text");
    this.wordsAmount = document.querySelector(".words-amount");
    this.typoAmount = document.querySelector(".typo-amount");
    this.correctCharsAmount = document.querySelector(".correct-chars-amount");
    this.stopTypingButton.addEventListener("click", () => this.stopTimer(true));
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
    if (this.isRestarted) {
      this.notify("typingTrainerRestart");
    } else {
      this.notify("typingTrainerStopped");
    }
    this.isRestarted = false;
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

      this.stopTimer = (isRestarted = false) => {
        this.isRestarted = isRestarted;
        clearInterval(this.timer);
        resolve();
      };
    });
  }

  configureStatisticsBar() {
    this.leftTime.innerHTML = storage.totalTime;
    this.wordsAmount.innerHTML = storage.correctWordsAmount;
    this.typoAmount.innerHTML = storage.typoAmount;
    this.correctCharsAmount.innerHTML = storage.correctCharsAmount;
  }

  increaseCorrectChars() {
    this.correctCharsAmount.innerHTML++;
  }

  decreaseCorrectChars() {
    if (+this.correctCharsAmount.innerHTML) {
      this.correctCharsAmount.innerHTML--;
    }
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
