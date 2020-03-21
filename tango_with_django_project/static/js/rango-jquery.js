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
        msgstr = "This is ridiculous by the way!"
        $("#msg").html(msgstr)
    });
});