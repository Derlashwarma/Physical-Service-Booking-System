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

    $('button:contains("Accept")').on('click', function(e) {
        e.preventDefault(); 
        const form = $(this).closest('form');
        showPopup("Are you sure you want to accept the application?", form);
    });
    $('button:contains("Reject")').on('click', function(e) {
        e.preventDefault(); 
        const form = $(this).closest('form');
        showPopup("Discard changes?", form);
    });

    $('#confirm-btn').on('click', function() {
        if (formToSubmit) {
            formToSubmit.submit(); 
        }
        else{
            const urlSegments = window.location.href.split('/');
            const jobId = urlSegments[urlSegments.length - 1];
            const baseUrl = window.location.origin;
            window.location.href = `${baseUrl}/job/jobs/${jobId}`; 
        }
        closePopup();
    });

    $('#cancel-btn').on('click', function() {
        closePopup();
    });

    $('#save-changes').on('click', function(e) {
        e.preventDefault(); 
        const form = $(this).closest('form');
        showPopup("Save changes?", form);
    });

    $('#discard-changes').on('click', function(e) {
        e.preventDefault(); 
        showPopup("Are you sure you want to discard changes?", null);
    });

    $('#delete-job').on('click', function(e) {
        e.preventDefault(); 
        const form = $(this).closest('form');
        showPopup("Are you sure you want to delete this job post?", form);
    });

    $("#post").on('click',function(e){
        e.preventDefault();
        const form = $(this).closest('form');
        showPopup("Confirm Job Post?", form)
    })
    $("#apply").on('click',function(e){
        e.preventDefault();
        const form = $(this).closest('form');
        showPopup("Submit Job Application?", form)
    })

    $("#go-back").click(() => {
        history.back();
      });
});
