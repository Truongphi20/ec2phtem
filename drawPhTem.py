import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import pandas as pd


def DraStart(index,s,e):
	# print(s,e)
	if pd.isna(e):
		pint = s
	else:
		pint = e
	# print(index,s,pint)
	plt.plot([s,pint], [index,index], color="blue",
						 linewidth=0.4,
						 marker="|",
						 markeredgewidth=1,
						 markersize=3,
						 mec = 'black',
						 mfc = 'None')

def DraOpt(index,s,e):
	if pd.isna(e):
		pint = s
	else:
		pint = e
	# print(index,s,pint)
	plt.plot([s,pint], [index,index], color="red",
					linewidth=0.4, 
					marker="o",
					markersize=1.5,
					mec = 'r',
					mfc = 'r')

def drawGraph(data):
	## Plot pH
	for word in ["temperature", "ph"]:
		ph_range = data[["organism",
						f'{word}Stability', f'{word}StabilityMaximum',
						f'{word}Optimum', f'{word}OptimumMaximum']]
		column_choose = [i for i in list(ph_range.columns) if i != "organism"]

		ph_data = data[["organism",
						f'{word}Stability', f'{word}StabilityMaximum',
						f'{word}Optimum', f'{word}OptimumMaximum']].\
						dropna(how="all", subset=column_choose).\
						reset_index(drop=True)
		# print(ph_data)
		organism = list(ph_data["organism"])
		# print(organism)

		### pH stability
		phsta_data = ph_data[[f'{word}Stability', f'{word}StabilityMaximum']].\
									dropna(subset=[f'{word}Stability']).\
									reset_index()
		# print(phsta_data)

		### pH optimal
		phopt_data = ph_data[[f'{word}Optimum', f'{word}OptimumMaximum']].\
									dropna(subset=[f'{word}Optimum']).\
									reset_index()
		# print(phopt_data)
		## Drawing

		plt.figure(figsize=(18,9))


		phsta_data.apply(lambda x: DraStart(x['index'], x[f"{word}Stability"], x[f'{word}StabilityMaximum']), axis=1)
		phopt_data.apply(lambda x: DraOpt(x['index'], x[f"{word}Optimum"], x[f'{word}OptimumMaximum']), axis=1)

		plt.yticks(range(len(organism)), organism, fontsize=4)
		plt.grid(axis='y', linewidth=0.3)

		red_line = mlines.Line2D([], [], color='red', marker='o',
		                          markersize=5, label=f'{word.capitalize()} Optimum')

		blue_line = mlines.Line2D([], [], color='blue', marker='|',
		                          markersize=5, mec = 'black', label=f'{word.capitalize()} Stability')

		plt.legend(handles=[red_line, blue_line])
		# plt.show()
		plt.tight_layout()
		plt.savefig(f"{word}.png", dpi=300)

# data = pd.read_csv("test.csv")
# print(data.head())
# drawGraph(data)

## Plot Temperture


