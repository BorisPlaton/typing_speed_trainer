class DataStorage {
  constructor() {
    this.setDefaultProperties();
  }

  setDefaultProperties() {
    this._executionTime = 0;
    this._typoAmount = 0;
    this._correctWordsAmount = 0;
  }

  increaseTypoAmount() {
    this._typoAmount++;
  }

  decreaseTypoAmount() {
    this._typoAmount--;
  }

  increaseCorrectWordsAmount() {
    this._correctWordsAmount++;
  }

  decreaseCorrectWordsAmount() {
    this._correctWordsAmount--;
  }

  cleanUpStorage() {
    this.setDefaultProperties();
  }

  getAllData() {
    return {
      executionTime: this._executionTime,
      typoAmount: this._typoAmount,
      correctWordsAmount: this._correctWordsAmount,
    };
  }

  get executionTime() {
    return this._executionTime;
  }

  set executionTime(value) {
    this._executionTime = value * 60 * 1000;
  }

  get typoAmount() {
    return this._typoAmount;
  }

  set typoAmount(value) {
    this._typoAmount = value;
  }

  get correctWordsAmount() {
    return this._correctWordsAmount;
  }

  set correctWordsAmount(value) {
    this._correctWordsAmount = value;
  }
}

const storage = new DataStorage();
export default storage;
