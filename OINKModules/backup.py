import MOSES

if __name__ == "__main__":
	try:
		MOSES.takeOINKBackup()
	except Exception, e:
		print "Backup failed."
		print repr(e)
		raise
	raw_input("Press Enter to exit.")