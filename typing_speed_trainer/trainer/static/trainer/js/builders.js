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

  configureBeforeTrainerStart() {
    this.settingsBar.typingTrainerStarted();
    this.statisticsBar.setup();
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

    this.resultModalWindow.addBrokerListener("typingTrainerStarted", () => {
      console.log(1);
      this.configureBeforeTrainerStart();
    });

    this.textField.setup();
    this.settingsBar.setup();
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
      this.configureBeforeTrainerStart();
      this.resultsList.hideResultsList();
    });

    this.textField.addBrokerListener("typingTrainerStarted", () => {
      this.configureBeforeTrainerStart();
      this.resultsList.hideResultsList();
    });

    this.statisticsBar.addBrokerListener("typingTrainerStopped", () => {
      console.log(1);
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
      this.configureBeforeTrainerStart();
    });

    this.textField.addBrokerListener("typingTrainerStarted", () => {
      this.configureBeforeTrainerStart();
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

export default class TextFieldFactory {
  constructor(isUserAuthenticated) {
    return isUserAuthenticated
      ? new AuthenticatedUserTextField()
      : new AnonymousUserTextField();
  }
}
