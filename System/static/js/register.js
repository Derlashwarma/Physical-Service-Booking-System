$(document).ready(()=>{
    $("#client").click(()=>{
        $("#id_is_worker_0").prop("checked", true);
        $("#client").addClass('border-green-700')
        $("#worker").removeClass('border-green-700')
    })
    $("#worker").click(()=>{
        $("#id_is_worker_1").prop("checked", true);
        $("#worker").addClass('border-green-700')
        $("#client").removeClass('border-green-700')
    })
    
})