var selectedRecordId = 1;

function generatePassword() {
    let chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    let stringLength = 12;
    let randomString = '';
    for (let i = 0; i < stringLength; i++) {
        var rnum = Math.floor(Math.random() * chars.length);
        randomString += chars.substring(rnum,rnum+1);
    }
    return randomString;
}

function togglePasswordVisibility(id) {
    let passwordInput = document.getElementById("password" + id);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

function selectRecord(id) {
    let oldRecord = document.getElementById("record" + selectedRecordId);
    let newRecord = document.getElementById("record" + id);
    if (oldRecord != null) 
        oldRecord.style.backgroundColor = "#090909";
    newRecord.style.backgroundColor = "#328F32";
    selectedRecordId = id;
}

function openAddRecordWindow() {
    let addRecordWindow = window.open("/add-record", "PARMAN | Добавить поле...", "width=600,height=800");
    addRecordWindow.onbeforeunload = function() {
        location.reload();
    }
}

function openEditRecordWindow() {
    let editRecordWindow = window.open("/edit-record?id=" + selectedRecordId, "PARMAN | Изменить поле...", "width=600,height=800");
    editRecordWindow.onbeforeunload = function() {
        location.reload();
    }
}

function deleteRecord() {
    if (confirm("Вы уверены, что хотите удалить запись?")) {
        location.href = '/delete-record?record_id=' + selectedRecordId
    }
}