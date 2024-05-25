function togglePasswordVisibility(id) {
    let passwordInput = document.getElementById("password" + id);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

function openAddRecordWindow() {
    let AddRecordWindow = window.open("/add_record", "PARMAN | Добавить поле...", "width=600,height=800");
    AddRecordWindow.onbeforeunload = function() {
        location.reload();
    }
}