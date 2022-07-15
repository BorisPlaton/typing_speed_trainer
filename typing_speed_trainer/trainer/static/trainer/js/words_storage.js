class WordsServer {
  getWordsFromServer(wordsAmount = null, wordsLanguage = null) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("GET", this.getWordsServerUrl(wordsAmount, wordsLanguage));
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

  getWordsServerUrl(wordsAmount, wordsLanguage) {
    const serverUrl = new URL("http://127.0.0.1:5050/");

    if (wordsAmount) {
      serverUrl.searchParams.append("quantity", wordsAmount);
    }

    if (wordsLanguage) {
      serverUrl.searchParams.append("lang", wordsLanguage);
    }

    return serverUrl.toString();
  }
}

class Words {
  constructor() {
    this.wordsServer = new WordsServer();
    this.wordsList = [];
  }

  async updateWordsList(wordsAmount = null, wordsLanguage = null) {
    try {
      const response = await this.wordsServer.getWordsFromServer(
        wordsAmount,
        wordsLanguage
      );
      return response;
    } catch (e) {
      console.error(e);
    }
  }

  async getWordsList(wordsAmount = null, wordsLanguage = null) {
    if (!this.wordsList.length || wordsAmount || wordsLanguage) {
      this.wordsList = await this.updateWordsList(wordsAmount, wordsLanguage);
    }
    return this.wordsList;
  }
}

const wordsStorage = new Words();
export default wordsStorage;
