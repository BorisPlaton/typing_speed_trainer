import SettingsBar from "./settings_bar.js";
import StatisticsBar from "./statistics_bar.js";
import ResultModalWindow from "./result_modal_window.js";
import TextField from "./text_field.js";
import AjaxResult from "./ajax_result.js";
import ResultsList from "./last_results.js";
import storage from "./data_storage.js";
import { Publisher } from "./publisher.js";

class BaseProjectBuilder {
  constructor() {
    this.publisher = new Publisher();
    this.settingsBar = new SettingsBar(this.publisher);
    this.statisticsBar = new StatisticsBar(this.publisher);
    this.resultModalWindow = new ResultModalWindow(this.publisher);
    this.textField = new TextField(this.publisher);
  }

  setup() {
    this.configureEvents();
    this.configureComponents();
  }

  configureComponents() {
    this.settingsBar.setup();
    this.textField.setup();
  }

  configureEvents() {
    this.publisher.addSubscriber("correctWord", () => {
      storage.increaseCorrectWordsAmount();
      this.statisticsBar.increaseCorrectWord();
    });
    this.publisher.addSubscriber("correctChar", () => {
      storage.increaseCorrectCharsAmount();
      this.statisticsBar.increaseCorrectChars();
    });
    this.publisher.addSubscriber("invalidChar", () => {
      storage.increaseTypoAmount();
      this.statisticsBar.increaseWrongChar();
    });
    this.publisher.addSubscriber("decreaseCorrectChar", () => {
      storage.decreaseCorrectCharsAmount();
      this.statisticsBar.decreaseCorrectChars();
    });
    this.publisher.addSubscriber("languageChanged", () => {
      this.textField.updateTextField();
    });
    this.publisher.addSubscriber("typingTrainerStarted", () => {
      storage.cleanUpStorage();
      this.settingsBar.typingTrainerStarted();
      this.statisticsBar.setup();
      this.textField.trainerStarted();
    });
    this.publisher.addSubscriber("typingTrainerStopped", () => {
      this.textField.stopTyping();
      storage.setDateEndIsNow();
      this.resultModalWindow.show();
      this.settingsBar.showSettingsBar();
    });
    this.publisher.addSubscriber("typingTrainerRestart", () => {
      this.textField.stopTyping();
      this.settingsBar.showSettingsBar();
    });
  }
}

class AuthenticatedUserProject extends BaseProjectBuilder {
  constructor() {
    super();
    this.resultsList = new ResultsList();
    this.ajaxResult = new AjaxResult();
  }

  configureComponents() {
    super.configureComponents();
    this.resultsList.setup();
  }

  configureEvents() {
    super.configureEvents();
    this.publisher.addSubscriber("typingTrainerStarted", () => {
      this.resultsList.hideResultsList();
    });
    this.publisher.addSubscriber("typingTrainerRestart", () => {
      this.resultsList.showResultsList();
    });
    this.publisher.addSubscriber("typingTrainerStopped", () => {
      this.ajaxResult.sendResultToServer();
      this.resultsList.addLastResultFromStorage();
      this.resultsList.showResultsList();
    });
  }
}

export default function getConfiguredProject(isUserAuthenticated) {
  return isUserAuthenticated
    ? new AuthenticatedUserProject()
    : new BaseProjectBuilder();
}
