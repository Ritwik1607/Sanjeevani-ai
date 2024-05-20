document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const openIcon = document.querySelector(".open-icon");
    const closeIcon = document.querySelector(".close-icon");

    openIcon.addEventListener("click", function() {
        sidebar.style.left = "0";
        openIcon.style.display = "none";
        closeIcon.style.display = "block";
    });

    closeIcon.addEventListener("click", function() {
        sidebar.style.left = "-250px";
        closeIcon.style.display = "none";
        openIcon.style.display = "block";
    });
});
