$(document).ready(function () {
    $(".sidenav").sidenav();
    $(".hideit").click(function () {
        $(".hideme").fadeToggle('slow', 'linear');
    });
});
