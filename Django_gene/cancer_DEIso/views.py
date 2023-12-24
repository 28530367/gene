from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from survival_analysisv3.survival_analysis import *
import base64
import math
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

media_path = settings.MEDIA_DIRS_PATH

def survival_analyis(request):

    return render(request, 'survival_analyis.html', locals())

def ajax_survival_analyis(request):
    plot = Survival_plot()
    input_project = "TCGA-ACC"
    input_primary_site = "Adrenal_Gland_Adrenocortical_Carcinoma"
    input_primary_site = input_primary_site.replace("_", " ")
    input_type = request.POST['input_type']
    input_name = request.POST['input_element']
    Low_Percentile = request.POST['input_low']
    High_Percentile = request.POST['input_high']
    survival_days = request.POST['input_days']
    survival_select = request.POST['samples_select'].replace("_", " ")
    check = int(request.POST['check'])
    
    if check == 1:
        if plot.survival_max_days(input_project, input_name, input_type, survival_select)+5 < float(survival_days) or 0 > float(survival_days):
            print(f"maxmium days is {plot.survival_max_days(input_project, input_name, input_type, survival_select)}")
            print("input days error")
            response = {
                'error': f"maxmium days is {plot.survival_max_days(input_project, input_name, input_type, survival_select)}",
            }
        else: 
            plot_arg = {
                'project':"TCGA-ACC",
                'primary_site': input_primary_site,
                'search_by': input_type,
                'GT_input': input_name,
                "random_id": "",
                'Low_Percentile': Low_Percentile,
                'High_Percentile': High_Percentile,
                'survival_days': survival_days,
                'survival_select': survival_select,
            }
            plot.survival_plot_realtime(plot_arg)

            with open('/home/shouweihuang/Lab_Training/gene/Django_gene/static/image/survival_plot.png', 'rb') as f:
                image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            response = {
                'error': '',
                'image': encoded_image
            }

    elif check == 0:
        maxmium_day = plot.survival_max_days(input_project, input_name, input_type, survival_select)
        plot_arg = {
            'project':"TCGA-ACC",
            'primary_site': input_primary_site,
            'search_by': input_type,
            'GT_input': input_name,
            "random_id": "",
            'Low_Percentile': Low_Percentile,
            'High_Percentile': High_Percentile,
            'survival_days': maxmium_day,
            'survival_select': survival_select,
        }
        plot.survival_plot_realtime(plot_arg)

        with open('/home/shouweihuang/Lab_Training/gene/Django_gene/static/image/survival_plot.png', 'rb') as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        response = {
            'error': '',
            'image': encoded_image,
            'maxmium_day': int(maxmium_day),
        }
        
    return JsonResponse(response)

'----------------------------------------------------------survival_screener---------------------------------------------------------------'
def survival_screener(request):

    return render(request, 'survival_screener.html', locals())

def ajax_survival_screener(request):
    screener = Survival_screener()

    input_project = "TCGA-ACC"
    input_primary_site = "Adrenal_Gland_Adrenocortical_Carcinoma"
    input_primary_site = input_primary_site.replace("_", " ")
    input_type = request.POST['type']
    low_Percentile = int(request.POST['Low_Percentile'])
    high_Percentile = int(request.POST['High_Percentile'])
    max_p_value = float(request.POST['max_p_value'])
    survival_select = request.POST['samples_select'].replace("_", " ")

    plot_arg = {
        'project': input_project,
        'primary_site': input_primary_site,
        'search_by': input_type,
        'Low_Percentile': low_Percentile,
        'High_Percentile': high_Percentile,
        'max_p_value': max_p_value,
        'survival_select': survival_select,
    }
    table_data = screener.controller(plot_arg)

    response = {
        'table_data': table_data,
    }

    return JsonResponse(response)

'----------------------------------------------------------DE_GENES_SCREENER---------------------------------------------------------------'
def DE_gene_screener_web(request):

    return render(request, 'DE_gene_screener.html')

def DE_gene_screener_main(request):
    input_project = 'TCGA-LIHC'
    input_type = 'genes'
    condition1 = request.POST['condition1']
    condition2 = request.POST['condition2']

    conditions_compare = request.POST['conditions_compare']
    fold_change = float(request.POST['fold_change'])

    test = request.POST['test']
    direction = request.POST['direction']
    qvalue = float(request.POST['qvalue'])

    file_path = f"{media_path}/DE_gene_data/{input_project}_{condition1}_{condition2}_{input_type}.csv"
    df = pd.read_csv(file_path)

     # 對 log2(fold_change) 取 2的次方倍
    df['log2(fold_change)'] = np.exp2(df['log2(fold_change)'])

    if condition1 == 'N':
        condition1_text = 'Normal (n=50)'
        csv_condition1_text = 'normal'
    elif condition1 == '1':
        condition1_text = 'Stage I (n=171)'
        csv_condition1_text = 'stage i'
    elif condition1 == '2':
        condition1_text = 'Stage II (n=86)'
        csv_condition1_text = 'stage ii'
    elif condition1 == '3':
        condition1_text = 'Stage III (n=85)'
        csv_condition1_text = 'stage iii'
    elif condition1 == '4':
        condition1_text = 'Stage IV (n=5)'
        csv_condition1_text = 'stage iv'

    if condition2 == 'N':
        condition2_text = 'Normal (n=50)'
        csv_condition2_text = 'normal'
    elif condition2 == '1':
        condition2_text = 'Stage I (n=171)'
        csv_condition2_text = 'stage i'
    elif condition2 == '2':
        condition2_text = 'Stage II (n=86)'
        csv_condition2_text = 'stage ii'
    elif condition2 == '3':
        condition2_text = 'Stage III (n=85)'
        csv_condition2_text = 'stage iii'
    elif condition2 == '4':
        condition2_text = 'Stage IV (n=5)'
        csv_condition2_text = 'stage iv'

    compared_cancer_stages = f"Condition2 [{condition2_text}] vs. Condition1 [{condition1_text}]"

    # 根據條件進行篩選
    if conditions_compare == 'ge':
        df = df[df['log2(fold_change)'] >= fold_change]
        conditions_compare_text = f"Condition2 / Condition1 ≥ {fold_change}"
    elif conditions_compare == 'le':
        df = df[df['log2(fold_change)'] <= fold_change]
        conditions_compare_text = f"Condition2 / Condition1 ≤ {fold_change}"

    test_column = f"{test}_{direction}"

    test_text = test.replace('_', ' ');
    if direction == 'greater':
        df = df[df[test_column] < qvalue]
        direction_text = 'Greater (Condition2 ≥ Condition1)'
    elif direction == 'less':
        df = df[df[test_column] > qvalue]
        direction_text = 'Less (Condition2 ≤ Condition1)'
    
    Statistical_Significance_text = f"{test_text}, {direction_text}, q-value < {qvalue}"

    selected_columns = ['gene', 'value_1', 'value_2', 'log2(fold_change)', 'q_value']
    df_table_data = df[selected_columns]

    # 定義轉換函數
    def format_scientific(value):
        return '{:.3e}'.format(value)
    # 將指定欄位轉換為科學記號
    df_table_data['q_value'] = df_table_data['q_value'].apply(format_scientific)

    format_columns = ['value_1', 'value_2', 'log2(fold_change)']
    # 定義轉換函數
    def format_to_three_decimals(value):
        return '{:.3f}'.format(value)
    # 將指定欄位轉換為小數點後三位
    df_table_data[format_columns] = df_table_data[format_columns].applymap(format_to_three_decimals)

    df_table_data.rename(columns={'log2(fold_change)':'fold_change'}, inplace=True)

    # print(df)
    table_data = df_table_data.to_dict(orient='records')

    # 生成 .csv
    header_content = [
        ['Primary site', "Liver"],
        ['Condition1', csv_condition1_text],
        ['Condition2', csv_condition2_text],
        ['Differential Expression level', 'DE genes'],
        [f"Fold Change ({csv_condition1_text}/{csv_condition2_text})", f"≥ {fold_change} Fold"],
        ['Hypothesis Test', f"{test_text} ({direction}) significance level: {qvalue}"],
        []
    ]
    
    selected_columns = ['gene', 'value_1', 'value_2', 'log2(fold_change)', test_column]
    new_column_names = {'gene': 'Gene', 'value_1': 'Condition1 Avg FPKM', 'value_2': 'Condition2 Avg FPKM', 'log2(fold_change)': 'Fold Change', test_column: f"{test_text} ({direction})"}

    gene_data_df = df[selected_columns]
    gene_data_df.rename(columns=new_column_names, inplace=True)

    column_names = gene_data_df.columns.tolist()
    gene_data_list = [column_names] + gene_data_df.values.tolist()
    output_list = header_content + gene_data_list

    filename = f"/home/shouweihuang/Lab_Training/gene/Django_gene/static/csv/DE_gene_output.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(output_list)

    response = {
        'table_data': table_data,
        'compared_cancer_stages': compared_cancer_stages,
        'conditions_compare_text': conditions_compare_text,
        'Statistical_Significance_text': Statistical_Significance_text,
        'header_content': header_content,
    }
    return JsonResponse(response)