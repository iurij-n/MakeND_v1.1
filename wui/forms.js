var admittingParent = document.querySelector('form#admitting_list_form');
var issuingParent = document.querySelector('form#issuing_list_form');
var approvingParent = document.querySelector('form#approving_list_form');

eel.expose(generate_forms);
function generate_forms(admittingArray, admittingValueArray, issuingArray, issuingValueArray, approvingArray, approvingValueArray) {

var selectAdmittingList = document.createElement("select");
selectAdmittingList.id = "admitting_id";
admittingParent.appendChild(selectAdmittingList);

for (var i = 0; i < admittingArray.length; i++) {
    var option = document.createElement("option");
    option.text = admittingArray[i];
    option.value = admittingValueArray[i];
    selectAdmittingList.appendChild(option);
}

var selectIssuingList = document.createElement("select");
selectIssuingList.id = "issuing_id";
issuingParent.appendChild(selectIssuingList);

for (var i = 0; i < issuingArray.length; i++) {
    var option = document.createElement("option");
    option.text = issuingArray[i];
    option.value = issuingValueArray[i];
    selectIssuingList.appendChild(option);
}

var selectApprovingList = document.createElement("select");
selectApprovingList.id = "approving_id";
approvingParent.appendChild(selectApprovingList);

for (var i = 0; i < approvingArray.length; i++) {
    var option = document.createElement("option");
    option.text = approvingArray[i];
    option.value = approvingValueArray[i];
    selectApprovingList.appendChild(option);
}

}