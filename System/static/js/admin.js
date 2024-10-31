$(document).ready(function() {
    let formToSubmit = null;

    function showPopup(message, form) {
        $('#popup-message').text(message);
        formToSubmit = form;
        $('#custom-popup').css('display','flex');
        $('#custom-popup').css('z-index','1');
    }

    function closePopup() {
        $('#custom-popup').css('display','none');
        formToSubmit = null;
    }

    $('#confirm-btn').click(function(){
        if(formToSubmit){
            formToSubmit.submit()
        }
        else {
            alert("something is wrong")
            alert(formToSubmit)
        }
    })
    $('#cancel-btn').click(function(){
        closePopup()
    })

    $('button:contains("Confirm Changes")').on('click', function(e) {
        e.preventDefault();
        const form = $(this).closest('form');
        showPopup('Save Changes?', form);
    })

    $('#sort_by').change(function() {
        $("#sort-form").submit();
    });
    $('#sort_option').change(function() {
        $("#sort-form").submit();
    });
});
