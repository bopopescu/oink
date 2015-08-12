import os
from PyQt4.QtGui import QPushButton, QPixmap, QIcon
from PyQt4.QtCore import QSize

class RefreshButton(QPushButton):
	def __init__(self,*args, **kwargs):
		super(RefreshButton,self).__init__(*args, **kwargs)
		button_style = """
		QPushButton {
            color: white;
            font: 8pt;
		}
		QPushButton:hover {
			background-color: white;
            color: #008080;
            font: 04pt;
		}"""
		refresh_image_path = os.path.join("Images","refresh.png")
		if "OINKModules" in os.getcwd():
			refresh_image_path = os.path.join("..",refresh_image_path)
		refresh_pixmap = QPixmap(refresh_image_path)
		refresh_icon = QIcon(refresh_pixmap)
		#self.setStyleSheet(button_style)
		self.setIcon(refresh_icon)
		icon_size = refresh_pixmap.rect().size()
		button_size = QSize(icon_size.width()*1.5,icon_size.height()*1.5)
		self.setIconSize(refresh_pixmap.rect().size())
		self.setFixedSize(button_size)