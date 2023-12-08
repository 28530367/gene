$(document).ready(function () {
    // Add a click event handler to the <a> elements
    $(".btn-toggle").click(function () {
        // Remove the 'active' class from all buttons
        $(".btn-toggle").removeClass("active");
        $(".btn-toggle").addClass("notActive");

        // Add the 'active' class to the clicked button
        $(this).removeClass("notActive");
        $(this).addClass("active");

        // Update the input value
        var dataTitle = $(this).data("title");
        $("#DE_level").val(dataTitle);
    });
});