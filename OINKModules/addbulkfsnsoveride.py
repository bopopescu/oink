import MOSES
import datetime

date_ = datetime.date(2015, 05, 8)

FSNs = ["HLMDCG9E4ZSGFZF9",]
for fsn in FSNs:
	try:
		MOSES.addOverride(fsn, date_, "bigbrother", "orwell")
		print "Processed %s" %fsn
	except Exception, e:
		print "Pass"
		print repr(e)
		