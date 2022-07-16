const loadingAnimation = document.querySelector(".loading-page");

export function startLoadingAnimation() {
  loadingAnimation.style.display = "flex";
}

export function stopLoadingAnimation() {
  loadingAnimation.style.display = "none";
}
