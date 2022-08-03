import SettingsBar from "./settings_bar.js";
import StatisticsBar from "./statistics_bar.js";
import ResultModalWindow from "./result_modal_window.js";
import TextField from "./text_field.js";
import AjaxResult from "./ajax_result.js";
import ResultsList from "./last_results.js";
import storage from "./data_storage.js";

class BaseTextField {
  constructor() {
    this.settingsBar = new SettingsBar();
    this.statisticsBar = new StatisticsBar();
    this.resultModalWindow = new ResultModalWindow();
    this.textField = new TextField();
  }

  setup() {
    this.textField.addBrokerListener("correctWord", () => {
      storage.increaseCorrectWordsAmount();
      this.statisticsBar.increaseCorrectWord();
    });

    this.textField.addBrokerListener("invalidChar", () => {
      storage.increaseTypoAmount();
      this.statisticsBar.increaseWrongChar();
    });

    this.textField.addBrokerListener("correctChar", () => {
      storage.increaseCorrectCharsAmount();
      this.statisticsBar.increaseCorrectChars();
    });

    this.textField.addBrokerListener("decreaseCorrectChar", () => {
      storage.decreaseCorrectCharsAmount();
      this.statisticsBar.decreaseCorrectChars();
    });

    this.settingsBar.addBrokerListener("languageChanged", (args) => {
      this.textField.updateTextField(args);
    });

    this.textField.setup();
    this.settingsBar.setup();
  }
}

export default class TextFieldFactory {
  constructor(isUserAuthenticated) {
    return isUserAuthenticated
      ? new AuthenticatedUserTextField()
      : new AnonymousUserTextField();
  }
}

class AuthenticatedUserTextField extends BaseTextField {
  constructor() {
    super();

    this.resultsList = new ResultsList();
    this.ajaxResult = new AjaxResult();
  }

  setup() {
    super.setup();

    this.resultsList.setup();

    this.settingsBar.addBrokerListener("typingTrainerStarted", () => {
      this.resultsList.hideResultsList();
      this.statisticsBar.setup();
    });

    this.textField.addBrokerListener("typingTrainerStarted", () => {
      this.settingsBar.typingTrainerStarted();
      this.resultsList.hideResultsList();
      this.statisticsBar.setup();
    });

    this.statisticsBar.addBrokerListener("typingTrainerStopped", () => {
      storage.setDateEndIsNow();
      this.textField.stopTyping();
      this.resultModalWindow.show();
      this.ajaxResult.sendResultToServer();
      this.resultsList.addLastResultFromStorage();
      storage.cleanUpStorage();
      this.settingsBar.showSettingsBar();
      this.resultsList.showResultsList();
      this.settingsBar.languageSelected();
    });

    this.statisticsBar.addBrokerListener("typingTrainerRestart", () => {
      storage.cleanUpStorage();
      this.settingsBar.showSettingsBar();
      this.resultsList.showResultsList();
      this.textField.stopTyping();
      this.settingsBar.languageSelected();
    });
  }
}

class AnonymousUserTextField extends BaseTextField {
  setup() {
    super.setup();

    this.settingsBar.addBrokerListener("typingTrainerStarted", () => {
      this.statisticsBar.setup();
    });

    this.textField.addBrokerListener("typingTrainerStarted", () => {
      this.settingsBar.typingTrainerStarted();
      this.statisticsBar.setup();
    });

    this.statisticsBar.addBrokerListener("typingTrainerStopped", () => {
      storage.setDateEndIsNow();
      this.textField.stopTyping();

      this.resultModalWindow.show();

      storage.cleanUpStorage();

      this.settingsBar.showSettingsBar();
      this.settingsBar.languageSelected();
    });

    this.statisticsBar.addBrokerListener("typingTrainerRestart", () => {
      storage.cleanUpStorage();

      this.settingsBar.showSettingsBar();
      this.textField.stopTyping();
      this.settingsBar.languageSelected();
    });
  }
}
