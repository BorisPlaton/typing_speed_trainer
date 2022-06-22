export default class EventListener {
  constructor() {
    this.events = {
      typingTrainerStarted: [],
      typingTrainerStoped: [],
    };
  }

  addListener(event, callback) {
    this.events[event].push(callback);
  }

  notify(event) {
    this.events[event].forEach((callback) => callback());
  }
}
