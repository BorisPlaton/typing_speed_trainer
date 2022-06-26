import Broker from "./broker.js";
import Cookies from "https://cdn.skypack.dev/js-cookie";
import storage from "./data_storage.js";

export default class AjaxResult extends Broker {
  constructor() {
    super();
    this.csrfToken = Cookies.get("csrftoken");
    this.sendToUrl = window.location.href;
  }

  sendResultToServer() {
    this.sendJSONRequest()
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  sendJSONRequest() {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", this.sendToUrl);

      xhr.setRequestHeader("Content-type", "application/json");
      xhr.setRequestHeader("X-CSRFToken", this.csrfToken);

      xhr.responseType = "json";

      xhr.addEventListener("load", () => {
        if (xhr.status == 200) {
          resolve(xhr.response);
        } else {
          reject(xhr.response);
        }
      });

      xhr.send(JSON.stringify(this.getResultData()));
    });
  }

  getResultData() {
    const result = {
      typoAmount: storage.typoAmount,
      correctWordsAmount: storage.correctWordsAmount,
    };

    return result;
  }
}
