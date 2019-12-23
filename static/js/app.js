$(document).ready(function () {
    $(".sidenav").sidenav();
    $(".hideit").click(function () {
        $(".hideme").slideToggle(1250);
    });
});
