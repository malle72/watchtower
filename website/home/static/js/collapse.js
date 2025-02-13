
document.addEventListener('DOMContentLoaded', function () {
    const collapsibleButtons = document.querySelectorAll(".collapsible-button");
    collapsibleButtons.forEach(button => {
        button.addEventListener("click", function () {
            this.nextElementSibling.classList.toggle("active");
        });
    });
});
