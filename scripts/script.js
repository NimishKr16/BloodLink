window.onclick = function(event) {
    var popups = document.getElementsByClassName('popup');
    for (var i = 0; i < popups.length; i++) {
        if (event.target == popups[i]) {
            closePopup(popups[i].id);
        }
    }
}

function openPopup(id) {
    document.getElementById(id).style.display = "block";
}

function closePopup(id) {
    document.getElementById(id).style.display = "none";
}

function openSignupPopup() {
    openPopup("signupPopup");
}

function openAdminLoginPopup() {
    openPopup("adminLoginPopup");
}

function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var errorMessage = document.getElementById("passwordError");
    if (password != confirmPassword) {
        errorMessage.innerHTML = "Passwords do not match";
        return false;
    } else {
        errorMessage.innerHTML = "";
        return true;
    }
}

document.querySelectorAll('.popup-content .close').forEach(function(button) {
    button.addEventListener('click', function() {
        var popup = this.closest('.popup');
        closePopup(popup.id);
    });
});
