$(document).ready(()=>{
    $('#show_password').change(()=>{
        if($('#show_password').is(':checked')) {
            $('#id_password').attr('type','text');
        }
        else {
            $('#id_password').attr('type','password');
        }
    })
})