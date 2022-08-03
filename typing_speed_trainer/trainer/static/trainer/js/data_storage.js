class DataStorage {
  constructor() {
    this.dateEnd;
    this.setDefaultProperties();
  }

  setDefaultProperties() {
    this.totalTime = 0;
    this.executionTime = 0;
    this.typoAmount = 0;
    this.correctCharsAmount = 0;
    this.correctWordsAmount = 0;
    this.totalWordsAmount = 0;
    this.charsAmount = 0;
  }

  get typingStatistics() {
    return {
      invalidKeystrokes: storage.typoAmount,
      correctKeystrokes: storage.correctCharsAmount,
      summaryKeystrokes: storage.charsAmount,
      invalidWordsAmount: storage.invalidWordsAmount,
      correctWordsAmount: storage.correctWordsAmount,
      totalWordsAmount: storage.totalWordsAmount,
      typingAccuracy: Number(
        (storage.correctCharsAmount / (storage.charsAmount + storage.typoAmount) * 100).toFixed(2)
      ),
      wpm: Math.ceil(storage.correctCharsAmount / 5),
      dateEnd: storage.dateEnd,
    };
  }

  get invalidWordsAmount() {
    return this.totalWordsAmount - this.correctWordsAmount;
  }

  increaseCorrectCharsAmount() {
    this.correctCharsAmount++;
  }

  decreaseCorrectCharsAmount() {
    this.correctCharsAmount--;
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
