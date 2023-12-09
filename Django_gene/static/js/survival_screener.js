$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

$(document).ready(function () {
    var dataTitle = 'genes'
    // Add a click event handler to the <a> elements
    $(".btn-toggle").click(function () {
        // Remove the 'active' class from all buttons
        $(".btn-toggle").removeClass("active");
        $(".btn-toggle").addClass("notActive");

        // Add the 'active' class to the clicked button
        $(this).removeClass("notActive");
        $(this).addClass("active");

        // Update the input value
        dataTitle = $(this).data("title");
        $("#DE_level").val(dataTitle);
    });

    $('#send').click(function(){
        const loadingContainer = $('#loading-container');
        const loadingbackground = $('#loading-background');
        const secondsCounter = $("#secondsCounter");
        loadingContainer.show();
        loadingbackground.show();
        secondsCounter.show();

        let seconds = 0;
        $("#secondsCounter").text(seconds);
        function countSeconds() {
            seconds++;
            $("#secondsCounter").text(seconds);
        }
        // Call countSeconds every second (1000 milliseconds)
        let intervalId = setInterval(countSeconds, 1000);

        $('#table').empty();

        var formData = {};
        $('input, select').each(function () {
            formData[this.name] = $(this).val();
        });
        formData['type'] = dataTitle
        console.log(formData);

        $.ajax({
            url: '/DEIso/ajax_survival_screener/', 
            data: formData,
            success: function(response){
                loadingContainer.hide();
                loadingbackground.hide();
                secondsCounter.hide();
                clearInterval(intervalId);

                table_data = response.table_data
                
                var datatable = $('<table>').attr('id', 'datatable').attr('class', 'table table-striped table-hover table-bordered').attr('style', 'width: 70%; text-align: center;').addClass('display');
                $('#table').append(datatable);

                dt = $('#datatable').DataTable({
                    lengthChange: false, // "Show X entries"
                    data: table_data,
                    columns: [
                        { data: 'name', title: 'Name' },
                        { data: 'p_value', title: 'P Value' },
                        { data: null, title: 'Site', render: function (data, type, row) {
                            return '<a href="http://127.0.0.1:8000/DEIso/survival_analyis/?text=' + data['name'] + '"><button class="btn btn-primary btn-site">site</button></a>';
                        }},
                    ],
                });

            }
        });

    });
});