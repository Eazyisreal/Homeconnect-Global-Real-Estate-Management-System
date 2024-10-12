const hamburger = document.getElementById('hamburger');
const navs = document.querySelectorAll('.nav-items');
const btn = document.getElementById('btn');
const navItem = document.getElementById('nav');
const successAlert = document.getElementById('success-alert');

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        if (successAlert) {
            successAlert.style.display = "none";
        }
    }, 3500);
});


function toggleMobile() {
    navs.forEach(nav => nav.classList.toggle('visible'));
    btn.classList.toggle('visible');
    navItem.classList.toggle('visible');
    hamburger.classList.toggle('visible');
}

hamburger.addEventListener('click', toggleMobile);
