import StandardPage from "./settings_bar.js";
import TypingTrainer from "./statistics_bar.js";

const standardPage = new StandardPage();
const typingTrainer = new TypingTrainer();

standardPage.setup();
standardPage.addBrokerListener("typingTrainerStarted", () =>
  typingTrainer.setup()
);
typingTrainer.addBrokerListener("typingTrainerStopped", () =>
  standardPage.setup()
);
