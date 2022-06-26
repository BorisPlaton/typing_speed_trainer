class DataStorage {
  constructor() {
    this.setDefaultProperties();
  }

  setDefaultProperties() {
    this._totalTime = 0;
    this._executionTime = 0;
    this._typoAmount = 0;
    this._correctWordsAmount = 0;
    this._totalWordsAmount = 0;
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

  increaseTotalWordsAmount() {
    this._totalWordsAmount++;
  }

  decreaseTotalWordsAmount() {
    this._totalWordsAmount--;
  }

  cleanUpStorage() {
    this.setDefaultProperties();
  }

  get totalTime() {
    return this._totalTime;
  }

  set totalTime(value) {
    this._totalTime = value * 5;
  }

  get executionTime() {
    return this._executionTime;
  }

  set executionTime(value) {
    this._executionTime = value;
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

  get totaltWordsAmount() {
    return this._totalWordsAmount;
  }

  set totaltWordsAmount(value) {
    this._totalWordsAmount = value;
  }
}

const storage = new DataStorage();
export default storage;
