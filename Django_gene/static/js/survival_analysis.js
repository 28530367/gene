$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

function download_btn() {
    var csvFilePath = '/static/csv/Survival_Profile.csv';
    var link = $('<a>', {
        href: csvFilePath,
        download: 'Survival_Profile.csv'
    });
    // Create a button element
    var button = $('<button>', {
        type: 'button',
        class: 'btn btn-danger',
        style: 'margin-bottom: 15px;'
    });
    // Create a span element
    var span = $('<span>', {
        class: 'glyphicon glyphicon-download-alt',
        'aria-hidden': 'true',
        text: ' Download Data'
    });

    button.append(span);
    link.append(button);

    $('#Download_csv').append(link);
}

$(document).ready(function(){
    $('.submit').click(function(){
        const loadingContainer = $('#loading-container');
        const loadingbackground = $('#loading-background')
        loadingContainer.show();
        loadingbackground.show();

        var formData = {};
        $('input, select').each(function () {
            formData[this.name] = $(this).val();
        });
        $('#image').empty();
        $('#Download_csv').empty();
        $.ajax({
            url: '/DEIso/ajax_survival_analyis/', 
            data: formData,
            success: function(response){
                loadingContainer.hide();
                loadingbackground.hide();
                if (response.error == '') {
                    $('#output').css('visibility', '');
                    download_btn()
                    $('#image').html('<img src="data:image/png;base64,' + response.image + '">');
                } else {
                    alert('Error : ' + response.error)
                } 
            }
        });
    });
});