#!/usr/bin/python2
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

from PassResetDialog import PassResetDialog
from EfficiencyCalculator import EfficiencyCalculator
from DateSelectorWidget import DateSelectorWidget
from FilterBox import FilterBox
from OINKMethods import version
import MOSES

class Bacon(QtGui.QMainWindow):
    def __init__(self, userID, password):
        """BACON"""
        super(BACONMainWindow,self).__init__()
        self.userID = userID
        self.password = password
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.createActions()
        self.refreshGraphs()
        self.setVisuals()
    def createWidgets(self):
        """BACON"""

    def createLayouts(self):
        """BACON"""

    def createEvents(self):
        """BACON"""

    def createActions(self):
        """BACON"""

    def fetchAuditQueue(self):
        """BACON"""

    def refreshGraphs(self):
        """BACON"""

    def plotCoverageChart(self):
        """BACON"""

    def plotPolarScatter(self):
        """BACON"""

    def fetchRawData(self):
        """BACON"""

    def openAuditForm(self):
        """BACON"""


class BACONAuditForm(QtGui.QDialog):
    def __init__(self, userID, password):
        """BACON Form"""
        super(BACONAuditForm, self).__init__()
        self.userID = userID
        self.password = password
        self.createWidgets()
        self.createLayouts()
        self.createEvents()
        self.createActions()
        self.setVisuals()

    def createWidgets(self):
        """BACON Form"""

    def createLayouts(self):
        """BACON Form"""

    def createEvents(self):
        """BACON Form"""

    def createActions(self):
        """BACON Form"""

    def fetchNextArticle(self):
        """BACON Form"""

    def fetchPreviousArticle(self):
        """BACON Form"""

    def publishAudits(self):
        """BACON Form"""

    def saveToLocal(self):
        """BACON Form"""

    def populateAuditFields(self):
        """BACON Form"""

    def addComment(self):
        """BACON Form"""

    def raiseRCA(self):
        """BACON Form"""
