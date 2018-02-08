# Echo server program
import socket
import sys

#HOST = '192.168.1.251'               # Symbolic name meaning all available interfaces
#HOST = '192.168.43.53'               # Symbolic name meaning all available interfaces
HOST = '172.30.59.49'               # Symbolic name meaning all available interfaces
PORT = 8080              # Arbitrary non-privileged port
s = None

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

HOST=get_lan_ip()
print("Ho preso come ip " + str(HOST))

while True:
	for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
								socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
		af, socktype, proto, canonname, sa = res
		try:
			s = socket.socket(af, socktype, proto)
		except socket.error as msg:
			s = None
			continue
		try:
			s.bind(sa)
			s.listen(1)
		except socket.error as msg:
			s.close()
			s = None
			continue
		break
	if s is None:
		print ('could not open socket')
		sys.exit(1)
	while True:
		conn, addr = s.accept()
		print ('Connected by', addr)
		data = conn.recv(1024)
		if data.endswith("\n"): data = data[:-1]
		print ("Ricevuto: " + str(data))
		if data == 'q':
			print ('il programma deve terminare')
			conn.send(data)
			conn.close()
			sys.exit(1)
		else:
#			conn.send(data + "\n")
			conn.send(data)
			print(data)
		#conn.flush()
	conn.close()