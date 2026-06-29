(function () {
  var images = document.querySelectorAll(".guide-aside-media img:not(.guide-no-zoom)");
  if (!images.length) return;

  var overlay = document.createElement("div");
  overlay.className = "guide-lightbox";
  overlay.hidden = true;
  overlay.innerHTML =
    '<button type="button" class="guide-lightbox-close" aria-label="Close enlarged image">&times;</button>' +
    '<figure class="guide-lightbox-figure"><img src="" alt=""></figure>';
  document.body.appendChild(overlay);

  var overlayImg = overlay.querySelector("img");
  var closeBtn = overlay.querySelector(".guide-lightbox-close");

  function openLightbox(img) {
    overlayImg.src = img.currentSrc || img.src;
    overlayImg.alt = img.alt;
    overlay.hidden = false;
    document.body.classList.add("guide-lightbox-open");
    closeBtn.focus();
  }

  function closeLightbox() {
    overlay.hidden = true;
    overlayImg.removeAttribute("src");
    document.body.classList.remove("guide-lightbox-open");
  }

  images.forEach(function (img) {
    img.classList.add("guide-zoomable");
    img.tabIndex = 0;
    img.setAttribute("role", "button");
    img.setAttribute("aria-label", (img.alt || "Guide screenshot") + " — click to enlarge");

    img.addEventListener("click", function () {
      openLightbox(img);
    });
    img.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openLightbox(img);
      }
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  overlay.addEventListener("click", function (event) {
    if (event.target === overlay) closeLightbox();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !overlay.hidden) closeLightbox();
  });
})();
