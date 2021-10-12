var elem = document.querySelector(".grid-container");
imagesLoaded(elem, () => {
  var msnry = new Masonry(elem, {
    // options
    itemSelector: ".grid-item",
    columnWidth: 300,
    gutter: 20,
    isFitWidth: true,
  });
});