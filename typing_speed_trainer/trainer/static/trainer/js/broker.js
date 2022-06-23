export default class Broker {
  constructor() {
    this.events = {
      typingTrainerStarted: [],
      typingTrainerStopped: [],
      correctChar: [],
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
