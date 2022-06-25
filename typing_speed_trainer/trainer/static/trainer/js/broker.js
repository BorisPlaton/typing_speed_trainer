export default class Broker {
  constructor() {
    this.events = {
      typingTrainerStarted: [],
      typingTrainerStopped: [],
      typingTrainerRestart: [],
      correctWord: [],
      invalidChar: [],
    };
  }

  addBrokerListener(event, callback) {
    this.events[event].push(callback);
  }

  notify(event) {
    this.events[event].forEach((callback) => callback());
  }
}
