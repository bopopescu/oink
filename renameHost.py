import os

if __name__ == "__main__":

	host_file_locations = ["Data",os.path.join("OINKModules","Data")]
	file_name = "hostid.txt"
	local_host = "localhost"
	server = "172.17.188.139"
	host_id_files = [os.path.join(location, file_name) for location in host_file_locations]
	for host_id_file in host_id_files:
		current_host_id = open(host_id_file, "r").read()
		print "Current Host ID is %s" %current_host_id
		file_handler = open(host_id_file,"w")
		file_handler.truncate()
		if current_host_id == local_host:
			file_handler.write(server)
		else:
			file_handler.write(local_host)
		file_handler.close()
		current_host_id = open(host_id_file, "r").read()
		print "Host ID is %s" %current_host_id
		