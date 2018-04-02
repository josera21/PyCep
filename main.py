import math
import sys
import decimal
from PyQt5 import QtCore, QtGui, QtWidgets, uic

form_class = uic.loadUiType("interface.ui")[0]

class MyWindowClass(QtWidgets.QMainWindow, form_class):
	# Global variables
	Yi = 0
	Ri = 0

	def __init__(self, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.d = 0
		self.k = 0
		self.h = 0
		self.p = 0
		self.e = 0
		self.a = 0
		self.b = 0
		self.fx = 0
		# Estos son botones, lo que esta dentro de Connect llamo a los metodos
		self.pushCal.clicked.connect(self.run_program)
		self.pushClear.clicked.connect(self.clear)

	def emptyFields(self, *args):
		for field in args:
			if field.text() == "":
				return True
		return False
	
	def getData(self):
		if not self.emptyFields(
			self.txtD, self.txtK, self.txtH, self.txtP, self.txtE, self.txtA, self.txtB):
			self.d = float(self.txtD.text())
			self.k = float(self.txtK.text())
			self.h = float(self.txtH.text())
			self.p = float(self.txtP.text())
			self.e = float(self.txtE.text())
			self.a = float(self.txtA.text())
			self.b = float(self.txtB.text())

	def cal_opt(self, s):
		yOpt = math.sqrt((2*self.d*(self.k + self.p * s)) / self.h)
		return yOpt

	def cal_y_chapo(self):
		return math.sqrt((2*self.d*(self.k + self.p*self.e)) / self.h)

	def cal_y_raya(self):
		return (self.p*self.d)/self.h

	def cal_hy_pd(self, y):
		return (self.h*y)/(self.p*self.d)

	def cal_R(self, y):
		R = ((self.cal_hy_pd(y) - 1)*self.fx)*(-1)
		return R

	def cal_S(self, R):
		S = ((math.pow(R,2)) / (self.fx*2) - (R) + (self.fx/2))
		return S

	def cal_fx(self):
		self.fx = self.b - self.a

	def aprox(self, Ri, RiAnt):
		# dif = math.round((RiAnt - Ri) * 1000000.0) / 1000000.0
		decimal.getcontext().rounding = decimal.ROUND_DOWN
		a = decimal.Decimal(Ri)
		b = decimal.Decimal(RiAnt)
		dif = round(b, 6) - round(a, 6)
		print("diferencia: ", dif)
		return float(dif) == 0.000001

	def run_algoritm(self):
		global Yi, Ri
		i = 0
		RiAnt = 0
		seguir = True

		while seguir and i < 20:
			if i == 0:
				Yi = self.cal_opt(0)
				Ri = self.cal_R(Yi)
				print("Yi:", Yi)
				print("Ri:", Ri)
				RiAnt = Ri
			else:
				S = self.cal_S(RiAnt)
				Yi = self.cal_opt(S)
				Ri = self.cal_R(Yi)
				print("Yi:", Yi)
				print("Ri:", Ri)

				if self.aprox(Ri, RiAnt):
					seguir = False
					print("aproximacion alcanzada")
				else:
					RiAnt = Ri
			i += 1

	def has_solutions(self):
		self.getData()
		yChapo = self.cal_y_chapo()
		yRaya = self.cal_y_raya()

		return yRaya > yChapo

	def clear(self):
		self.txtD.setText("")
		self.txtK.setText("")
		self.txtH.setText("")
		self.txtP.setText("")
		self.txtE.setText("")
		self.txtA.setText("")
		self.txtB.setText("")
		self.labelYi.setText("")
		self.labelRi.setText("")
		self.labelDesc.setText("")

	def show_result(self, yi, ri):
		decimal.getcontext().rounding = decimal.ROUND_DOWN
		y_opt = decimal.Decimal(yi)
		r_opt = decimal.Decimal(ri)

		self.labelYi.setText(str(round(y_opt, 6)))
		self.labelRi.setText(str(round(r_opt, 6)))
		self.labelDesc.setText(
		"Pedir " + self.labelYi.text() + " unidades cuando el nivel de existencia baje a " + self.labelRi.text())

	def run_program(self):
		global Yi, Ri

		if not self.emptyFields(
			self.txtD, self.txtK, self.txtH, self.txtP, self.txtE, self.txtA, self.txtB):

			self.getData()
			if self.has_solutions():
				self.cal_fx()
				self.run_algoritm()
				self.show_result(Yi, Ri)
			else:
				self.labelDesc.setText("No hay soluciones factibles.")
		else:
			self.labelDesc.setText("No puede haber campos vacios.")

app = QtWidgets.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
