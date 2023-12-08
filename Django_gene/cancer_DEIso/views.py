from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from survival_analysisv3.survival_analysis import *
import base64

def survival_analyis(request):

    return render(request, 'survival_analyis.html', locals())

def ajax_survival_analyis(request):
    plot = Survival_plot()
    input_project = "TCGA-ACC"
    input_primary_site = "Adrenal_Gland_Adrenocortical_Carcinoma"
    input_primary_site = input_primary_site.replace("_", " ")
    input_type = "genes"
    input_name = request.POST['input_element']
    Low_Percentile = request.POST['input_low']
    High_Percentile = request.POST['input_high']
    survival_days = request.POST['input_days']
    survival_select = request.POST['samples_select'].replace("_", " ")
    	
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

    return JsonResponse(response)

'----------------------------------------------------------survival_screener---------------------------------------------------------------'
def survival_screener(request):

    return render(request, 'survival_screener.html', locals())