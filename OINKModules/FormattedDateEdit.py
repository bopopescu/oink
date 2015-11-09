import datetime
from PyQt4.QtGui import QDateEdit

class FormattedDateEdit(QDateEdit):
	def __init__(self, *args, **kwargs):
		super(FormattedDateEdit, self).__init__(*args, **kwargs)
		self.setDisplayFormat("ddd, dd-MMM-yyyy")
		self.setCalendarPopup(True)