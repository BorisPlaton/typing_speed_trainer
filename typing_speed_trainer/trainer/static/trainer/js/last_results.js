import Broker from "./broker.js";
import storage from "./data_storage.js";

export default class ResultsList extends Broker {
  constructor() {
    super();

    this.sendToUrl = "results/";
    this.isResultBarCreated = false;

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
    sidebar.appendChild(divElement.firstChild);

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

    const correctWordsAmount = div.querySelector(
      ".result-correct-words-amount"
    );
    const typoAmount = div.querySelector(".result-typo-amount");
    const date = div.querySelector(".date");

    correctWordsAmount.innerHTML = data.correctWordsAmount;
    typoAmount.innerHTML = data.typoAmount;
    date.innerHTML = data.date;

    return div.firstChild;
  }

  getCurrentUserResultsDataFromServer() {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("GET", this.sendToUrl);
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

  addLastResultFromStorage() {
    const data = {
      typoAmount: storage.typoAmount,
      correctWordsAmount: storage.correctWordsAmount,
      date: storage.dateEnd,
    };
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
  }

  showResultsList() {
    if (this.isResultBarCreated) {
      this.resultsBar.style.display = "flex";
    }
  }
}
