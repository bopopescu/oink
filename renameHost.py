import os
import psutil
from subprocess import check_output
if __name__ == "__main__":

	host_file_locations = ["Data",os.path.join("OINKModules","Data")]
	file_name = "hostid.txt"
	local_host = "localhost"
	server = "172.17.188.141"
	host_id_files = [os.path.join(location, file_name) for location in host_file_locations]
	for host_id_file in host_id_files:
		current_host_id = open(host_id_file, "r").read()
		print "Current Host ID in %s is %s" %(host_id_file,current_host_id)
		file_handler = open(host_id_file,"w")
		file_handler.truncate()
		if current_host_id == local_host:
			file_handler.write(server)
		else:
			file_handler.write(local_host)
		file_handler.close()
		current_host_id = open(host_id_file, "r").read()
		print "Host ID in %s changed to %s" %(host_id_file,current_host_id)
	print "Checking MySQL56 status."
	process_names = [str(psutil.Process(i).name()) for i in psutil.pids()]
#	print process_names
	if current_host_id == "localhost":
		if "mysqld.exe" not in process_names:
			check_output("net start MySQL56",shell=True)
			print "Starting MySQL56!"
	else:
		if "mysqld.exe" in process_names:
			check_output("net stop MySQL56",shell=True)
			print "MySQL56 has been stopped!"
	raw_input("Hit ENTER to exit> ")
		