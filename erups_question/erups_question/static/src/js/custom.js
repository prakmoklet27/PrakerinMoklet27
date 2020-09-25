// require('jquery-validation');
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    // $('.search-select').selectpicker();
});
function allowNumbersOnly(e) {
    var code = (e.which) ? e.which : e.keyCode;
    if (code > 31 && (code < 48 || code > 57)) {
        e.preventDefault();
    }
}

// var textbox = document.getElementById("regisNumber");
// if (textbox) {
//     function setInputFilter(textbox, inputFilter) {
//         ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
//             textbox.addEventListener(event, function () {
//                 if (inputFilter(this.value)) {
//                     this.oldValue = this.value;
//                     this.oldSelectionStart = this.selectionStart;
//                     this.oldSelectionEnd = this.selectionEnd;
//                 } else if (this.hasOwnProperty("oldValue")) {
//                     this.value = this.oldValue;
//                     this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
//                 } else {
//                     this.value = "";
//                 }
//             });
//         });
//     }
// }

// setInputFilter(document.getElementById("regisNumber"), function (value) {
//     return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 99999999999);
// });

// setInputFilter(document.getElementById("sahamNumber"), function (value) {
//     return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 99999999999);
// });

$(document).on("click", "#delete", function () {
    $('#Modalconfirm').modal('hide');
});
