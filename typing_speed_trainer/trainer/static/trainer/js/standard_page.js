import EventListener from "./broker";

export default class StandardPage extends EventListener {
  constructor() {
    this.settingsBar = document.querySelector(".settings-bar");
    this.textField = document.querySelector(".text-field");
    this.hiddenInput = document.querySelector(".input-text");
    this.startTrainerButton = document.querySelector(".start-typing-trainer");
  }

  setup() {
    this.createEventListeners();
    this.showSettingsBar();
  }

  createEventListeners() {
    this.startTrainerButton.addEventListener(
      "click",
      this.typingTrainerStarted
    );
    this.hiddenInput.addEventListener(
      "keydown",
      this.typingTrainerStarted
    );
  }

  removeEventListeners() {
    this.startTrainerButton.removeEventListener(
      "click",
      this.typingTrainerStarted
    );
    this.hiddenInput.removeEventListener(
      "keydown",
      this.typingTrainerStarted
    );
  }

  typingTrainerStarted() {
    this.removeEventListeners();
    this.hideSettingsBar();
    this.notify("typingTrainerStarted");
  }

  showSettingsBar() {
    this.settingsBar.display = "block";
  }

  hideSettingsBar() {
    this.settingsBar.display = "none";
  }
}
