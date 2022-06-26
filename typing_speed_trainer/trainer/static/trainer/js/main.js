import SettingsBar from "./settings_bar.js";
import StatisticsBar from "./statistics_bar.js";
import ResultModalWindow from "./result_modal_window.js";
import TextField from "./text_field.js";
import AjaxResult from "./ajax_result.js";
import ResultsList from "./last_results.js";
import storage from "./data_storage.js";

const settingsBar = new SettingsBar();
const statisticsBar = new StatisticsBar();
const resultModalWindow = new ResultModalWindow();
const textField = new TextField();
const resultsList = new ResultsList();
const ajaxResult = new AjaxResult();

textField.setup();
settingsBar.setup();
resultsList.setup();

settingsBar.addBrokerListener("typingTrainerStarted", () => {
  resultsList.hideResultsList();
  statisticsBar.setup();
});

statisticsBar.addBrokerListener("typingTrainerStopped", () => {
  storage.setDateEndIsNow();
  ajaxResult.sendResultToServer();
  resultModalWindow.show();
  resultsList.addLastResultFromStorage();

  storage.cleanUpStorage();

  settingsBar.setup();
  resultsList.showResultsList();
  textField.stopTyping();
});

statisticsBar.addBrokerListener("typingTrainerRestart", () => {
  settingsBar.setup();
  resultsList.showResultsList();
  textField.stopTyping();
});

textField.addBrokerListener("correctWord", () =>
  statisticsBar.increaseCorrectWord()
);
textField.addBrokerListener("invalidChar", () =>
  statisticsBar.increaseWrongChar()
);
