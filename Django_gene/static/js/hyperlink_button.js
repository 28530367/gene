function search_matrix_id(MatrixID) {
    var form = document.createElement('form');
    form.method = 'post';
    form.action = 'http://plantpan.itps.ncku.edu.tw/plantpan4/TF_info.php';  //server端頁面的url
    form.target = '_blank';

    var input1 = document.createElement('input');
    input1.type = 'hidden';
    input1.name = 'GeneID';
    input1.value = MatrixID;

    form.appendChild(input1);

    // 將表單添加到 body 中
    document.body.appendChild(form);

    // 提交表單
    form.submit();
}

$(document).ready(function(){
    $('.button').click(function(){
        var buttonText = $(this).text();
        search_matrix_id(buttonText)
    });
})