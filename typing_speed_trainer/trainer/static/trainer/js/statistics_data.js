import storage from "./data_storage.js";
import Broker from "./broker.js";

class Statistics extends Broker {
  calculateTypingStatistics() {
    this.invalidKeystrokes = storage.typoAmount;
    this.totalKeystrokes = storage.charsAmount;
    this.correctKeystrokes = storage.charsAmount - storage.typoAmount;

    this.correctWordsAmount = storage.correctWordsAmount;
    this.invalidWordsAmount =
      storage.totalWordsAmount - storage.correctWordsAmount;
    this.totalWordsAmount = storage.totalWordsAmount;

    this.wpm = Math.ceil(this.correctKeystrokes / 5);
    this.dateEnd = storage.dateEnd;

    if (this.totalKeystrokes) {
      this.typingAccuracy =
        (this.correctKeystrokes / this.totalKeystrokes) * 100;
    } else {
      this.typingAccuracy = 0;
    }
  }

  getTypingStatistics() {
    return {
      invalidKeystrokes: this.invalidKeystrokes,
      correctKeystrokes: this.correctKeystrokes,
      summaryKeystrokes: this.totalKeystrokes,
      invalidWordsAmount: this.invalidWordsAmount,
      correctWordsAmount: this.correctWordsAmount,
      totalWordsAmount: this.totalWordsAmount,
      typingAccuracy: Number(this.typingAccuracy.toFixed(2)),
      wpm: this.wpm,
      dateEnd: this.dateEnd,
    };
  }
}

const statistics = new Statistics();
export default statistics;
