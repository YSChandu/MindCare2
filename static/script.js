document.addEventListener('DOMContentLoaded', function () {
    const profileBtn = document.getElementById("profileBtn");
    const dropdown = document.getElementById("dropdown");

    profileBtn.addEventListener("click", function() {
        dropdown.classList.toggle("show");
    });

    window.addEventListener("click", function(event) {
        if (!event.target.matches('.profile-btn')) {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        }
    });
});

