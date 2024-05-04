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

$(document).ready(function(){
 
    // Initialize select2
    $("#SelExample").select2();
    $("#SelExample").select2("val", "4");
  $('#SelExample option:selected').text('Vizag');
    // Read selected option
    $('#but_read').click(function(){
      var username = $('#SelExample option:selected').text();
      var userid = $('#SelExample').val();
  
      $('#result').text("id : " + userid + ", name : " + username);
    });
  });
  
  $(document).ready(function(){
   
    // Initialize select2
    $("#SelExample2").select2();
    $("#SelExample2").select2("val", "4");
  $('#SelExample2 option:selected').text('Vizag');
    // Read selected option
    $('#but_read2').click(function(){
      var username = $('#SelExample2 option:selected').text();
      var userid = $('#SelExample2').val();
  
      $('#result2').text("id : " + userid + ", name : " + username);
    });
  });
  
  
  