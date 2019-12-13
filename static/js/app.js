$(document).ready(function () {
    $(".sidenav").sidenav();
    $(".hideit").click(function () {
        $("#hideme").toggle();
    });
    $('.collapsible').collapsible();
});
