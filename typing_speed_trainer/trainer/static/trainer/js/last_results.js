import Broker from "./broker.js";

export default class ResultsList extends Broker {
  constructor() {
    super();

    this.resultsBar = document.querySelector(".last-results-list ");
  }

  addLastResult() {}

  hideResultsList() {
    this.resultsBar.style.display = "none";
  }

  showResultsList() {
    this.resultsBar.style.display = "flex";
  }
}
