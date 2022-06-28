import Broker from "./broker.js";
import Cookies from "https://cdn.skypack.dev/js-cookie";
import statistics from "./statistics_data.js";

export default class AjaxResult extends Broker {
  constructor() {
    super();
    this.csrfToken = Cookies.get("csrftoken");
    this.sendToUrl = "results/";
  }

  sendResultToServer() {
    this.sendJSONRequest().catch((error) => {
      console.error(error);
    });
    console.log(2);
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

      xhr.send(JSON.stringify(statistics.getTypingStatistics()));
    });
  }
}
