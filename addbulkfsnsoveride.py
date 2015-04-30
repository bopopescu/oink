import MOSES
import datetime

date_ = datetime.date(2015, 03, 27)

FSNs = ["9780070699717"]
for fsn in FSNs:
	MOSES.addOveride(fsn, date_, "bigbrother", "orwell")