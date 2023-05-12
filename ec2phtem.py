import pandas as pd
import concurrent.futures
import re
import requests
import hashlib
from zeep import Client
import numpy as np
from Bio import Entrez
import statistics
from getpass import getpass
from tqdm import tqdm

tqdm.pandas()

# emaila = input("Email address: ")
# passa = getpass()

wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
# password = hashlib.sha256(passa.encode("utf-8")).hexdigest()
# email = emaila.replace("@", "\@")
client = Client(wsdl)

# ec_num = input("EC number: ")
# print("\n")


def PubIDfromLitID(ec_num, ec_lit):
    lit_payload = f"https://www.brenda-enzymes.org/literature.php?e={ec_num}&r={ec_lit[0]}"
    lit_respond = requests.get(lit_payload).text
    #print(lit_respond)

    pub_id = re.findall(r"https:\/\/pubmed\.ncbi\.nlm\.nih\.gov\/([0-9]+)",lit_respond)
    #print(pub_id)
    
    if len(pub_id) > 0:
        return pub_id[0]
    else:
        return float("nan")

def MakeDDF(data, ec_num): #Create dataframe from extract list of dictionary
	if len(data) != 0:
		headers = list(data[0])
	    #print(headers)

		total_list = []
		for header in headers:
			tem = []
			for dic in data:
		   		tem.append(dic[header])                      
			total_list.append(tem)
		tata = pd.DataFrame(list(zip(*total_list)), columns=headers)
		tata = tata.drop("ecNumber", axis=1)
		tata["literature"] = tata["literature"].apply(lambda x: PubIDfromLitID(ec_num, x))
		#print(tata)
		return tata
	else:
		raise Exception("Empty data.")

def RepuScore_html(pub_id): # Get reputation score from html
    
    payload = f"https://pubmed.ncbi.nlm.nih.gov/?linkname=pubmed_pubmed_citedin&from_uid={pub_id}"
    page = requests.get(payload)
    html_doc = page.text
    total = re.findall(r"<span class=\"value\">(\d+)</span>", html_doc)
    if len(total) > 0:
        return int(total[0])
    else:
        return 0

def GetPhStability(email, password, ec_num):## Get pH stability
	
	phsta_parameters =  (email,password,f"ecNumber*{ec_num}",
	                     "phStability*", "phStabilityMaximum*",
	                     "commentary*", "organism*", "literature*")

	while True:
		try:
			result_phsta = client.service.getPhStability(*phsta_parameters)
			#print(result_phsta[0:2])
		except:
			continue
		break

	ph_sta = MakeDDF(result_phsta, ec_num)
	print("Get pH stability done!")
	return ph_sta

def GetPhRange(email, password, ec_num): ## Get pH range
	
	phra_parameters =  (email,password,f"ecNumber*{ec_num}",
	                     "phRange*", "phRangeMaximum*", 
	                    "commentary*", "organism*", "literature*")
	while True:
		try:
			result_phra = client.service.getPhRange(*phra_parameters)
			#print(result_phra[0:2])
		except:
			continue
		break

	ph_range = MakeDDF(result_phra, ec_num)
	print("Get pH range done!")
	return ph_range

def GetPhOptimal(email, password, ec_num): ## Get pH optimal
	
	phop_parameters =  (email,password,f"ecNumber*{ec_num}",
	                     "phOptimum*", "phOptimumMaximum*", 
	                    "commentary*", "organism*", "literature*")

	while True:
		try:
			result_phop = client.service.getPhOptimum(*phop_parameters)
			#print(result_phop[0:2])
		except:
			continue
		break

	ph_opt = MakeDDF(result_phop, ec_num)
	print("Get pH optimal done!")
	return ph_opt

def GetTemperatureOptimum(email, password, ec_num): ## Get Temperature Optimum
	
	temop_parameters =  (email,password,f"ecNumber*{ec_num}", 
	                     "temperatureOptimum*", "temperatureOptimumMaximum*", 
	                     "commentary*", "organism*", "literature*")
	while True:
		try:
			result_temop = client.service.getTemperatureOptimum(*temop_parameters)
			#print(result_temop[0:2])
		except:
			continue
		break

	tem_opt = MakeDDF(result_temop, ec_num)
	print("Get Temperature Optimum done!")
	return tem_opt

def GetTemperatureRange(email, password, ec_num): ## Get Temperature Range
	
	temran_parameters =  (email,password,f"ecNumber*{ec_num}",
	                      "temperatureRange*", "temperatureRangeMaximum*", 
	                      "commentary*", "organism*", "literature*")
	while True:
		try:
			result_temran = client.service.getTemperatureRange(*temran_parameters)
			#print(result_temran[0:2])
		except:
			continue
		break

	tem_range = MakeDDF(result_temran, ec_num)
	print("Get Temperature Range done!")
	return tem_range

def GetTemperatureStability(email, password, ec_num): ## Get Temperature Stability
	
	temsta_parameters =  (email,password,f"ecNumber*{ec_num}",
	                      "temperatureStability*", "temperatureStabilityMaximum*", 
	                      "commentary*", "organism*", "literature*")
	while True:
		try:
			result_temsta = client.service.getTemperatureStability(*temsta_parameters)
			#print(result_temsta[0:2])
		except:
			continue
		break

	tem_sta = MakeDDF(result_temsta, ec_num)
	print("Get Temperature Stability done!")
	return tem_sta

def ClearData(ph_range): # Preplace -999 and add reputation score
    
    collay = [i for i in ph_range.columns.values if i not in ['organism',"literature","commentary"]]
    ph_range[collay] = ph_range[collay].apply(pd.to_numeric, errors='coerce')
    
    ph_range = ph_range.replace(-999, np.nan)## Replace -999 value in phRange by NaN
    ph_range["reputation"] = ph_range["literature"].progress_apply(lambda x: RepuScore_html(x)) # Find reputation score
    return ph_range

def GroupByOrg(ph_range): # Group data by organism
    clear_ph_range = ClearData(ph_range)
    extr_ph_range = clear_ph_range.loc[:, ~clear_ph_range.columns.isin(["literature","commentary"])]
    tem1 = extr_ph_range.loc[:,~extr_ph_range.columns.isin(["reputation"])].groupby("organism").mean()
    tem2 = extr_ph_range.loc[:,["reputation","organism"]].groupby("organism").sum()
    total = pd.merge(tem1, tem2, how="outer", left_index=True, right_index=True)
    return total

def ProcessInfor(ph_range,ph_opt,ph_sta):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        thread1 = executor.submit(GroupByOrg,ph_range)
        thread2 = executor.submit(GroupByOrg,ph_sta)
        thread3 = executor.submit(GroupByOrg,ph_opt)

    extr_ph_range = thread1.result()
    extr_ph_sta = thread2.result()
    extr_ph_opt = thread3.result()
    
    total_repu1 = pd.merge(extr_ph_opt["reputation"], extr_ph_sta["reputation"],how="outer", left_index=True, right_index=True).sum(axis=1)
    total_repu1.name = "reputation"

    total_repu2 = pd.merge(total_repu1, extr_ph_range["reputation"],how="outer", left_index=True, right_index=True).sum(axis=1)
    total_repu2.name = "reputation"
    
    data1 = pd.merge(extr_ph_range.iloc[:,~extr_ph_range.columns.isin(["reputation"])],
         extr_ph_sta.iloc[:,~extr_ph_sta.columns.isin(["reputation"])],
         how="outer", left_index=True, right_index=True)
    data2 = pd.merge(data1,
             extr_ph_opt.iloc[:,~extr_ph_opt.columns.isin(["reputation"])],
             how="outer", left_index=True, right_index=True)
    
    total_data = pd.merge(data2, total_repu2, how="outer", left_index=True, right_index=True)
    return total_data 

def CompleteData(ph_data, tem_data):
	total_data = pd.merge(ph_data, tem_data, how="outer",
	                      left_index=True, right_index=True,
	                      suffixes=["_ph","_tem"])
	total_data["sum_reputation"] = total_data.loc[:,["reputation_ph", "reputation_tem"]].sum(axis=1)
	total_data.sort_values(by=['sum_reputation',"reputation_ph", "reputation_tem"], inplace=True, ascending=False)
	return(total_data)

def ecRun(email, password, ec_num):
	with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
		thread1 = executor.submit(GetPhStability,email, password, ec_num)
		thread2 = executor.submit(GetPhRange,email, password, ec_num)
		thread3 = executor.submit(GetPhOptimal,email, password, ec_num)


		thread4 = executor.submit(GetTemperatureOptimum,email, password, ec_num)
		thread5 = executor.submit(GetTemperatureRange,email, password, ec_num)
		thread6 = executor.submit(GetTemperatureStability,email, password, ec_num)

		ph_sta = thread1.result()
		ph_range = thread2.result()
		ph_opt = thread3.result()

		tem_opt = thread4.result()
		tem_range = thread5.result()
		tem_sta = thread6.result()

	print("\nCalculating Reputation Score...")

	ph_data = ProcessInfor(ph_range,ph_opt,ph_sta)
	tem_data = ProcessInfor(tem_range,tem_opt,tem_sta)


	print("\n\nCompleting...","\n")
	total_data = CompleteData(ph_data, tem_data)
	# total_data.to_csv(f"{ec_num}_data.csv")
	return total_data

# print(ecRun(email, password, ec_num))