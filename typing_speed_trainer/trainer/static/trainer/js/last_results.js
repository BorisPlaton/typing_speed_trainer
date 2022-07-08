import Broker from "./broker.js";
import statistics from "./statistics_data.js";

export default class ResultsList extends Broker {
  constructor() {
    super();

    this.sendToUrl = "results/";
    this.isResultBarCreated = false;
    this.otherUserResults = document.querySelector(".other-users-results");

    this.resultsBar;
    this.resultsList;

    this.resultTemplate;
    this.resultsListTemplate;
  }

  setup() {
    this.setLastResultsList();
  }

  setLastResultsList() {
    this.getCurrentUserResultsDataFromServer()
      .then((response) => {
        this.saveServerResponse(response);
        if (response.resultsData.length) {
          this.setResultsBar(response.resultsData);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }

  saveServerResponse(serverResponse) {
    this.resultTemplate = serverResponse.resultTemplate;
    this.resultsListTemplate = serverResponse.resultsListTemplate;
  }

  setResultsBar(resultsData) {
    this.createResultsBar(resultsData);
    this.populateResultBarWithData(resultsData);
  }

  createResultsBar() {
    const sidebar = document.querySelector(".sidebar");
    const divElement = document.createElement("div");

    divElement.innerHTML = this.resultsListTemplate;
    sidebar.insertBefore(divElement.firstChild, this.otherUserResults);

    this.resultsBar = document.querySelector(".last-results-list");
    this.resultsList = document.querySelector(".last-results-list .list");

    this.isResultBarCreated = true;
  }

  populateResultBarWithData(resultsData) {
    for (const data of resultsData) {
      this.addLastResult(data);
    }
  }

  getResultTemplate(data) {
    const div = document.createElement("div");
    div.innerHTML = this.resultTemplate;

    const wpm = div.querySelector(".result-wpm");
    const correctWordsAmount = div.querySelector(
      ".result-correct-words-amount"
    );
    const invalidWordsAmount = div.querySelector(
      ".result-invalid-words-amount"
    );
    const correctKeystrokes = div.querySelector(".result-keystrokes .correct");
    const invalidKeystrokes = div.querySelector(".result-keystrokes .invalid");
    const summaryKeystrokes = div.querySelector(".result-keystrokes .summary");
    const keystrokesAccuracy = div.querySelector(".result-accuracy");
    const dateEnd = div.querySelector(".result-date-end small");

    wpm.innerHTML = data.wpm;
    correctWordsAmount.innerHTML = data.correctWordsAmount;
    invalidWordsAmount.innerHTML = data.invalidWordsAmount;
    correctKeystrokes.innerHTML = data.correctKeystrokes;
    invalidKeystrokes.innerHTML = data.invalidKeystrokes;
    summaryKeystrokes.innerHTML = data.summaryKeystrokes;
    keystrokesAccuracy.innerHTML = data.typingAccuracy + "%";

    const dateEndValue = new Date(data.dateEnd);
    dateEnd.innerHTML = dateEndValue.toISOString().substring(11, 19);

    return div.firstChild;
  }

  getCurrentUserResultsDataFromServer() {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("GET", this.getUrlToTakeTemplates());
      xhr.setRequestHeader("Content-type", "application/json");
      xhr.responseType = "json";

      xhr.addEventListener("load", () => {
        if (xhr.status == 200) {
          resolve(xhr.response);
        } else {
          reject(xhr.response);
        }
      });

      xhr.send();
    });
  }

  getUrlToTakeTemplates() {
    return this.sendToUrl + "?templates=true";
  }

  addLastResultFromStorage() {
    const data = statistics.getTypingStatistics();
    this.addLastResult(data);
  }

  addLastResult(data) {
    if (!this.isResultBarCreated) {
      this.createResultsBar();
    }
    this.resultsList.prepend(this.getResultTemplate(data));
  }

  hideResultsList() {
    if (this.isResultBarCreated) {
      this.resultsBar.style.display = "none";
    }
    this.otherUserResults.style.display = "none";
  }

  showResultsList() {
    if (this.isResultBarCreated) {
      this.resultsBar.style.display = "flex";
    }
    this.otherUserResults.style.display = "flex";
  }
}
