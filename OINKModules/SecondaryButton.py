from PyQt4.QtGui import QPushButton

class SecondaryButton(QPushButton):
	def __init__(self,*args, **kwargs):
		super(SecondaryButton,self).__init__(*args, **kwargs)
		button_style = """
		QPushButton {
			background-color: white;
            color: black;
            font: 8pt;
		}
		QPushButton:hover {
			background-color: #FDDE2E;
            color: #0088D6;
            font: 10pt;
		}"""
		self.setStyleSheet(button_style)