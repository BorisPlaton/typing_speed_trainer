import { faker } from "https://cdn.skypack.dev/@faker-js/faker";
import storage from "./data_storage.js";
import Broker from "./broker.js";

export default class TextField extends Broker {
  constructor() {
    super();

    this.backGroundText = document.querySelector(".background-text");
    this.hiddenInput = document.querySelector(".input-text");

    this.currentWordSpan;
    this.currentWordText;
    this.currentWordNum;
    this.currentCharIndex;
  }

  setup() {
    this.backGroundText.addEventListener("click", () => {
      this.hiddenInput.focus();
    });
    this.hiddenInput.addEventListener("input", () => {
      this.analyzeInputChar();
      this.analyzeWord();
    });

    this.setTextFieldWords();
  }

  stopTyping() {
    this.hiddenInput.blur();
    this.setTextFieldWords();
  }

  analyzeInputChar() {
    switch (true) {
      case this.isSpaceKeyPressed():
        this.currentWordText += " ";
        this.skipWord();
        break;
      case this.isCharRemoved():
        this.removeLastChar();
        break;
      case this.isCharAdded():
        this.updateLastChar(
          this.currentWordText[this.currentCharIndex] ==
            this.getInputChar().slice(-1)
        );
    }
  }

  analyzeWord() {
    switch (true) {
      case this.isInputBiggerThenWord():
        this.setInputIsLonger();
        break;
      case this.isInputAndWordSameLength():
        this.removeInputIsLonger();
        break;
    }
  }

  isInputAndWordEqual() {
    return this.getInputChar() == this.currentWordText;
  }

  isInputBiggerThenWord() {
    return this.getInputChar().length > this.currentWordText.length;
  }

  isSpaceKeyPressed() {
    return this.getInputChar().slice(-1) == " ";
  }

  isCharRemoved() {
    return this.currentCharIndex > this.getInputChar().length;
  }

  isCharAdded() {
    if (!this.isInputBiggerThenWord()) {
      return this.currentCharIndex < this.getInputChar().length;
    }
  }

  isInputAndWordSameLength() {
    return this.currentCharIndex == this.getInputChar().length;
  }

  skipWord() {
    if (this.isInputAndWordEqual()) {
      storage.increaseCorrectWordsAmount();
      this.notify("correctWord");
    }
    storage.increaseTotalWordsAmount();
    this.clearHiddenInput();
    this.setCurrentWordProperties(++this.currentWordNum);
  }

  removeLastChar() {
    if (!this.isInputBiggerThenWord()) {
      if (this.currentCharIndex > 0) {
        this.currentCharIndex--;
      }
      this.setCurrentCharIsNormal();
    }
  }

  setInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      span.classList.add("invalid-word");
    }
  }

  removeInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      span.classList.remove("invalid-word");
    }
  }

  updateLastChar(isCorrect) {
    if (isCorrect) {
      this.setCurrentCharIsCorrect();
    } else {
      this.setCurrentCharIsInvalid();
      storage.increaseTypoAmount();
      this.notify("invalidChar");
    }
    this.currentCharIndex++;
  }

  getCurrentWordText() {
    const wordSpans = this.currentWordSpan.querySelectorAll("span");
    let wordText = "";
    for (const charSpan of wordSpans) {
      wordText += charSpan.innerHTML;
    }
    return wordText;
  }

  setCurrentCharIsCorrect() {
    this.currentWordSpan
      .querySelector(`.chr-${this.currentCharIndex}`)
      .classList.add("correct-char");
  }

  setCurrentCharIsInvalid() {
    this.currentWordSpan
      .querySelector(`.chr-${this.currentCharIndex}`)
      .classList.add("invalid-char");
  }

  setCurrentCharIsNormal() {
    const currentCharClassList = this.currentWordSpan.querySelector(
      `.chr-${this.currentCharIndex}`
    ).classList;
    currentCharClassList.remove("correct-char");
    currentCharClassList.remove("invalid-char");
  }

  getInputChar() {
    return this.hiddenInput.value;
  }

  setCurrentWordProperties(wordNum) {
    this.currentWordNum = wordNum;
    this.currentWordSpan = document.querySelector(`.wrd-${wordNum}`);
    this.currentWordText = this.getCurrentWordText();
    this.currentCharIndex = 0;
  }

  setTextFieldWords() {
    this.clearTextField();
    this.clearHiddenInput();
    for (let i = 0; i < 150; i++) {
      const spanElement = this.getTextFieldSpanElement(
        faker.random.words(1).toLowerCase(),
        i
      );
      this.backGroundText.append(spanElement);
      this.backGroundText.innerHTML += " ";
    }

    this.setCurrentWordProperties(0);
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

  clearTextField() {
    this.backGroundText.innerHTML = "";
  }

  clearHiddenInput() {
    this.hiddenInput.value = "";
  }
}
