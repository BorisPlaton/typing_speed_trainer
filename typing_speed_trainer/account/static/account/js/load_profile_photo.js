const selectPhotoButton = document.querySelector(".select-new-profile-photo");
const modalSelectPhotoForm = document.querySelector(".modal-page.photo");

const deletePhotoButton = document.querySelector(".delete-profile-photo");
const modalDeletePhotoForm = document.querySelector(".modal-page.delete");

selectPhotoButton.addEventListener("click", () => {
  modalSelectPhotoForm.style.display = "flex";
});

modalSelectPhotoForm.addEventListener("click", (event) => {
  if (event.target === event.currentTarget) {
    modalSelectPhotoForm.style.display = "none";
  }
});

if (deletePhotoButton) {
  deletePhotoButton.addEventListener("click", () => {
    modalDeletePhotoForm.style.display = "flex";
  });

  modalDeletePhotoForm.addEventListener("click", (event) => {
    if (event.target === event.currentTarget) {
      modalDeletePhotoForm.style.display = "none";
    }
  });
}
