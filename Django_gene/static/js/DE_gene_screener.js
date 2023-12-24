$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

// 當頁面載入完成時執行
document.addEventListener("DOMContentLoaded", function () {
    // 獲取兩個下拉選單的元素
    var condition1Select = document.getElementById("condition1");
    var condition2Select = document.getElementById("condition2");

    // 為兩個下拉選單添加事件監聽器
    condition1Select.addEventListener("change", handleConditionChange);
    condition2Select.addEventListener("change", handleConditionChange);

    // 初始時執行一次
    handleConditionChange();
});

// 處理下拉選單改變的函數
function handleConditionChange() {
    var condition1Select = document.getElementById("condition1");
    var condition2Select = document.getElementById("condition2");

    // 如果其中一個選擇了 "Narmal"，則禁用或隱藏另一個選項的 "Narmal"
    if (condition1Select.value === "N") {
        disableOption(condition2Select, "N");
    } else {
        enableOption(condition2Select, "N");
    }

    if (condition2Select.value === "N") {
        disableOption(condition1Select, "N");
    } else {
        enableOption(condition1Select, "N");
    }

    if (condition1Select.value === "1") {
        disableOption(condition2Select, "1");
    } else {
        enableOption(condition2Select, "1");
    }

    if (condition2Select.value === "1") {
        disableOption(condition1Select, "1");
    } else {
        enableOption(condition1Select, "1");
    }

    if (condition1Select.value === "2") {
        disableOption(condition2Select, "2");
    } else {
        enableOption(condition2Select, "2");
    }

    if (condition2Select.value === "2") {
        disableOption(condition1Select, "2");
    } else {
        enableOption(condition1Select, "2");
    }

    if (condition1Select.value === "3") {
        disableOption(condition2Select, "3");
    } else {
        enableOption(condition2Select, "3");
    }

    if (condition2Select.value === "3") {
        disableOption(condition1Select, "3");
    } else {
        enableOption(condition1Select, "3");
    }

    if (condition1Select.value === "4") {
        disableOption(condition2Select, "4");
    } else {
        enableOption(condition2Select, "4");
    }

    if (condition2Select.value === "4") {
        disableOption(condition1Select, "4");
    } else {
        enableOption(condition1Select, "4");
    }
}

// 禁用指定值的選項
function disableOption(selectElement, value) {
    for (var i = 0; i < selectElement.options.length; i++) {
        if (selectElement.options[i].value === value) {
            selectElement.options[i].disabled = true;
            break;
        }
    }
}

// 啟用指定值的選項
function enableOption(selectElement, value) {
    for (var i = 0; i < selectElement.options.length; i++) {
        if (selectElement.options[i].value === value) {
            selectElement.options[i].disabled = false;
            break;
        }
    }
}

function userInput(Condition){
    // 創建 table 元素
    var table = $('<table>').addClass('table table-hover').css('width', '90%').attr('align', 'center');

    // 創建 tbody 元素
    var tbody = $('<tbody>');

    // 添加第一行
    var row1 = $('<tr>');
    row1.append($('<th>').addClass('active').text('Search').css('color', 'black'));
    row1.append($('<td>').text('DE genes'));
    tbody.append(row1);
    
    // 添加第二行
    var row2 = $('<tr>');
    row2.append($('<th>').addClass('active').attr('width', '50%').text('The selected cancer').css('color', 'black'));
    row2.append($('<td>').text('Liver cancer'));
    tbody.append(row2);

    // 添加第三行
    var row3 = $('<tr>');
    row3.append($('<th>').addClass('active').text('Two compared cancer stages').css('color', 'black'));
    row3.append($('<td>').text(Condition).css('font-size', '12px'));
    tbody.append(row3);

    // 將 tbody 添加到 table
    table.append(tbody);

    // 將 table 添加到 body
    $('#userInput').append(table);
}

function defineExpression(conditions_compare_text, Statistical_Significance){
    // 創建 table 元素
    var table = $('<table>').addClass('table table-hover').css('width', '90%').attr('align', 'center');

    // 創建 tbody 元素
    var tbody = $('<tbody>');

    // 添加第一行
    var row1 = $('<tr>');
    row1.append($('<th>').addClass('active').text('Fold Change of Average FPKM').css('color', 'black'));
    row1.append($('<td>').text(conditions_compare_text));
    tbody.append(row1);
    
    // 添加第二行
    var row2 = $('<tr>');
    row2.append($('<th>').addClass('active').text('Statistical Significance').css('color', 'black'));
    row2.append($('<td>').text(Statistical_Significance));
    tbody.append(row2);

    // 將 tbody 添加到 table
    table.append(tbody);

    // 將 table 添加到 body
    $('#defineExpression').append(table);
}



$(document).ready(function(){
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
    
    $("#send").click(function(){
        $('#result').css('visibility', 'hidden');

        $('#table').empty();
        $('#userInput').empty();
        $('#defineExpression').empty();

        // 捕獲表單的數據
        var formData = {};
        $('input, select').each(function () {
            formData[this.name] = $(this).val();
        });
        formData['type'] = dataTitle
        console.log(formData);
        
        $.ajax({
            url: '/DEIso/ajax_DE_gene_screener/',
            data: formData,
            success:function(response) {

                compared_cancer_stages = response.compared_cancer_stages
                userInput(compared_cancer_stages)
                conditions_compare_text = response.conditions_compare_text
                Statistical_Significance_text = response.Statistical_Significance_text
                defineExpression(conditions_compare_text, Statistical_Significance_text)

                var datatable = $('<table>').attr('id', 'screenResult').attr('class', 'table table-striped table-hover table-bordered').attr('style', 'width: 100%;');
                $('#table').append(datatable);

                table_data = response.table_data
                
                dt = $('#screenResult').DataTable({
                    "lengthChange": true, // 允许用户选择每页显示多少条数据
                    "lengthMenu": [10, 25, 50, 100], // 自定义可选择的每页条数
                    "searching": true, // 關閉搜索功能
                    "scrollX": true,  // 啟用水平滾動
                    "scrollY": '80vh',  // 設置垂直滾動高度，可以更改為您需要的值
                    "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                    "paging": true,  // 要啟用分頁才能自訂每頁筆數
                    "data": table_data,
                    "columns": [
                        { data: 'gene', title: 'Gene' },
                        { data: 'value_1', title: 'Condition1 Avg FPKM' },
                        { data: 'value_2', title: 'Condition2 Avg FPKM' },
                        { data: 'fold_change', title: 'Fold Change' },
                        { data: 'q_value', title: 'q-value' },
                    ],
                    "dom": 'Bfrtip',
                    "buttons": [
                        {
                            extend: 'csv',
                            text: 'Download',
                            action: function() {
                                // 創建下載連結
                                var link = document.createElement('a');
                                link.href = '/static/csv/DE_gene_output.csv';  // 指向服务器上的 CSV 文件路径
                                link.download = 'DE_gene_output.csv';
                
                                // 觸發點擊連結
                                document.body.appendChild(link);
                                link.click();
                
                                // 移除連結
                                document.body.removeChild(link);
                            }
                        }
                    ]
                });

                $('#result').css('visibility', '');
            }
        });
    
    });
})