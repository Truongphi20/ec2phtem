import check_login as login
import ec2phtem as ec
import drawPhTem as draw
import hashlib
import streamlit as st
import streamlit_ext as ste


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
			st.write('Checked log in.')

			st.write('Downloading the data. Please wait.')
			total_data = ec.ecRun(email, password, ec_num).reset_index()
			ste.download_button(
		       label="Download csv file",
		       data=convert_df(total_data),
		       file_name='data.csv',
		       mime='text/csv',
   )
		else:
			st.write('Username or password is wrong, or account was not activated.')

		
# total_data.to_csv('test.csv')
# print(total_data)

# draw.drawGraph(total_data)