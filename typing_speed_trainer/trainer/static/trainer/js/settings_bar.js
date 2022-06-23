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

    this.createEvents();
  }

  setup() {
    this.createEventListeners();
    this.showSettingsBar();
  }

  createEvents() {
    this._typingTrainerStarted = () => this.typingTrainerStarted.call(this);
  }

  createEventListeners() {
    this.startTrainerButton.addEventListener(
      "click",
      this._typingTrainerStarted
    );
    this.hiddenInput.addEventListener("keydown", this._typingTrainerStarted);
  }

  removeEventListeners() {
    this.startTrainerButton.removeEventListener(
      "click",
      this._typingTrainerStarted
    );
    this.hiddenInput.removeEventListener("keydown", this._typingTrainerStarted);
  }

  typingTrainerStarted() {
    this.removeEventListeners();
    this.setExecutionTime();
    this.hideSettingsBar();
    this.notify("typingTrainerStarted");
  }

  setExecutionTime() {
    storage.executionTime =
      this.timeSelect.options[this.timeSelect.selectedIndex].value;
  }

  showSettingsBar() {
    this.settingsBar.style.display = "block";
  }

  hideSettingsBar() {
    this.settingsBar.style.display = "none";
  }
}
