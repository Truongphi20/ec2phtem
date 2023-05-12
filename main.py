import check_login as login
import ec2phtem as ec
import drawPhTem as draw
import hashlib
import streamlit as st

st.set_page_config(page_title="View query", page_icon='icon.png' ,layout='wide')

emaila = "phi.nguyenphinguyen@hcmut.edu.vn"
passa = 'anh2cuchit'
password = hashlib.sha256(passa.encode("utf-8")).hexdigest()
email = emaila.replace("@", "\@")
ec_num = '2.4.1.25'

input_array = [email, password, ec_num]

if login.checkLogin(input_array):
	print('Checked log in.')
else:
	print('Username or password is wrong, or account was not activated.')

# total_data = ec.ecRun(email, password, ec_num).reset_index()
# total_data.to_csv('test.csv')
# print(total_data)

# draw.drawGraph(total_data)