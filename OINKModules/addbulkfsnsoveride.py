import MOSES
import datetime

date_ = datetime.date(2015, 04, 27)

FSNs = ["SFFEYW35YWH26CHS","SFFEYYFAEK8ZUY8H"]
for fsn in FSNs:
	try:
		MOSES.addOverride(fsn, date_, "bigbrother", "orwell")
		print "Processed %s" %fsn
	except Exception, e:
		print "Pass"
		print repr(e)
		