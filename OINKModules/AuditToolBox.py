#!usr/bin/python2
# -*- coding: utf-8 -*-
#Bacon Widget Class definition
from PyQt4 import QtGui
from PrimaryButton import PrimaryButton
from SecondaryButton import SecondaryButton
from RefreshButton import RefreshButton

class AuditToolBox(QtGui.QWidget):
	def __init__(self):
		super(AuditToolBox, self).__init__()
		self.createUI()

	def createUI(self):
		self.audit_queue_button = PrimaryButton("Audit Queue\n(Audits Pending)")
		self.audit_queue_button.setToolTip("Open Audit Queue and Audit Articles")
		self.TNA_button = SecondaryButton("TNA")
		self.TNA_button.setToolTip("Open Training Needs Analysis Report")
		self.raw_data_button = SecondaryButton("Raw Data")
		self.raw_data_button.setToolTip("View Raw Data")
		self.ask_your_editor_button = SecondaryButton("Ask Your Editor Queries\n(Questions Open)")
		self.ask_your_editor_button.setToolTip("Open the ask your editor portal to answer open questions.")
		self.refresh_reports_button = RefreshButton()
		self.refresh_reports_button.setToolTip("Refresh all visible reports")

		self.layout = QtGui.QGridLayout()
		self.layout.addWidget(self.audit_queue_button,0,0,1,2)
		self.layout.addWidget(self.TNA_button,0,2,1,1)
		self.layout.addWidget(self.raw_data_button,1,0,1,1)
		self.layout.addWidget(self.ask_your_editor_button,1,1,1,1)
		self.layout.addWidget(self.refresh_reports_button,1,2,1,1)

		self.setLayout(self.layout)
