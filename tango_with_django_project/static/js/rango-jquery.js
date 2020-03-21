$(document).ready(() => {
    $('#about-btn').click(event => {
        alert('You clicked the button using JQuery!!')
    });

    $("p").hover( function() {
        $(this).css('color','red');
    }, function() {
        $(this).css('color','blue');
    });

    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = "I was here for an example and why the hell did you click that button instead of admiring me?"
        $("#msg").html(msgstr)
    });
});