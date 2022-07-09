import { faker } from "https://cdn.skypack.dev/@faker-js/faker";
import storage from "./data_storage.js";
import Broker from "./broker.js";

export default class TextField extends Broker {
  constructor() {
    super();

    this.loadingAnimation = document.querySelector(".loading-page");

    this.backgroundText = document.querySelector(".background-text");
    this.hiddenInput = document.querySelector(".input-text");

    this.currentWordSpan;
    this.currentWordText;
    this.currentWordNum;
    this.currentCharIndex;
    this.isWordLonger = false;
  }

  setup() {
    this.setTextFieldWords();

    this.backgroundText.addEventListener("click", () => {
      this.hiddenInput.focus();
    });

    this.hiddenInput.addEventListener("input", () => {
      this.analyzeInputChar();
      this.analyzeWord();
    });

    this.hiddenInput.addEventListener("focus", () => {
      this.backgroundText.classList.add("selected");
      this.setNextCharIsSelected();
    });

    this.hiddenInput.addEventListener("focusout", () => {
      this.backgroundText.classList.remove("selected");
      this.setCurrentCharIsUnfocused();
    });
  }

  stopTyping() {
    this.hiddenInput.blur();
    this.setTextFieldWords();
  }

  setTextFieldWords() {
    this.loadingAnimation.style.display = "flex";

    setTimeout(() => {
      this.clearTextField();
      this.clearHiddenInput();
      for (let i = 0; i < 200; i++) {
        const spanElement = this.getTextFieldSpanElement(
          faker.random.words(1).toLowerCase(),
          i
        );
        this.backgroundText.append(spanElement);
        this.backgroundText.innerHTML += " ";
      }
      this.setCurrentWordProperties(0);

      this.loadingAnimation.style.display = "none";
    }, 0);
  }

  analyzeInputChar() {
    storage.increaseCharsAmount();
    this.setCurrentCharIsUnfocused();
    switch (true) {
      case this.isSpaceKeyPressed():
        this.currentWordText += " ";
        this.skipWord();
        break;
      case this.isCharRemoved():
        storage.decreaseCharsAmount();
        this.removeLastChar();
        break;
      case this.isCharAdded():
        this.updateLastChar(
          this.currentWordText[this.currentCharIndex] ==
            this.getInputText().slice(-1)
        );
        break;
    }
    this.setNextCharIsSelected();
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
    return this.getInputText() == this.currentWordText;
  }

  isInputBiggerThenWord() {
    return this.getInputText().length > this.currentWordText.length;
  }

  isSpaceKeyPressed() {
    return this.getInputText().slice(-1) == " ";
  }

  isCharRemoved() {
    return this.currentCharIndex > this.getInputText().length;
  }

  isCharAdded() {
    if (!this.isInputBiggerThenWord()) {
      return this.currentCharIndex < this.getInputText().length;
    }
  }

  isInputAndWordSameLength() {
    return this.currentWordText.length == this.getInputText().length;
  }

  skipWord() {
    if (this.isInputAndWordEqual()) {
      this.notifyCorrectWord("correctWord");
    } else {
      if (!this.isWordLonger) {
        this.notifyInvalidChar();
      }
    }
    storage.increaseTotalWordsAmount();
    this.clearHiddenInput();
    this.setCurrentWordProperties(++this.currentWordNum);
  }

  removeLastChar() {
    this.setCurrentCharIsUnfocused();
    if (this.currentCharIndex > 0) {
      this.currentCharIndex--;
    }
    this.setCurrentCharIsNormal();
  }

  setInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      if (!this.isWordLonger) {
        this.notifyInvalidChar();
        this.isWordLonger = true;
      }
      span.classList.add("invalid-word");
    }
  }

  removeInputIsLonger() {
    for (const span of this.currentWordSpan.querySelectorAll("span")) {
      this.isWordLonger = false;
      span.classList.remove("invalid-word");
    }
  }

  notifyInvalidChar() {
    storage.increaseTypoAmount();
    this.notify("invalidChar");
  }

  notifyCorrectWord() {
    storage.increaseCorrectWordsAmount();
    this.notify("correctWord");
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

  getCurrentWordText() {
    const wordSpans = this.currentWordSpan.querySelectorAll("span");
    let wordText = "";
    for (const charSpan of wordSpans) {
      wordText += charSpan.innerHTML;
    }
    return wordText;
  }

  setCurrentCharIsCorrect() {
    try {
      this.getCurrentCharSpan().classList.add("correct-char");
    } catch (e) {}
  }

  setCurrentCharIsInvalid() {
    try {
      this.getCurrentCharSpan().classList.add("invalid-char");
    } catch (e) {}
  }

  setNextCharIsSelected() {
    try {
      this.getCurrentCharSpan().classList.add("selected-char");
    } catch (e) {}
  }

  setCurrentCharIsUnfocused() {
    try {
      this.getCurrentCharSpan().classList.remove("selected-char");
    } catch (e) {}
  }

  getCurrentCharSpan() {
    return this.currentWordSpan.querySelector(`.chr-${this.currentCharIndex}`);
  }

  setCurrentCharIsNormal() {
    const currentCharClassList = this.currentWordSpan.querySelector(
      `.chr-${this.currentCharIndex}`
    ).classList;
    currentCharClassList.remove("correct-char");
    currentCharClassList.remove("invalid-char");
  }

  getInputText() {
    return this.hiddenInput.value;
  }

  setCurrentWordProperties(wordNum) {
    this.currentWordNum = wordNum;
    this.currentWordSpan = document.querySelector(`.wrd-${wordNum}`);
    this.currentWordText = this.getCurrentWordText();
    this.currentCharIndex = 0;
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
    this.backgroundText.innerHTML = "";
  }

  clearHiddenInput() {
    this.hiddenInput.value = "";
  }
}
