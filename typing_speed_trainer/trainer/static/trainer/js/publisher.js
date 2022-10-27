export class Publisher {
  constructor() {
    this.events = {};
  }

  /**
   * @param {string} event
   */
  addSubscriber(event, callback) {
    if (!this.events.hasOwnProperty(event)) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  }

  /**
   * @param {string} event
   */
  notify(event) {
    if (this.events.hasOwnProperty(event)) {
      this.events[event].forEach((callback) => callback());
    }
  }
}

export class Subscriber {
  /**
   * @param {Publisher} publisher
   */
  constructor(publisher) {
    this.publisher = publisher;
  }

  /**
   * @param {string} event
   */
  notify(event, args) {
    this.publisher.notify(event, args);
  }
}
