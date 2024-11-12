$(document).ready(function(){
    let formToSubmit = null;

    function showPopup(message, form) {
        $('#popup-message').text(message);
        formToSubmit = form;
        $('#custom-popup').addClass('flex').removeClass('hidden');
    }

    function closePopup() {
        $('#custom-popup').removeClass('flex').addClass('hidden');
        formToSubmit = null;
    }

    $('#confirm-btn').on('click', function(e) {
        console.log(formToSubmit)
        if (formToSubmit != null) {
            document.getElementById("click-to-submit").click()
        } else {
            window.history.back();
        }
    });

    $("#cancel-btn").click(function(){
        closePopup(); 
    });

    $("#submit").click(function(e){
        e.preventDefault(); 
        const form = $("#submit").closest('form');  
        form.submit()
        showPopup('Are you sure you want to submit these ratings?', form);  
    });

    $("#cancel").click(function(e){
        e.preventDefault();
        showPopup('Are you certain you want to discard these ratings?', null); 
    });
});
