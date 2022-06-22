import EventListener from "./broker";

class TextField {
  constructor() {
    this.backGroundText = document.querySelector(".background-text");
    this.hiddenInput = document.querySelector(".input-text");
  }

  setup() {
    this.createEventListeners();
  }

  createEventListeners() {
    this.backGroundText.addEventListener("click", () => {
      this.hiddenInput.focus();
    });
  }
}
