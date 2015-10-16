import pygame
import os
from PyQt4 import QtCore
class Player(QtCore.QThread):
    def __init__(self):
        super(Player, self).__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.allow_play = False
        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)

    def run(self):
        while True:
            if self.allow_play:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(os.path.join("Images","tmnt.mp3"))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
                self.allow_play = False