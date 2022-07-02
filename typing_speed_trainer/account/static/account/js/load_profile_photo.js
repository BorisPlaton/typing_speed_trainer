const selectPhoto = document.querySelector(".select-new-profile-photo");
const modalSelectPhotoForm = document.querySelector(".load-photo-modal-page");

selectPhoto.addEventListener("click", () => {
  modalSelectPhotoForm.style.display = "flex";
});

modalSelectPhotoForm.addEventListener("click", (event) => {
  if (event.target === event.currentTarget) {
    modalSelectPhotoForm.style.display = "none";
  }
});
