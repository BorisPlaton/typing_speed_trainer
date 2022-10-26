import { Subscriber, Publisher } from "./mediator.js";
import storage from "./data_storage.js";

export default class SettingsBar extends Subscriber {
  /**
   * @param {Publisher} publisher
   */
  constructor(publisher) {
    super(publisher);
    this.settingsBar = document.querySelector(".settings-bar");
    this.hiddenInput = document.querySelector(".input-text");
    this.startTrainerButton = document.querySelector(".start-typing-trainer");
    this.textLanguage = document.querySelector(".select-text-language");
    this.typingTrainerStarted = this.typingTrainerStarted.bind(this);
  }

  setup() {
    this.setEvents();
    this.showSettingsBar();
  }

  typingTrainerStarted() {
    this.setTotalTime();
    this.hideSettingsBar();
    this.hiddenInput.focus();
  }

  setTotalTime() {
    storage.totalTime = 5;
  }

  setEvents() {
    this.startTrainerButton.addEventListener("click", () => {
      this.notify("typingTrainerStarted");
    });
    this.textLanguage.addEventListener("change", () =>
      this.notify("languageChanged", this.textLanguage.value)
    );
  }

  showSettingsBar() {
    this.settingsBar.style.display = "flex";
  }

  hideSettingsBar() {
    this.settingsBar.style.display = "none";
  }
}
