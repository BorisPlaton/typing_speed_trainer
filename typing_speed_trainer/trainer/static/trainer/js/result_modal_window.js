import storage from "./data_storage.js";
import { Subscriber, Publisher } from "./mediator.js";

export default class ResultModalWindow extends Subscriber {
  /**
   * @param {Publisher} publisher
   */
  constructor(publisher) {
    super(publisher);

    this.modalWindow = document.querySelector(".result-modal");
    this.closeButton = document.querySelector(".close-result-modal");
    this.startAgainButton = document.querySelector(".start-trainer-again");

    this.wpm = this.modalWindow.querySelector(".modal-wpm");
    this.correctWordsAmount = this.modalWindow.querySelector(
      ".modal-correct-words-amount"
    );
    this.invalidWordsAmount = this.modalWindow.querySelector(
      ".modal-invalid-words-amount"
    );
    this.correctKeystrokes = this.modalWindow.querySelector(
      ".modal-keystrokes .correct"
    );
    this.invalidKeystrokes = this.modalWindow.querySelector(
      ".modal-keystrokes .invalid"
    );
    this.summaryKeystrokes = this.modalWindow.querySelector(
      ".modal-keystrokes .summary"
    );
    this.keystrokesAccuracy = this.modalWindow.querySelector(".modal-accuracy");

    this.closeButton.addEventListener("click", () => {
      this.hideWindow();
    });

    this.startAgainButton.addEventListener("click", () => {
      this.hideWindow();
      this.notify("typingTrainerStarted");
    });
  }

  show() {
    this.setStatisticsValues();
    this.showWindow();
  }

  setStatisticsValues() {
    const data = storage.typingStatistics;
    this.wpm.innerHTML = data.wpm;
    this.correctWordsAmount.innerHTML = data.correctWordsAmount;
    this.invalidWordsAmount.innerHTML = data.invalidWordsAmount;
    this.correctKeystrokes.innerHTML = data.correctKeystrokes;
    this.invalidKeystrokes.innerHTML = data.invalidKeystrokes;
    this.summaryKeystrokes.innerHTML = data.summaryKeystrokes;
    this.keystrokesAccuracy.innerHTML = data.typingAccuracy + "%";
  }

  showWindow() {
    this.modalWindow.style.display = "flex";
  }

  hideWindow() {
    this.modalWindow.style.display = "none";
  }
}
