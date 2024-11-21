$(document).ready(function(){
    $('.django-ckeditor-widget').addClass('w-full')

    var formToSubmit = null;

    function showPopUp(form, message){
        $("#message").text(message)
        $("#pop-up").removeClass('hidden');
        window.scrollTo({ top: 0});
        $("body").addClass('overflow-x-hidden overflow-y-hidden')
        formToSubmit = form;
    }

    function hidePopUp(){
        $("#pop-up").addClass('hidden');
        $("body").removeClass('overflow-x-hidden overflow-y-hidden')
    }
    $("#confirm").click(()=>{
        if(formToSubmit != null) {
            formToSubmit.submit()
        }    
        else {
            window.history.back();
        }
    })

    $("#cancel").click(()=>{
        hidePopUp()
    })

    $("#save-button").click((e)=>{
        e.preventDefault()
        var form = $('#form');
        showPopUp(form,"Confirm Changes?")
    })

    $("#cancel-changes").click(()=>{
        showPopUp(null, "Exit and discard changes?")
    })
})