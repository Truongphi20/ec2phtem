import check_login as login
import ec2phtem as ec
import drawPhTem as draw
import hashlib
import streamlit as st
import streamlit_ext as ste
from PIL import Image

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

		fig = plt.figure(figsize=(18,9))

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
		# plt.savefig(f"{word}.png", dpi=300)
		st.pyplot(fig)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.set_page_config(page_title="EC2phtem", page_icon='icon.png' ,layout='wide')

hide_streamlit_style="""
   <style>
   #MainMenu {visibility: hidden;}
   footer {visibility: hidden;}
   </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("**EC2phtem**")
st.markdown("""
   This tool is used to visualize pH and temperature range of organism's enzyme based\
    on the EC number of [Brenda database](https://www.brenda-enzymes.org/index.php).
   """)

col1, col2 = st.columns([2,4])
with col1:
	with st.form("formid"):

		emaila = st.text_input("Please enter your Email:", 
                           	key="email")
		passa = st.text_input('Your password:',
							key="password", type="password")
		ec_num = st.text_input('EC number:')

		submit = st.form_submit_button('Excute')

if submit:

	# emaila = "phi.nguyenphinguyen@hcmut.edu.vn"
	# passa = 'anh2cuchit'
	password = hashlib.sha256(passa.encode("utf-8")).hexdigest()
	email = emaila.replace("@", "\@")
	# ec_num = '2.4.1.25'

	with col2:
		input_array = [email, password, ec_num]

		if login.checkLogin(input_array):

			# st.write('Downloading the data. Please wait.')
			total_data = ec.ecRun(email, password, ec_num).reset_index()
			ste.download_button(
		       label="Download csv file",
		       data=convert_df(total_data),
		       file_name='data.csv',
		       mime='text/csv',
   			)
			drawGraph(total_data)

		else:
			st.write('Username or password is wrong, or account was not activated.')

		
# total_data.to_csv('test.csv')
# print(total_data)

