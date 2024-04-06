const nav_btn_click = function(x) {
    x.classList.toggle("change");
}
document.querySelector(".nav-btn").addEventListener(
  "click", function () {
    document.querySelector(".wrapper .nav-links").classList.toggle("hide-show");
})