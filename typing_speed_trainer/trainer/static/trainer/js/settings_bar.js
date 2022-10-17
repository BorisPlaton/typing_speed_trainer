import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class SettingsBar extends Broker {
  constructor() {
    super();

    this.settingsBar = document.querySelector(".settings-bar");
    this.hiddenInput = document.querySelector(".input-text");
    this.startTrainerButton = document.querySelector(".start-typing-trainer");
    this.textLanguage = document.querySelector(".select-text-language");
    this.typingTrainerStarted = this.typingTrainerStarted.bind(this);
  }

  setup() {
    this.setEventListeners();
    this.showSettingsBar();
    this.languageSelected();
  }

  typingTrainerStarted() {
    this.setTotalTime();
    this.hideSettingsBar();
    this.hiddenInput.focus();
  }

  setTotalTime() {
    storage.totalTime = 5;
  }

  showSettingsBar() {
    this.settingsBar.style.display = "flex";
  }

  hideSettingsBar() {
    this.settingsBar.style.display = "none";
  }

  languageSelected() {
    this.notify("languageChanged", this.textLanguage.value);
  }

  setEventListeners() {
    this.startTrainerButton.addEventListener("click", () => {
      this.typingTrainerStarted();
      this.notify("typingTrainerStarted");
    });
    this.textLanguage.addEventListener("change", () => this.languageSelected());
  }
}
