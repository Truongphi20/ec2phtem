from zeep import Client
from zeep.transports import Transport
import zeep
import hashlib

# emaila = "phi.nguyenphinguyen@hcmut.edu.vn"
# passa = 'anh2cuchit'

def checkLogin(input_array):
	result = True
	wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
	client = Client(wsdl)
	ec_num = '3.4.22.32'

	phsta_parameters =  (input_array[0],input_array[1],f"ecNumber*{input_array[2]}",
	                     "phStability*", "phStabilityMaximum*",
	                     "commentary*", "organism*", "literature*")
	while True:
		try:
			result_phsta = client.service.getPhStability(*phsta_parameters)
		except zeep.exceptions.Fault:
			# print('Username or password is wrong, or account was not activated.')
			result = False
			break
		except zeep.exceptions.TransportError:
			# print("a")
			continue
		break

	return result

# print(checkLogin(emaila,passa))