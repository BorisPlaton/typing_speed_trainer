import storage from "./data_storage.js";
import wordsStorage from "./words_storage.js";
import { Subscriber, Publisher } from "./mediator.js";

class Word {
  /**
   * @param {string} word
   */
  constructor(word) {
    this.word = word;
    this.wordCharsStates = [];
  }

  removeLastChar() {
    this.wordCharsStates.pop();
  }

  addCharIsCorrect() {
    if (!this.isWordFull) {
      this.wordCharsStates.push(true);
    }
  }

  addCharIsWrong() {
    if (!this.isWordFull) {
      this.wordCharsStates.push(false);
    }
  }

  /**
   * @param {string} char
   */
  addNewChar(char) {
    if (this.isWordFull) {
      return;
    }
    if (this.currentChar === char) {
      this.addCharIsCorrect();
    } else {
      this.addCharIsWrong();
    }
  }

  resetWordCharsStates() {
    this.wordCharsStates = [];
  }

  /**
   * @param {string} word
   */
  changeWord(word) {
    this.word = word;
    this.resetWordCharsStates();
  }

  get currentChar() {
    return this.isWordFull
      ? this.lastWrittenChar
      : this.word.charAt(this.writtenWordLength);
  }

  get writtenWordLength() {
    return this.wordCharsStates.length;
  }

  get lastWrittenCharIndex() {
    return this.writtenWordLength ? this.writtenWordLength - 1 : 0;
  }

  get lastWrittenChar() {
    return this.word.charAt(this.lastWrittenCharIndex);
  }

  get originalWordLength() {
    return this.word.length;
  }

  get isWordFull() {
    return this.originalWordLength == this.writtenWordLength;
  }

  get isLastCharCorrect() {
    return this.writtenWordLength
      ? this.wordCharsStates[this.lastWrittenCharIndex]
      : null;
  }
}

export default class TextField extends Subscriber {
  /**
   * @param {Publisher} publisher
   */
  constructor(publisher) {
    super(publisher);

    this.backgroundText = document.querySelector(".background-text");
    this.hiddenInput = document.querySelector(".input-text");

    this.currentWordNum = 0;
    this.currentWord = new Word();

    this.isTrainerStarted = false;
    this.isWordsUpdated = false;
    this.wordsIsAlreadyLonger = false;

    this.renderedTextHtml = null;

    this.fieldWordsAmount = 250;
    this.fieldWordsLanguage;
  }

  setup() {
    this.hiddenInput.addEventListener("input", () => {
      this.notifyTrainerStarted();
      this.updateWordsListIfNeeded();
      this.analyzeInput();
    });

    this.backgroundText.addEventListener("click", () => {
      this.hiddenInput.focus();
    });

    this.hiddenInput.addEventListener("focus", () => {
      this.setTextIsSelected();
      this.setCurrentCharIsSelected();
    });

    this.hiddenInput.addEventListener("focusout", () => {
      this.setTextIsUnfocused();
      this.setCurrentCharIsUnfocused();
    });
  }

  stopTyping() {
    this.hiddenInput.blur();
    this.isTrainerStarted = false;
  }

  updateTextField(wordsLanguage = null) {
    this.fieldWordsLanguage = wordsLanguage || this.fieldWordsLanguage;
    this.clearHiddenInput();

    if (!this.renderedTextHtml) {
      startLoadingAnimation();
      this.getTextFieldHtml().then((textHtml) => {
        this.setTextFieldHtml(textHtml);
        this.setCurrentWordProperties(0);
        stopLoadingAnimation();
      });
    } else {
      this.setTextFieldHtml(this.renderedTextHtml);
      this.setCurrentWordProperties(0);
      this.setCurrentCharIsSelected();
      this.renderedTextHtml = null;
      this.isWordsUpdated = false;
    }
  }

  async getTextFieldHtml() {
    const newBackgroundText = document.createElement("div");
    const newWords = await wordsStorage.getWordsList(
      this.fieldWordsAmount,
      this.fieldWordsLanguage
    );

    for (let i = 0; i < this.fieldWordsAmount; i++) {
      const spanElement = this.getTextFieldSpanElement(newWords.words[i], i);
      newBackgroundText.append(spanElement);
      newBackgroundText.innerHTML += " ";
    }

    return newBackgroundText.innerHTML;
  }

  analyzeInput() {
    this.setCurrentCharIsUnfocused();

    if (this.isSpaceKeyPressed) {
      return this.skipWord();
    }

    if (this.isCharRemoved) {
      storage.decreaseCharsAmount();
      this.removeLastChar();
    } else if (this.isCharAdded) {
      storage.increaseCharsAmount();
      this.updateLastChar(
        this.currentWord.currentChar === this.inputText.slice(-1)
      );
    }

    if (this.isInputWordLonger) {
      if (!this.wordsIsAlreadyLonger) {
        this.notifyInvalidChar();
        this.wordsIsAlreadyLonger = true;
      }
      this.setInputIsLonger();
    } else {
      this.removeInputIsLonger();
      this.wordsIsAlreadyLonger = false;
    }

    this.setCurrentCharIsSelected();
  }

  async updateWordsListIfNeeded() {
    if ((this.wordsLeft < 15) & !this.isWordsUpdated) {
      await wordsStorage.updateWordsList(
        this.fieldWordsAmount,
        this.fieldWordsLanguage
      );
      this.isWordsUpdated = true;
      this.renderedTextHtml = await this.getTextFieldHtml();
    }
  }

  skipWord() {
    storage.increaseTotalWordsAmount();
    if (this.inputText.slice(0, -1) == this.currentWord.word) {
      this.notify("correctWord");
    } else if (!this.isInputWordLonger) {
      this.notifyInvalidChar();
    }
    this.clearHiddenInput();
    try {
      this.setCurrentWordProperties(++this.currentWordNum);
      this.setCurrentCharIsSelected();
    } catch {
      this.updateTextField();
    }
  }

  clearHiddenInput() {
    this.hiddenInput.value = "";
  }

  updateLastChar(isCorrect) {
    if (isCorrect) {
      this.setCurrentCharIsCorrect();
      this.currentWord.addCharIsCorrect();
      this.notify("correctChar");
    } else {
      this.setCurrentCharIsInvalid();
      this.currentWord.addCharIsWrong();
      this.notifyInvalidChar();
    }
  }

  removeLastChar() {
    if (this.currentWord.isLastCharCorrect) {
      this.notify("decreaseCorrectChar");
    }
    this.currentWord.removeLastChar();
    this.setCurrentCharIsNormal();
  }

  removeInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      span.classList.remove("invalid-word");
    }
  }

  get wordsLeft() {
    return this.fieldWordsAmount - this.currentWordNum;
  }

  get isInputWordLonger() {
    return this.inputText.length > this.currentWord.originalWordLength;
  }

  get isSpaceKeyPressed() {
    return this.inputText.slice(-1) == " ";
  }

  get isCharRemoved() {
    return this.currentWord.writtenWordLength > this.inputText.length;
  }

  get isCharAdded() {
    if (!this.isInputWordLonger) {
      return this.currentWord.writtenWordLength < this.inputText.length;
    }
  }

  get currentCharSpan() {
    return this.currentWordSpan.querySelector(
      `.chr-${this.currentWord.writtenWordLength}`
    );
  }

  get inputText() {
    return this.hiddenInput.value;
  }

  get currentWordSpan() {
    return document.querySelector(`.wrd-${this.currentWordNum}`);
  }

  updateCurrentWord() {
    const wordSpans = this.currentWordSpan.querySelectorAll("span");
    let wordText = "";
    for (const charSpan of wordSpans) {
      wordText += charSpan.innerHTML;
    }
    this.currentWord.changeWord(wordText);
  }

  notifyInvalidChar() {
    this.notify("invalidChar");
  }

  notifyTrainerStarted() {
    if (!this.isTrainerStarted) {
      this.notify("typingTrainerStarted");
      this.isTrainerStarted = true;
    }
  }

  setTextFieldHtml(textFieldHtml) {
    this.backgroundText.innerHTML = textFieldHtml;
  }

  setCurrentCharIsNormal() {
    const currentCharClassList = this.currentWordSpan.querySelector(
      `.chr-${this.currentWord.writtenWordLength}`
    ).classList;
    currentCharClassList.remove("correct-char");
    currentCharClassList.remove("invalid-char");
  }

  setCurrentWordProperties(wordNum) {
    this.currentWordNum = wordNum;
    this.updateCurrentWord();
  }

  setInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      span.classList.add("invalid-word");
    }
  }

  setCurrentCharIsCorrect() {
    try {
      this.currentCharSpan.classList.add("correct-char");
    } catch (e) {}
  }

  setCurrentCharIsInvalid() {
    try {
      this.currentCharSpan.classList.add("invalid-char");
    } catch (e) {}
  }

  setCurrentCharIsSelected() {
    try {
      this.currentCharSpan.classList.add("selected-char");
    } catch (e) {}
  }

  setCurrentCharIsUnfocused() {
    try {
      this.currentCharSpan.classList.remove("selected-char");
    } catch (e) {}
  }

  setTextIsSelected() {
    this.backgroundText.classList.add("selected");
  }

  setTextIsUnfocused() {
    this.backgroundText.classList.remove("selected");
  }

  getTextFieldSpanElement(word, wordNum) {
    const spanElement = document.createElement("span");
    spanElement.classList.add(`wrd-${wordNum}`);
    for (let i = 0; i < word.length; i++) {
      const charSpan = document.createElement("span");
      charSpan.classList.add(`chr-${i}`);
      charSpan.innerHTML = word[i];

      spanElement.appendChild(charSpan);
    }

    return spanElement;
  }
}

const loadingAnimation = document.querySelector(".loading-page");

export function startLoadingAnimation() {
  loadingAnimation.style.display = "flex";
}

export function stopLoadingAnimation() {
  loadingAnimation.style.display = "none";
}
