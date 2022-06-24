import storage from "./data_storage.js";

export default class ResultModalWindow {
  constructor() {
    this.modalWindow = document.querySelector(".result-modal");
    this.closeButton = document.querySelector(".close-result-modal");
    this.timeAmount = document.querySelector(".modal-time");
    this.typoAmount = document.querySelector(".modal-typo-amount");
    this.wpm = document.querySelector(".modal-wpm");

    this.closeButton.addEventListener("click", () => {
      this.hideWindow();
    });
  }

  show() {
    this.setStatisticsValues();
    this.showWindow();
    storage.cleanUpStorage();
  }

  setStatisticsValues() {
    this.typoAmount.innerHTML = storage.typoAmount;
    this.wpm.innerHTML = storage.correctWordsAmount;
    this.timeAmount.innerHTML = storage.executionTime + "c";
  }

  showWindow() {
    this.modalWindow.style.display = "flex";
  }

  hideWindow() {
    this.modalWindow.style.display = "none";
  }
}
