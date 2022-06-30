import SettingsBar from "./settings_bar.js";
import StatisticsBar from "./statistics_bar.js";
import ResultModalWindow from "./result_modal_window.js";
import TextField from "./text_field.js";
import AjaxResult from "./ajax_result.js";
import ResultsList from "./last_results.js";
import storage from "./data_storage.js";
import statistics from "./statistics_data.js";

class AbstractTextField {
  setup() {}
}

export default class TextFieldFactory {
  constructor(isUserAuthenticated) {
    return isUserAuthenticated
      ? new AuthenticatedUserTextField()
      : new AnonymousUserTextField();
  }
}

class AuthenticatedUserTextField extends AbstractTextField {
  constructor() {
    super();

    this.settingsBar = new SettingsBar();
    this.statisticsBar = new StatisticsBar();
    this.resultModalWindow = new ResultModalWindow();
    this.textField = new TextField();
    this.resultsList = new ResultsList();
    this.ajaxResult = new AjaxResult();
  }

  setup() {
    this.textField.setup();
    this.settingsBar.setup();
    this.resultsList.setup();

    this.settingsBar.addBrokerListener("typingTrainerStarted", () => {
      this.resultsList.hideResultsList();
      this.statisticsBar.setup();
    });

    this.statisticsBar.addBrokerListener("typingTrainerStopped", () => {
      storage.setDateEndIsNow();
      statistics.calculateTypingStatistics();
      this.textField.stopTyping();

      this.resultModalWindow.show();

      this.ajaxResult.sendResultToServer();

      this.resultsList.addLastResultFromStorage();

      storage.cleanUpStorage();

      this.settingsBar.setup();
      this.resultsList.showResultsList();
    });

    this.statisticsBar.addBrokerListener("typingTrainerRestart", () => {
      storage.cleanUpStorage();

      this.settingsBar.setup();
      this.resultsList.showResultsList();
      this.textField.stopTyping();
    });

    this.textField.addBrokerListener("correctWord", () =>
      this.statisticsBar.increaseCorrectWord()
    );

    this.textField.addBrokerListener("invalidChar", () =>
      this.statisticsBar.increaseWrongChar()
    );
  }
}

class AnonymousUserTextField extends AbstractTextField {
  constructor() {
    super();

    this.settingsBar = new SettingsBar();
    this.statisticsBar = new StatisticsBar();
    this.resultModalWindow = new ResultModalWindow();
    this.textField = new TextField();
  }

  setup() {
    this.textField.setup();
    this.settingsBar.setup();

    this.settingsBar.addBrokerListener("typingTrainerStarted", () => {
      this.statisticsBar.setup();
    });

    this.statisticsBar.addBrokerListener("typingTrainerStopped", () => {
      storage.setDateEndIsNow();
      statistics.calculateTypingStatistics();
      this.textField.stopTyping();

      this.resultModalWindow.show();

      storage.cleanUpStorage();

      this.settingsBar.setup();
    });

    this.statisticsBar.addBrokerListener("typingTrainerRestart", () => {
      storage.cleanUpStorage();

      this.settingsBar.setup();
      this.textField.stopTyping();
    });

    this.textField.addBrokerListener("correctWord", () =>
      this.statisticsBar.increaseCorrectWord()
    );

    this.textField.addBrokerListener("invalidChar", () =>
      this.statisticsBar.increaseWrongChar()
    );
  }
}
