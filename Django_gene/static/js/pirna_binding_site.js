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
            var piRNAs = response.piRNA 
            $.each(str_pirna_table, function(key, value) {
                pirna_table.push(value);
            });

            console.log(pirna_table)
            pirna_table = $('#pirna_table').DataTable({
                "lengthChange": true, // "Show X entries"
                "searching": true, // 搜索功能
                "scrollX": true,  // 啟用水平滾動
                "scrollY": '70vh',  // 設置垂直滾動高度，可以更改為您需要的值
                "paging": true,
                "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                "paging": true,  // 禁用分頁（如果不需要的話）
                "pageLength": 9,
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
            var table = $('#piRNATable').DataTable({
                "paging": true,
                "ordering": false,
                "scrollX": false,  // 啟用水平滾動
                "info": false,
                "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                "pageLength": 6,
            });

            piRNAs.forEach(function(piRNA) {
                table.row.add([`<input type="checkbox" class="piRNA-checkbox" value="${piRNA}">`, piRNA]);
            });
        
            table.draw();
        
            // Add event listener for "Select All" checkbox
            $('#selectAll').on('change', function() {
                // Check/uncheck checkboxes on the current page
                $('.piRNA-checkbox').prop('checked', this.checked);
            
                // Check/uncheck checkboxes on other pages
                if (this.checked) {
                    table.rows().nodes().to$().find('.piRNA-checkbox').prop('checked', true);
                } else {
                    table.rows().nodes().to$().find('.piRNA-checkbox').prop('checked', false);
                }
            });


        },
        error: function(){
            alert('something wrong!')
        },       
    });
});
