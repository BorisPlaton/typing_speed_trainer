import { faker } from "https://cdn.skypack.dev/@faker-js/faker";

export default class TextField {
  constructor() {
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
    this.hiddenInput.addEventListener("keyup", (e) => {
      this.analyzePressedKey(e);
    });
    this.hiddenInput.addEventListener("input", () => this.analyzeInputChar());

    this.setTextFieldWords();
  }

  analyzePressedKey(event) {
    switch (event.key) {
      case "Backspace":
        this.removeLastChar();
        break;
      case " ":
        this.skipWord();
        break;
    }
  }

  analyzeInputChar() {
    const userInput = this.getInputChar();

    console.log(
      userInput.slice(-1),
      this.currentWordText[this.currentCharIndex]
    );

    if (
      this.currentWordText[this.currentCharIndex] == userInput.slice(-1) &&
      userInput.length <= this.currentWordText.length
    ) {
      this.setCurrentCharIsCorrect();
    } else {
      this.setCurrentCharIsInvalid();
    }

    this.currentCharIndex++;
  }

  skipWord() {
    this.clearHiddenInput();
    this.setCurrentWordProperties(++this.currentWordNum);
  }

  removeLastChar() {
    this.currentCharIndex > 0 ? this.currentCharIndex-- : {};
    this.setCurrentCharIsNormal();
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
      .classList.add("text-success");
  }

  setCurrentCharIsInvalid() {
    this.currentWordSpan
      .querySelector(`.chr-${this.currentCharIndex}`)
      .classList.add("text-danger");
  }

  setCurrentCharIsNormal() {
    const currentCharClassList = this.currentWordSpan.querySelector(
      `.chr-${this.currentCharIndex}`
    ).classList;
    currentCharClassList.remove("text-success");
    currentCharClassList.remove("text-danger");
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
