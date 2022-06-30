import TextFieldFactory from "./project.js";

function getIsUserAuthenticated() {
  const element = document.querySelector("main");
  return element.dataset.authenticated.toLowerCase() === "true" ? true : false;
}

const isUserAuthenticated = getIsUserAuthenticated();
const textField = new TextFieldFactory(isUserAuthenticated);

document.addEventListener("DOMContentLoaded", () => textField.setup());
