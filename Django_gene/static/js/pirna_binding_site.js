function piRNAdatatable(output_data) {
    if ($.fn.DataTable.isDataTable('#pirna_table')) {
        $('#pirna_table').DataTable().destroy();
    }
    // Clear the table content, if necessary
    $('#pirna_table').empty();
    $('#pirna_table tbody').off('click', '.id-button');
    pirna_table = $('#pirna_table').DataTable({
        "lengthChange": true, // "Show X entries"
        "searching": true, // 搜索功能
        "scrollX": true,  // 啟用水平滾動
        "scrollY": '70vh',  // 設置垂直滾動高度，可以更改為您需要的值
        "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
        "paging": true,  // 禁用分頁（如果不需要的話）
        "pageLength": 9,
        "data": output_data,
        "columns": [
            {
                data: 'id',
                title: "CLASH Read ID",
                render: function (data, type, row, meta) {
                    if (type === 'display') {
                        return '<button class="id-button" data-id="' + data + '">' + data + '</button>';
                    }
                    return data;
                }
            },
            { data: 'regulator_rna_name', title: "piRNA" },
            { data: 'algorithm', title: "CLASH algorithm" },
            { data: 'read_count', title: "hybrid count" },
            { data: 'target_rna_region_found_in_clash_read', title: "CLASH identified region" },
            { data: 'pirscan_min_ex_binding_site', title: "predicted binding site from pirScan" },
            { data: 'pirscan_min_ex_score', title: "pirScan targeting score" },
            { data: 'wt_wago_pirscan_min_ex25_22g', title: "WT_WAGO1 22G(pirScan)" },
            { data: 'prg1mut_wago1_22g_pirscan_min_ex25', title: "prg-1 mutant WAGO1 22G(pirScan)" },
            { data: 'wago1_22g_pirscan_min_ex25_foldchange', title: "22G-RNA fold change(prg-1/WT)(pirScan)" },
            { data: 'pirscan_min_ex_target_sequence', title: "pairing of binding site from pirScan" },
            { data: 'rnaup_min_ex_binding_site', title: "predicted binding site from RNAup" },
            { data: 'rnaup_min_ex_score', title: "RNAup binding energy" },
            { data: 'wt_wago_rnaup_min_ex25_22g', title: "WT_WAGO1 22G(RNAup)" },
            { data: 'prg1mut_wago1_22g_rnaup_min_ex25', title: "prg-1 mutant WAGO1 22G(RNAup)" },
            { data: 'wago1_22g_rnaup_min_ex25_foldchange', title: "22G-RNA fold change(prg-1/WT)(RNAup)" },
            { data: 'rnaup_min_ex_target_rna_sequence', title: "pairing of binding site from RNAup" },
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
    $('#pirna_table tbody').on('click', '.id-button', function () {
        var id = $(this).data('id');
        var buttonPosition = $(this).offset();
        showFloatingTable(id, output_data, buttonPosition,);
    });
    function showFloatingTable(id, output_data, buttonPosition) {
        fetchTableDataById(id, output_data).then(function (data) {
            populateFloatingTable(data);
            var floatingTable = $('#floating-table');
            floatingTable.css({
                position: 'absolute',
                top: buttonPosition.top -220,
                left: buttonPosition.left + 550,
            });
            floatingTable.toggle();
        });
    }
    function populateFloatingTable(data) {
        var table = $('#dynamic-table').DataTable({
            destroy: true,
            "lengthChange": false, // 關閉 "Show X entries"
            "searching": false, // 關閉搜索功能
            "info": false,
            "data": output_data,
            "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
            "paging": false,  // 禁用分頁（如果不需要的話）
            "columns": [
                { data: 'id', title: 'CLASH read ID' },
                { data: 'clash_read', title: 'CLASH read sequence' },
                { data: 'region_on_clash_read_identified_as_regulator_rna', title: 'Region identified by piRNA' },
                { data: 'region_on_clash_read_identified_as_target_rna', title: 'Region identified by target RNA' }
            ]
        });
        table.clear().draw();
        data.forEach(function (rowData) {
            table.row.add(rowData).draw();
        });
    }
    function fetchTableDataById(id, output_data) {
        return new Promise(function (resolve) {
            var foundData = output_data.find(function (item) {
                return item.id === id;
            });
            var data = foundData ? [foundData] : [];

            resolve(data);
        });
    }
}

function splicedsvg(xmaxElement, spliced_svgdata, spliced_svg_colorindex, spliced_exon_svgdata, spliced_exon_svg_colorindex) {

    // SVG 元素的尺寸
    var svgWidth = 2000;
    var svgHeight = 125;

    // 創建 spliced_svg 
    var spliced_svg = d3.select("#spliced_svg_div") // Selecting the container element
        .append("svg") // Appending an SVG within the selected container
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .attr("id", "spliced_svg");

    // 計算 x 軸的比例尺
    var spliced_xScale = d3.scaleLinear()
        .domain([1, xmaxElement])
        .range([150, svgWidth-300]);

    // 創建總長度矩形
    spliced_svg.selectAll("rect")
        .data(spliced_svgdata)
        .enter()
        .append("rect")
        .attr("x", function(d, i) { return spliced_xScale(d[0]); }) // 根據數值計算 x 位置
        .attr("y", 50)
        .attr("width", function(d, i) { return spliced_xScale(d[1]+1) - spliced_xScale(d[0]); })
        .attr("height", 30)
        .attr("fill",function(d, i) { 
            if (spliced_svg_colorindex[i] == 1) {
                return "lightgray";
            } else {
                return "lightblue";
            }
        })
        .attr("stroke", "black") // 添加黑色邊框
        .attr("stroke-width", 1); // 設置邊框寬度為1像素

    // 創建 spliced_exon 矩形
    spliced_svg.selectAll("rect.exon-rect")
    .data(spliced_exon_svgdata)
    .enter()
    .append("rect")
    .attr("x", function(d, i) { return spliced_xScale(d[0]); }) // 根據數值計算 x 位置
    .attr("y", 90)
    .attr("width", function(d, i) { return spliced_xScale(d[1]+1) - spliced_xScale(d[0]); })
    .attr("height", 30)
    .attr("fill", function(d, i) {
        if (spliced_exon_svg_colorindex[i] == 1) {
            return "yellow";
        } else if (spliced_exon_svg_colorindex[i] == 2) {
            return "orange";
        }
    })
    .attr("stroke", "black") // 添加黑色邊框
    .attr("stroke-width", 1); // 設置邊框寬度為1像素
    
    var customTickValues = [1];
    for (var i = 100; i <= xmaxElement; i += 100) {
        customTickValues.push(i);
    }
    customTickValues.push(xmaxElement)

    // 創建一個 x 軸生成函數
    var pliced_xAxis = d3.axisTop(spliced_xScale)
        .tickValues(customTickValues);

    // 在 SVG 中創建一個群組元素，用於容納 x 軸
    spliced_svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0, 45)") 
        .call(pliced_xAxis); // 將 x 軸應用到這個群組元素上
}

function pirnasvg(xmaxElement, pirna_svgdata, pirna_svgdata_index) {

    var max = Math.max.apply(null, pirna_svgdata_index);
    var svgWidth = 2000;
    var svgHeight = (max+1)*18;

    var pirna_svg = d3.select("#pirna_svg_div") // Selecting the container element
        .append("svg") // Appending an SVG within the selected container
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .attr("id", "pirna_svg");

    // 計算 x 軸的比例尺
    var pirna_xScale = d3.scaleLinear()
        .domain([1, xmaxElement])
        .range([150, svgWidth-300]);

    pirna_svg.selectAll("rect.pirna_svg-rect")
        .data(pirna_svgdata)
        .enter()
        .append("rect")
        .attr("x", function(d) { return pirna_xScale(d[0]); }) // 根據數值計算 x 位置
        .attr("y", function(d, i) { return 18 * pirna_svgdata_index[i]; })
        .attr("width", function(d) { return pirna_xScale(d[1]+1) - pirna_xScale(d[0]); })
        .attr("height", 15)
        .attr("fill", "red")
        .attr("stroke", "black") // 添加黑色邊框
        .attr("stroke-width", 1) // 設置邊框寬度為1像素
}

function wtwagoipsvg(xmaxElement, wt_wagoip_svgdata) {

    let Column2 = wt_wagoip_svgdata.map(row => row[2]);
    let ymaxElement = Math.max(...Column2);

    var svgWidth = 2000;
    var svgHeight = 350;

    var wt_wagoip_svg = d3.select("#wt_wagoip_svg_div") // Selecting the container element
        .append("svg") // Appending an SVG within the selected container
        .attr("width", svgWidth)
        .attr("height", svgHeight)
        .attr("id", "wt_wagoip_svg");

    // 計算 x 軸的比例尺
    var wt_wagoip_xScale = d3.scaleLinear()
        .domain([1, xmaxElement])
        .range([150, svgWidth-300]);

    // 計算 y 軸的比例尺
    var wt_wagoip_yScale = d3.scaleLinear()
        .domain([0, ymaxElement])
        .range([0, svgHeight-70]);

    wt_wagoip_svg.selectAll("rect.wt_wagoip_svg-rect")
        .data(wt_wagoip_svgdata)
        .enter()
        .append("rect")
        .attr("x", function(d) { return wt_wagoip_xScale(d[0]); }) // 根據數值計算 x 位置
        .attr("y", 50)
        .attr("width", function(d) { return wt_wagoip_xScale(d[1]+1) - wt_wagoip_xScale(d[0]); })
        .attr("height", function(d) { return wt_wagoip_yScale(d[2]); })
        .attr("fill", "darkblue")

    var customTickValues = [1];
    for (var i = 100; i <= xmaxElement; i += 100) {
        customTickValues.push(i);
    }
    customTickValues.push(xmaxElement)

    // 創建一個 x 軸生成函數
    var wt_wagoip_xAxis = d3.axisTop(wt_wagoip_xScale)
        .tickValues(customTickValues);

    // 在 SVG 中創建一個群組元素，用於容納 x 軸
    wt_wagoip_svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0, 45)") 
        .call(wt_wagoip_xAxis); // 將 x 軸應用到這個群組元素上

}

$(document).ready(function(){

    var urlParams = new URLSearchParams(window.location.search);
    var textParam = urlParams.get('text');

    var xmaxElement
    $.ajax({
        url: '/web_tool/ajax_pirna_binding_site/', 
        type: 'GET',
        data: {text: textParam},
        success: function(response){

            var str_pirna_table = JSON.parse(response.pirna_table);
            var pirna_table = [];
            var piRNAs = response.piRNA 
            $.each(str_pirna_table, function(key, value) {
                pirna_table.push(value);
            });

            var spliced_svgdata = response.spliced_svgdata
            var spliced_svg_colorindex = response.spliced_svg_colorindex
            var spliced_exon_svgdata = response.spliced_exon_svgdata
            var spliced_exon_svg_colorindex= response.spliced_exon_svg_colorindex
            var pirna_svgdata = response.pirna_svgdata
            var pirna_svgdata_index = response.pirna_svgdata_index
            var wt_wagoip_svgdata = response.wt_wagoip_svgdata
            xmaxElement = d3.max(spliced_svgdata, function(d) {
                return d[1];
            });

            piRNAdatatable(pirna_table)

            var piRNA_Search_table = $('#piRNA_Search_Table').DataTable({
                "paging": true,
                "ordering": false,
                "scrollX": false,  // 啟用水平滾動
                "info": false,
                "scrollCollapse": true,  // 如果內容不足，則隱藏滾動條
                "pageLength": 6,
            });
            
            piRNAs.forEach(function(piRNA) {
                piRNA_Search_table.row.add([`<input type="checkbox" class="piRNA-checkbox" value="${piRNA}" checked="checked">`, piRNA]);
            });
        
            piRNA_Search_table.draw();
        
            // Add event listener for "Select All" checkbox
            $('#selectAll').on('change', function() {
                // Check/uncheck checkboxes on the current page
                $('.piRNA-checkbox').prop('checked', this.checked);
            
                // Check/uncheck checkboxes on other pages
                if (this.checked) {
                    piRNA_Search_table.rows().nodes().to$().find('.piRNA-checkbox').prop('checked', true);
                } else {
                    piRNA_Search_table.rows().nodes().to$().find('.piRNA-checkbox').prop('checked', false);
                }
            });

            splicedsvg(xmaxElement, spliced_svgdata, spliced_svg_colorindex, spliced_exon_svgdata, spliced_exon_svg_colorindex)

            pirnasvg(xmaxElement, pirna_svgdata, pirna_svgdata_index)
            
            wtwagoipsvg(xmaxElement, wt_wagoip_svgdata)
        },
        error: function(){
            alert('something wrong!')
        },       
    });
    

    $('#piRNA_Search_Table').on('change', function() {
        var selectedValues = [];
        var piRNA_Search_table = $('#piRNA_Search_Table').DataTable();
        var currentPage = piRNA_Search_table.page.info().page;
    
        for (let i = 0; i < piRNA_Search_table.page.info().pages; i++) {
            piRNA_Search_table.page(i).draw(false);
            $('.piRNA-checkbox:checked').each(function() {
                selectedValues.push($(this).val());
            });
        }

        piRNA_Search_table.page(currentPage).draw('page');

        var selectedValuesStr = selectedValues.join(', ');

        $.ajax({
            url: '/web_tool/ajax_pirna_binding_site_search/', 
            type: 'GET',
            data: {
                selected: selectedValuesStr
            },
            success: function(response){

                if ($.fn.DataTable.isDataTable('#pirna_table')) {
                    $('#pirna_table').DataTable().destroy();
                }
                
                // Clear the table content, if necessary
                $('#pirna_table').empty();

                $('.unstable_svg').empty();

                var str_pirna_table = JSON.parse(response.pirna_table);
                var pirna_table = [];
                $.each(str_pirna_table, function(key, value) {
                    pirna_table.push(value);
                });

                var pirna_svgdata = response.pirna_svgdata;
                var pirna_svgdata_index = response.pirna_svgdata_index;

                piRNAdatatable(pirna_table)

                pirnasvg(xmaxElement, pirna_svgdata, pirna_svgdata_index)

            },
            error: function(){
                alert('something wrong!')
            },       
        });
    });
});
