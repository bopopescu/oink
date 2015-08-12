from PyQt4.QtGui import QPushButton

class PrimaryButton(QPushButton):
	def __init__(self,*args, **kwargs):
		super(PrimaryButton,self).__init__(*args, **kwargs)
		button_style = """
		QPushButton {
			background-color: #0088D6;
            color: white;
            font: 10pt;
		}
		QPushButton:hover {
			background-color: #FDDE2E;
            color: #0088D6;
            font: 11pt;
		}"""
		self.setStyleSheet(button_style)