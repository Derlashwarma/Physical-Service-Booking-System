$(document).ready(function () {
    var element = $('#animate');
    var position = element[0].getBoundingClientRect();

    if (position.top < window.innerHeight && position.bottom >= 0) {
        element.addClass('visible');
        alert('visible');
    } else {
        element.removeClass('visible');
    }
    setInterval(() => {
        console.log(position)
    }, 500);
});
