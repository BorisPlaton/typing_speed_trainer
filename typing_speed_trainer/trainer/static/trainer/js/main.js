import getConfiguredProject from "./builders.js";

function getIsUserAuthenticated() {
  const element = document.querySelector("main");
  return element.dataset.authenticated.toLowerCase() === "true" ? true : false;
}

const isUserAuthenticated = getIsUserAuthenticated();
const textField = getConfiguredProject(isUserAuthenticated);

document.addEventListener("DOMContentLoaded", () => textField.setup());
