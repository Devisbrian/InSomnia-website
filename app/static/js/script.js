var elem = document.querySelector(".news-cards");
imagesLoaded(elem, () => {
  var msnry = new Masonry(elem, {
    // options
    itemSelector: ".card-item",
    columnWidth: 320,
    gutter: 20,
    isFitWidth: true,
  });
});

function actualizarInputFile() {
  var filename = "'" + this.value.replace(/^.*[\\\/]/, '') + "'";
  if (filename === "''") {
        this.parentElement.style.setProperty('--fn', "'Seleccionar archivo'");
  } else {
    this.parentElement.style.setProperty('--fn', filename);
  }
}
document.querySelectorAll(".file-select input").forEach((ele)=>ele.addEventListener('change', actualizarInputFile));

/* */ 
function actualizarInputFile2() {
  var filename = "'" + this.value.replace(/^.*[\\\/]/, '') + "'";
  if (filename === "''") {
        this.parentElement.style.setProperty('--fn', "'Seleccionar archivo'");
  } else {
    this.parentElement.style.setProperty('--fn', "'Archivos seleccionados'");
  }
}
document.querySelectorAll(".multiple-file-select input").forEach((ele)=>ele.addEventListener('change', actualizarInputFile2));



document.querySelector('.menu-btn').addEventListener('click', () => {
  document.querySelector('.nav-menu').classList.toggle('show');
  document.querySelector('.nav-menu-right').classList.toggle('show');
});

document.querySelector('.dc-btn').addEventListener('click', () => {
  document.querySelector('.dc-btn-show').classList.toggle('show');
  document.querySelector('.fc-btn-show').classList.remove('show');
  document.querySelector('.user-btn-show').classList.remove('show');
});

document.querySelector('.fc-btn').addEventListener('click', () => {
  document.querySelector('.fc-btn-show').classList.toggle('show');
  document.querySelector('.dc-btn-show').classList.remove('show');
  document.querySelector('.user-btn-show').classList.remove('show');
});

document.querySelector("div.container").addEventListener('click', () => {
  document.querySelector('.fc-btn-show').classList.remove('show');
  document.querySelector('.dc-btn-show').classList.remove('show');
  document.querySelector('.user-btn-show').classList.remove('show');
  document.querySelector('.nav-main ul.nav-menu').classList.remove('show');
  document.querySelector('.nav-main ul.nav-menu-right').classList.remove('show');
});

document.querySelector('.home-btn').addEventListener('click', () => {
  document.querySelector('.fc-btn-show').classList.remove('show');
  document.querySelector('.dc-btn-show').classList.remove('show');
  document.querySelector('.user-btn-show').classList.remove('show');
})

// Get the modal
var modal = document.getElementById('idlogin');
var modal2 = document.getElementById('idsignup');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
      modal.style.display = "none";
  }
  if (event.target == modal2) {
      modal2.style.display = "none";
  }
}