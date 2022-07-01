import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class SettingsBar extends Broker {
  constructor() {
    super();

    this.settingsBar = document.querySelector(".settings-bar");
    this.hiddenInput = document.querySelector(".input-text");
    this.startTrainerButton = document.querySelector(".start-typing-trainer");
    this.typingTrainerStarted = this.typingTrainerStarted.bind(this);
  }

  setup() {
    this.hiddenInput.style.opacity = "1";
    this.setEventListeners();
    this.showSettingsBar();
  }

  typingTrainerStarted() {
    this.removeEventListeners();
    this.setTotalTime();
    this.hideSettingsBar();
    this.hiddenInput.style.opacity = "0";
    this.notify("typingTrainerStarted");
  }

  setTotalTime() {
    storage.totalTime = 60;
  }

  showSettingsBar() {
    this.settingsBar.style.display = "flex";
  }

  hideSettingsBar() {
    this.settingsBar.style.display = "none";
  }

  removeEventListeners() {
    this.startTrainerButton.removeEventListener(
      "click",
      this.typingTrainerStarted
    );
    this.hiddenInput.removeEventListener("keydown", this.typingTrainerStarted);
  }

  setEventListeners() {
    this.startTrainerButton.addEventListener(
      "click",
      this.typingTrainerStarted
    );
    this.hiddenInput.addEventListener("keydown", this.typingTrainerStarted);
  }
}
