class DataStorage {
  constructor() {
    this.setDefaultProperties();
  }

  setDefaultProperties() {
    this.totalTime = 0;
    this.executionTime = 0;
    this.typoAmount = 0;
    this.correctWordsAmount = 0;
    this.totalWordsAmount = 0;
    this.charsAmount = 0;

    this.dateEnd;
  }

  increaseTypoAmount() {
    this.typoAmount++;
  }

  decreaseTypoAmount() {
    this.typoAmount--;
  }

  increaseCorrectWordsAmount() {
    this.correctWordsAmount++;
  }

  decreaseCorrectWordsAmount() {
    this.correctWordsAmount--;
  }

  increaseTotalWordsAmount() {
    this.totalWordsAmount++;
  }

  decreaseTotalWordsAmount() {
    this.totalWordsAmount--;
  }

  increaseCharsAmount() {
    this.charsAmount++;
  }

  decreaseCharsAmount() {
    if (this.charsAmount > 0) {
      this.charsAmount--;
    }
  }

  cleanUpStorage() {
    this.setDefaultProperties();
  }

  setDateEndIsNow() {
    this.dateEnd = new Date();
  }
}

const storage = new DataStorage();
export default storage;
