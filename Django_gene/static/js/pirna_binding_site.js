$(document).ready(function(){
    var urlParams = new URLSearchParams(window.location.search);
    var textParam = urlParams.get('text');
    $.ajax({
        url: '/web_tool/ajax_pirna_binding_site/', 
        type: 'GET',
        data: {text: textParam},
        success: function(response){

            $('#pirna_table').html("")

            var str_pirna_table = JSON.parse(response.pirna_table);
            var pirna_table = [];
            $.each(str_pirna_table, function(key, value) {
                pirna_table.push(value);
            });

            console.log(pirna_table)
            pirna_table = $('#pirna_table').DataTable({
                "lengthChange": true, // 關閉 "Show X entries"
                "searching": true, // 關閉搜索功能
                "scrollX": true,  // 啟用水平滾動
                "scrollY": '70vh',  // 設置垂直滾動高度，可以更改為您需要的值
                "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                "paging": false,  // 禁用分頁（如果不需要的話）
                "data": pirna_table,
                "columns": [
                    { data: 'id', title: "CLASH READ ID" },
                    { data: 'Regulator RNA Name', title: "piRNA" },
                    { data: 'algorithm', title: "CLASH algorithm" },
                    { data: 'Read Count', title: "hybrid count" },
                    { data: 'Target RNA Region Found in CLASH Read', title: "CLASH identified region" },
                    { data: 'pirscan min_ex binding site', title: "predicted binding site from pirScan" },
                    { data: 'pirscan min_ex score', title: "pirScan targeting score" },
                    { data: 'WT_WAGO_pirscan min_ex25_22G', title: "WT_WAGO1 22G(pirScan)" },
                    { data: 'PRG1MUT_WAGO1_22G_pirscan min_ex25', title: "prg-1 mutant WAGO1 22G(pirScan)" },
                    { data: 'WAGO1_22G_pirscan min_ex25 foldchange', title: "22G-RNA fold change(prg-1/WT)(pirScan)" },
                    { data: 'pirscan min_ex Target sequence', title: "pairing of binding site from pirScan" },
                    { data: 'RNAup min_ex binding site', title: "predicted binding site from RNAup" },
                    { data: 'RNAup min_ex score', title: "RNAup binding energy" },
                    { data: 'WT_WAGO_RNAup min_ex25_22G', title: "WT_WAGO1 22G(RNAup)" },
                    { data: 'PRG1MUT_WAGO1_22G_RNAup min_ex25', title: "prg-1 mutant WAGO1 22G(RNAup)" },
                    { data: 'WAGO1_22G_RNAup min_ex25 foldchange', title: "22G-RNA fold change(prg-1/WT)(RNAup)" },
                    { data: 'RNAup min_ex Target RNA sequence', title: "pairing of binding site from RNAup" },
                ],
                "columnDefs": [
                    {
                        "targets": [10, 16],
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).addClass('sequence');
                        }
                    }
                ],
            });
            var form = $("#check_form"); // 取得表單元素

                $.each(response.piRNA, function (index, labelText) {
                    var label = $("<label></label>"); // 建立 <label> 元素
                    label.text(labelText); // 設定 <label> 元素的文字內容

                    var input = $("<input type='checkbox' />"); // 建立 <input> 元素，設定類型為文字
                    input.attr('id', labelText); // 設定 id，你可以自訂 id 名稱
                    input.attr('name', labelText); // 設定 name，這裡使用相同的 name
                    input.attr('value', labelText); // 設定 value，這裡將其設定為 labelText 的值
                    
                    // 將 <label> 和 <input> 加入表單
                    form.append(input);
                    form.append(label);
                    form.append("<br>");
                });

        },
        error: function(){
            alert('something wrong!')
        },       
    });
});
