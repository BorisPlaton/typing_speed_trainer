import storage from "./data_storage.js";
import Broker from "./broker.js";
import wordsStorage from "./words_storage.js";
import { startLoadingAnimation, stopLoadingAnimation } from "./shortcuts.js";

export default class TextField extends Broker {
  constructor() {
    super();

    this.backgroundText = document.querySelector(".background-text");
    this.hiddenInput = document.querySelector(".input-text");

    this.currentWordNum = 0;
    this.currentCharIndex = 0;
    this.currentWordText;

    this.isTrainerStarted = false;
    this.isWordsUpdated = false;
    this.wordsIsAlreadyLonger = false;

    this.renderedTextHtml = null;

    this.fieldWordsAmount = 125;
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

  setTextFieldHtml(textFieldHtml) {
    this.backgroundText.innerHTML = textFieldHtml;
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
        this.currentWordText[this.currentCharIndex] == this.inputText.slice(-1)
      );
    }

    if (this.isWordLonger) {
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

    if (this.inputText.slice(0, -1) == this.currentWordText) {
      this.notifyCorrectWord();
    } else if (!this.isWordLonger) {
      this.notifyInvalidChar();
    }

    this.clearHiddenInput();
    try {
      this.setCurrentWordProperties(++this.currentWordNum);
      this.updateCurrentWordText();
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
    } else {
      this.setCurrentCharIsInvalid();
      this.notifyInvalidChar();
    }
    this.currentCharIndex++;
  }

  removeLastChar() {
    if (this.currentCharIndex > 0) {
      this.currentCharIndex--;
    }
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

  get isWordLonger() {
    return this.inputText.length > this.currentWordText.length;
  }

  get isSpaceKeyPressed() {
    return this.inputText.slice(-1) == " ";
  }

  get isCharRemoved() {
    return this.currentCharIndex > this.inputText.length;
  }

  get isCharAdded() {
    if (!this.isWordLonger) {
      return this.currentCharIndex < this.inputText.length;
    }
  }

  get currentCharSpan() {
    return this.currentWordSpan.querySelector(`.chr-${this.currentCharIndex}`);
  }

  get inputText() {
    return this.hiddenInput.value;
  }

  get currentWordSpan() {
    return document.querySelector(`.wrd-${this.currentWordNum}`);
  }

  updateCurrentWordText() {
    const wordSpans = this.currentWordSpan.querySelectorAll("span");
    let wordText = "";
    for (const charSpan of wordSpans) {
      wordText += charSpan.innerHTML;
    }
    this.currentWordText = wordText;
  }

  notifyInvalidChar() {
    storage.increaseTypoAmount();
    this.notify("invalidChar");
  }

  notifyCorrectWord() {
    storage.increaseCorrectWordsAmount();
    this.notify("correctWord");
  }

  notifyTrainerStarted() {
    if (!this.isTrainerStarted) {
      this.notify("typingTrainerStarted");
      this.isTrainerStarted = true;
    }
  }

  setCurrentCharIsNormal() {
    const currentCharClassList = this.currentWordSpan.querySelector(
      `.chr-${this.currentCharIndex}`
    ).classList;
    currentCharClassList.remove("correct-char");
    currentCharClassList.remove("invalid-char");
  }

  setCurrentWordProperties(wordNum) {
    this.currentWordNum = wordNum;
    this.currentCharIndex = 0;
    this.updateCurrentWordText();
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
