export default class Broker {
  constructor() {
    this.events = {
      typingTrainerStarted: [],
      typingTrainerStopped: [],
      typingTrainerRestart: [],
      languageChanged: [],
      correctWord: [],
      correctChar: [],
      decreaseCorrectChar: [],
      invalidChar: [],
    };
  }

  addBrokerListener(event, callback) {
    this.events[event].push(callback);
  }

  notify(event, args = null) {
    this.events[event].forEach((callback) => callback(args));
  }
}
