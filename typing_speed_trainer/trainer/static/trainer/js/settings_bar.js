import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class SettingsBar extends Broker {
  constructor() {
    super();

    this.settingsBar = document.querySelector(".settings-bar");
    this.textField = document.querySelector(".text-field");
    this.hiddenInput = document.querySelector(".input-text");
    this.startTrainerButton = document.querySelector(".start-typing-trainer");
    this.timeSelect = document.querySelector("select");

    this.startTrainerButton.addEventListener("click", () =>
      this.typingTrainerStarted()
    );
    this.hiddenInput.addEventListener("keydown", () =>
      this.typingTrainerStarted()
    );
  }

  setup() {
    this.showSettingsBar();
  }

  typingTrainerStarted() {
    this.setTotalTime();
    this.hideSettingsBar();
    this.notify("typingTrainerStarted");
  }

  setTotalTime() {
    storage.totalTime =
      this.timeSelect.options[this.timeSelect.selectedIndex].value;
  }

  showSettingsBar() {
    this.settingsBar.style.display = "block";
  }

  hideSettingsBar() {
    this.settingsBar.style.display = "none";
  }
}
