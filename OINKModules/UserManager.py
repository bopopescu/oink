#User Manager Dialog Class definition.
class UserManager(QtGui.QDialog):
	def __init__(self, userID, password):
		QtGui.QDialog.__init__(self)
		self.users_list_label = QtGui.QLabel("Users: ")
		self.users_list = QtGui.QListView()
		#get the list of users from MOSES.
		self.reset_password_button = QtGui.QPushButton("Reset Password")
		self.add_user_button = QtGui.QAddUser("")