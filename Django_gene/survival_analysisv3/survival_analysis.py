import numpy as np
from argparse import ArgumentParser
import os
import sys
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import csv
from functools import partial
import multiprocessing
import time
from lifelines.statistics import logrank_test

file_path = os.path.dirname(os.path.abspath(__file__))

class Survival_plot():
	def __init__(self) -> None:
		pass
	def survival_data_realtime(self, project, column_table,search_by,GT_input):
		stage_dict = {
			'stage i' : 'stage_1',
			'stage ii' : 'stage_2',
			'stage iii' : 'stage_3',
			'stage iv' : 'stage_4',
		}
		df = pd.read_csv(f"{file_path}/data/{project}_{search_by}_FPKM_Cufflinks.csv")
		# df = df.rename(columns=lambda x: x.replace('"', ''))
		table_name = column_table.split('|')[1]
		primary_key = 'gene_name' if search_by == 'genes' else 'isoform_name'
		selected_columns = [primary_key]
		if column_table.split('|')[0] != 'all stage':
			print(column_table.split('|')[0])
			# selected_columns += stage_dict[column_table.split('|')[0]] if column_table.split('|')[0] != 'all stage' else ','.join(stage_dict.values())
			selected_columns += [stage_dict[column_table.split('|')[0]]]
		else:
			data_columns = df.columns.tolist()
			data_columns = data_columns[1:]
			selected_columns = [primary_key]
			for e in data_columns:
				if e != 'normal' and e !='all_stage' and e != 'pvalue(normal_allstage)' and e != 'pvalue(allstage_normal)':
					selected_columns.append(e)
			# selected_columns = ','.join(selected_columns)
		df = df[selected_columns]
		df_result = df[df[f"{primary_key}"] == GT_input]
		result = df_result.drop(columns= [f"{primary_key}"]).values.tolist()[0]
		return result

	def survival_plot(self, T1,E1,T2,E2,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,survival_days,survival_select):
		# from lifelines.estimation import KaplanMeierFitter
		from lifelines import KaplanMeierFitter
		from lifelines.statistics import logrank_test
		matplotlib.use('Agg')

		plot_path = f"/home/shouweihuang/Lab_Training/gene/Django_gene/static/image/survival_plot.png"
		try:
			os.remove(plot_path)
		except OSError:
			pass

		kmf = KaplanMeierFitter()
		dpi = 100

		logrank_result = logrank_test(T1, T2, E1, E2)
		logrank_p_value = logrank_result.p_value
		logrank_test_statistic = logrank_result.test_statistic

		if T2 != [] and E2 != []:
			kmf.fit(T2, event_observed=E2, label='Low Expression (n={}, {}%)'.format(len(T2),Low_Percentile))
			ax = kmf.plot(ci_show=False,color='green',show_censors=True, figsize=(1200/dpi, 800/dpi))

		if T1 != [] and E1 != []:
			kmf.fit(T1, event_observed=E1, label='High Expression (n={}, {}%)'.format(len(T1),High_Percentile))
			kmf.plot(ax=ax,ci_show=False,color='red',show_censors=True) 

		font = {'family' : 'verdana'}
		matplotlib.rc('font', **font)
		plt.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.06)

		plt.title("%s"%GT_input)
		ax.text(0.1, 0.2, 'Low Percentile: {}%\nHigh Percentile: {}%\nDays: {}\nCondition: {}'.format(Low_Percentile,High_Percentile,survival_days,survival_select), horizontalalignment='left',verticalalignment='center', transform=ax.transAxes, bbox={'facecolor':'#F5F5F5', 'pad':5},fontsize=10)
		ax.text(0.1, 0.1, 'logrank pvalue: {}'.format(round(logrank_p_value,3)), horizontalalignment='left',verticalalignment='center', transform=ax.transAxes, bbox={'facecolor':'#F5F5F5', 'pad':5},fontsize=10)

		ax.set_ylim(ymin=0)

		ax.set_xlabel('Days',fontsize=12)
		ax.set_ylabel('Survival probability',fontsize=12)

		ax.grid(True)
		gridlines = ax.get_xgridlines() + ax.get_ygridlines()
		for line in gridlines:
			line.set_linestyle('-.')

		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)

		plt.savefig(plot_path,dpi=dpi)
		plt.close()
		
		return logrank_p_value

	def survival_download(self, T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,survival_select):
		output_data = [
						['Query: %s'%(GT_input)],
						['Primary site: %s'%(primary_site)],
						['Low Percentile: %s'%(Low_Percentile)],
						['High Percentile: %s'%(High_Percentile)],
						['Condition: %s'%(survival_select)],
						[],
						['Patient','Days','Status','Expression','Group']
					]
		for idx,row in enumerate(low_case):
			Status = 'Alive' if E2[idx] == False else 'Dead'
			output_data += [[row,T2[idx],Status,low_FPKM[idx],'Low']]
		for idx,row in enumerate(high_case):
			Status = 'Alive' if E1[idx] == False else 'Dead'
			output_data += [[row,T1[idx],Status,high_FPKM[idx],'High']]
		print('survival_download')

		# download file
		filename=f"Survival_Profile.csv"
		with open(f"/home/shouweihuang/Lab_Training/gene/Django_gene/static/csv/{filename}", "w") as f:
			writer = csv.writer(f)
			for e in output_data:
				writer.writerow(e)
		
		return output_data
	
	def survival_plot_realtime(self, request:dict):
		project = request['project']
		# ex: TCGA-COAD
		primary_site = request['primary_site']
		# ex: Adrenal Gland Adrenocortical Carcinoma
		search_by = request['search_by']
		GT_input = request['GT_input']
		random_id = request['random_id']
		Low_Percentile = request['Low_Percentile']
		High_Percentile = request['High_Percentile']
		survival_days = request['survival_days']
		survival_select = request['survival_select']
		# stage : all stage, stage i, stage ii, stage iii, stage iv
		table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
		column_table = "%s|%s"%(survival_select,table_name)
	#### patched by t50504
		survival_data = self.survival_data_realtime(project, column_table,search_by,GT_input)
		survival_str = ""
		case_id_list = []

		FPKM_list = [float(y.split("|")[0]) for x in survival_data for y in x.split(',')]
		low_quartile = np.percentile(FPKM_list, float(Low_Percentile))
		high_quartile = np.percentile(FPKM_list, 100-float(High_Percentile))

		T1 = [] #high 存活天數
		E1 = [] #high 是否死亡
		T2 = []
		E2 = []
		high_case = []
		low_case = []
		high_FPKM = []
		low_FPKM = []

		for stage in survival_data:
			for info in stage.split(','):
				FPKM = float(info.split('|')[0])
				case_id = info.split('|')[1]

				survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
				# print(case_id,survival_times)
				survival_events = False if info.split('|')[3] == 'alive' else True #是否死亡
				if FPKM > high_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(survival_days):
					T1 += [survival_times]
					E1 += [survival_events]
					case_id_list += [case_id]
					high_case += [case_id]
					high_FPKM += [FPKM]
				elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(survival_days):
					T2 += [survival_times]
					E2 += [survival_events]
					case_id_list += [case_id]
					low_case += [case_id]
					low_FPKM += [FPKM]

		if (T2 != [] and E2 != []) and (T1 != [] and E1 != []):
			self.survival_plot(T1,E1,T2,E2,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,max(T1+T2),survival_select)
			survival_download = self.survival_download(T1,E1,T2,E2,high_case,low_case,high_FPKM,low_FPKM,GT_input,primary_site,random_id,Low_Percentile,High_Percentile,survival_select)
			# request.session["Survival_Profile_%s_%s_%s_%s"%(primary_site.replace('(','').replace(')',''),Low_Percentile,High_Percentile,random_id)] = survival_download
		else:
			survival_str = ' Survival analysis is not available for '+GT_input+' since more than half of the samples have zero expression.'

	def survival_max_days(self ,project, GT_input, search_by, survival_select) -> float:

		# project = request.POST['project']
		# GT_input = request.POST['GT_input']
		# search_by = request.POST['search_by']
		# survival_select = request.POST['survival_select']
		# project = request['project']
		# GT_input = request['GT_input']
		# search_by = request['search_by']
		# survival_select = request['survival_select']

		table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
		column_table = "%s|%s"%(survival_select,table_name)

		survival_data = "".join(self.survival_data_realtime(project, column_table,search_by,GT_input)).split(",")
		# survival_days = [float(y.split("|")[2]) for x in survival_data for y in x.split(',')]
		# survival_days = list(map(lambda x:x.split("|")[2],survival_data))
		# df = pd.read_csv(f"{file_path}/data/{project}_{search_by}_FPKM_Cufflinks.csv")
		
		# survival_data = 
		survival_days = [float(x.split("|")[2]) for x in survival_data if x.split("|")[2] != 'None']
		max_survival_days = max(survival_days)
		return max_survival_days
		# return JsonResponse({"max_survival_days": max_survival_days})

class Survival_screener():
	def __init__(self) -> None:
		pass

	def survival_read_csv(self, project, column_table, search_by):
		stage_dict = {
			'stage i' : 'stage_1',
			'stage ii' : 'stage_2',
			'stage iii' : 'stage_3',
			'stage iv' : 'stage_4',
		}
		df = pd.read_csv(f"{file_path}/data/{project}_{search_by}_FPKM_Cufflinks.csv")

		primary_key = 'gene_name' if search_by == 'genes' else 'isoform_name'
		selected_columns = [primary_key]

		if column_table.split('|')[0] != 'all stage':
			print(column_table.split('|')[0])
			selected_columns += [stage_dict[column_table.split('|')[0]]]
		else:
			data_columns = df.columns.tolist()
			data_columns = data_columns[1:]
			selected_columns = [primary_key]
			for e in data_columns:
				if e != 'normal' and e !='all_stage' and e != 'pvalue(normal_allstage)' and e != 'pvalue(allstage_normal)':
					selected_columns.append(e)
					
		df = df[selected_columns]
		result = df.values.tolist()

		return result

	def get_logrank_p_value(self, record, Low_Percentile, High_Percentile, search_by, max_p_value):

		primary_key = 'gene_name' if search_by == 'genes' else 'isoform_name'
		# Extract the first element (gene_name)
		primary_name = record[0]

		# Concatenate the remaining elements into a single string
		concatenated_values = ','.join(record[1:])

		FPKM_list = [float(x.split("|")[0]) for x in concatenated_values.split(',')]
		low_quartile = np.percentile(FPKM_list, float(Low_Percentile))
		high_quartile = np.percentile(FPKM_list, 100-float(High_Percentile))

		T1 = [] #high 存活天數
		E1 = [] #high 是否死亡
		T2 = []
		E2 = []

		for info in concatenated_values.split(','):
			FPKM = float(info.split('|')[0])

			survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
			# print(case_id,survival_times)
			survival_events = False if info.split('|')[3] == 'alive' else True #是否死亡
			if FPKM > high_quartile and (survival_times != 0 and survival_times != 'None'):
				T1 += [survival_times]
				E1 += [survival_events]
			elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None'):
				T2 += [survival_times]
				E2 += [survival_events]	
		try:
			logrank_result = logrank_test(T1, T2, E1, E2)
			logrank_p_value = logrank_result.p_value
		except:
			logrank_p_value = 1

		if logrank_p_value <= max_p_value:
			scientific_format_logrank_p_value = '{:.3e}'.format(logrank_p_value)
			result = {'name': primary_name, 'p_value': scientific_format_logrank_p_value}
			return result
		
		return 
	
	def controller(self, request:dict):

		search_by = request['search_by']
		project = request['project']
		Low_Percentile = request['Low_Percentile']
		High_Percentile = request['High_Percentile']
		survival_select = request['survival_select']
		max_p_value = request['max_p_value']

		table_name = '%s_%s_FPKM_Cufflinks'%(project,search_by)
		column_table = "%s|%s"%(survival_select,table_name)

		survival_data = self.survival_read_csv(project, column_table, search_by)

		pool_obj = multiprocessing.Pool(multiprocessing.cpu_count())
		partial_get_logrank_p_value = partial(self.get_logrank_p_value, Low_Percentile=Low_Percentile, High_Percentile=High_Percentile, search_by=search_by, max_p_value=max_p_value)
		result = pool_obj.map(partial_get_logrank_p_value, survival_data)

		return result

if __name__ == "__main__":

	ss = Survival_screener()
	## cancer ➔ project table
	# ex : python3 survival_analysis.py -p TCGA-ACC --primary_site Adrenal_Gland_Adrenocortical_Carcinoma -t genes -n KIF23 --Low_Percentile 50 --High_Percentile 50 --survival_days 4628 --survival_select all_stage
	# ex : python3 survival_analysis.py -p TCGA-ACC --primary_site Adrenal_Gland_Adrenocortical_Carcinoma -t isoforms -n NM_000014 --Low_Percentile 50 --High_Percentile 50 --survival_days 4673 --survival_select all_stage
	# stage argument :stage_i, stage_ii, stage_iii, stage_iv
	input_project = "TCGA-ACC"
	input_primary_site = "Adrenal_Gland_Adrenocortical_Carcinoma"
	input_primary_site = input_primary_site.replace("_", " ")
	input_type = "genes"
	input_name = "AAGAB"
	Low_Percentile = 50
	High_Percentile = 50
	survival_days = 4628
	survival_select = "all_stage"
	survival_select = survival_select.replace("_", " ")
	input_p_value = 0.5

	plot_arg = {
		# 'project':args.project,
		'project':"TCGA-ACC",
		'primary_site': input_primary_site,
		'search_by': input_type,
		'GT_input': input_name,
		"random_id": "",
		'Low_Percentile': Low_Percentile,
		'High_Percentile': High_Percentile,
		'survival_days': survival_days,
		'survival_select': survival_select,
		'max_p_value': input_p_value
	}
	start_time = time.time()

	result = ss.controller(plot_arg)
	
	end_time = time.time()
	print(result)
	print(end_time-start_time)






