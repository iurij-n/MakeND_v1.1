async function make_nd(){
    
    let dsp = document.querySelector('input[name="dsp_radio"]:checked').value;
    let date = document.getElementById("date_input");
        date.addEventListener("change", function(){});
    let admitting = document.getElementById('admitting_id').value;
    let issuing = document.getElementById('issuing_id').value;
    let approving = document.getElementById('approving_id').value;

    if (!(admitting == issuing) && !(issuing == approving) && !(approving == admitting)) {
        await eel.make_nd(dsp, date.value, admitting, issuing, approving)();
        }
    else {
        alert('Допускающий, выдающий и согласующий должны быть разными людьми.');
        }
}