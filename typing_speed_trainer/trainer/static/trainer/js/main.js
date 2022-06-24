import SettingsBar from "./settings_bar.js";
import StatisticsBar from "./statistics_bar.js";
import ResultModalWindow from "./result_modal_window.js";
import TextField from "./text_field.js";

const settingsBar = new SettingsBar();
const statisticsBar = new StatisticsBar();
const resultModalWindow = new ResultModalWindow();
const textField = new TextField();

textField.setup();
settingsBar.setup();

settingsBar.addBrokerListener("typingTrainerStarted", () =>
  statisticsBar.setup()
);

statisticsBar.addBrokerListener("typingTrainerStopped", () => {
  resultModalWindow.show();
  settingsBar.setup();
});
