import numpy as np
from scipy.constants import epsilon_0, mu_0
from render import SimulationRender
from fdtd_grid import FDTDGrid


class FDTDSimulation:
	"""
	Simulation object for two dimensional finite-difference time-domain method.
	Runnning a simulation solves for the time-varying vector components of the electric and magnetic fields in a two-
	dimensional box.
	Objects (rectangles, ellipses) with arbitrary properties can be simulated in the grid using the input file.
	Boundaries of the computational volume can be PML, PEC, PMC, or simply defined with constant
	permeability/permittivity.
	"""
	def __init__(self, **kwargs):
		self.__initsimulation__(kwargs)
		self.__initmesh__(kwargs)
		self.__checkgridspacing__()
		self.__initobjects__(kwargs)
		self.__initsource__(kwargs)

	def __initsimulation__(self, kwargs):
		"""
		"""
		self.delta_t = kwargs.get('time_stepsize', 1.0e-12)

		self.x_length = kwargs.get('x_length', 1.0e-6) 
		self.delta_x = kwargs.get('x_stepsize', 1.0e-9)    
		x_size = int(np.round(self.x_length/self.delta_x))
		
		self.y_length = kwargs.get('y_length', 1.0e-6)    		
		self.delta_y = kwargs.get('y_stepsize', 1.0e-9)    		
		y_size = int(np.round(self.y_length/self.delta_y))

		self.size = (x_size, y_size)
		self.n_sim_steps = 0

	def __initmesh__(self, kwargs):
		"""
		"""
		self.mesh = FDTDGrid(size=self.size)
		self.history = [self.mesh]

	def __checkgridspacing__(self):
		"""
		Makes sure grid spacing and time spacing correspond to an accurate simulation.
		Raises warning if accuracy will be affected, alters values if simulation will not be physical.
		"""
		raise NotImplementedError

	def __initobjects__(self, kwargs):
		raise NotImplementedError

	def __initsource__(self, kwargs):
		raise NotImplementedError

	def simulate(self):
		""" Executes main simulation loop. """
		done = False
		t = 0
		while not done:
			self.inject_source()
			self.update_magnetic_field()
			self.update_electric_field()
			self.record_history()

			t += 1
			if self.is_last_iteration(t):
				self.n_sim_steps = t
				done = True

	def inject_source(self):
		raise NotImplementedError

	def update_magnetic_field(self):
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				Chxh = self._Chxh(i, j)
				Chxez = self._Chxez(i, j)
				Chxm = self._Chxm(i, j)

				Chyh = self._Chyh(i, j)
				Chyez = self._Chyez(i, j)
				Chym = self._Chym(i, j)

				Chzh = self._Chzh(i, j)
				Chzex = self._Chzex(i, j)
				Chzey = self._Chzey(i, j)
				Chzm = self._Chzm(i, j)

				self.mesh[i, j].H.x = Chxh * self.mesh[i, j].H.x + \
									 Chxez * (self.mesh[i, j + 1].E.z - self.mesh[i, j].E.z) + \
									 Chxm * self.mesh[i, j].M.x

				self.mesh[i, j].H.y = Chyh * self.mesh[i, j].H.y + \
									 Chyez * (self.mesh[i + 1, j].E.z - self.mesh[i, j].E.z) + \
									 Chym * self.mesh[i, j].M.y

				self.mesh[i, j].H.z = Chzh * self.mesh[i, j].H.z + \
									  Chzex * (self.mesh[i, j + 1].E.x - self.mesh[i, j].E.x) + \
									  Chzey * (self.mesh[i + 1, j].E.y - self.mesh[i, j].E.y) + \
									  Chzm * self.mesh[i, j].M.z

	def update_electric_field(self):
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				Cexe = self._Cexe(i, j)
				Cexhz = self._Cexhz(i, j)
				Cexj = self._Cexj(i, j)

				Ceye = self._Ceye(i, j)
				Ceyhz = self._Ceyhz(i, j)
				Ceyj = self._Ceyj(i, j)

				Ceze = self._Ceze(i, j)
				Cezhy = self._Cezhy(i, j)
				Cezhx = self._Cezhx(i, j)
				Cezj = self._Cezj(i, j)

				self.mesh[i, j].E.x = Cexe * self.mesh[i, j].E.x + \
									 Cexhz * (self.mesh[i, j].H.z - self.mesh[i, j - 1].H.z) + \
									 Cexj * self.mesh[i, j].J.x

				self.mesh[i, j].E.y = Ceye * self.mesh[i, j].E.y + \
									 Ceyhz * (self.mesh[i, j].H.z - self.mesh[i - 1, j].H.z) + \
									 Ceyj * self.mesh[i, j].J.y

				self.mesh[i, j].E.z = Ceze * self.mesh[i, j].E.z + \
									  Cezhy * (self.mesh[i, j].H.y - self.mesh[i - 1, j].H.y) + \
									  Cezhx * (self.mesh[i, j].H.x - self.mesh[i, j - 1].H.x) + \
									  Cezj * self.mesh[i, j].J.z


	def record_history(self):
		self.history.append(self.mesh)

	def is_last_iteration(self, t):
		raise NotImplementedError

	def render(self):
		raise NotImplementedError

	def _Cff(self, p, sig):
		dt = self.delta_t
		return (2 * p - dt * sig) / (2 * p + dt * sig)

	def _Cexe(self, i, j):
		epsx = self.mesh[i, j].eps_r * epsilon_0
		sig_ex = self.mesh[i, j].sig_e.x
		return self._Cff(epsx, sig_ex)

	def _Ceye(self, i, j):
		epsy = self.mesh[i, j].eps_r * epsilon_0
		sig_ey = self.mesh[i, j].sig_e.y
		return self._Cff(epsy, sig_ey)

	def _Ceze(self, i, j):
		epsz = self.mesh[i, j].eps_r * epsilon_0
		sig_ez = self.mesh[i, j].sig_e.z
		return self._Cff(epsz, sig_ez)

	def _Chxh(self, i, j):
		mux = self.mesh[i, j].mu_r * mu_0
		sig_mx = self.mesh[i, j].sig_m.x
		return self._Cff(mux, sig_mx)

	def _Chyh(self, i, j):
		muy = self.mesh[i, j].mu_r * mu_0
		sig_my = self.mesh[i, j].sig_m.y
		return self._Cff(muy, sig_my)

	def _Chzh(self, i, j):
		muz = self.mesh[i, j].mu_r * mu_0
		sig_mz = self.mesh[i, j].sig_m.z
		return self._Cff(muz, sig_mz)

	def _Cfg(self, d, p, sig):
		dt = self.delta_t
		return 2 * dt / (d * (2 * p + dt * sig))

	def _Cexhz(self, i, j):
		dy = self.delta_y
		epsx = self.mesh[i, j].eps_r * epsilon_0
		sig_ex = self.mesh[i, j].sig_e.x
		return self._Cfg(dy, epsx, sig_ex)

	def _Ceyhz(self, i, j):
		dx = self.delta_x
		epsy = self.mesh[i, j].eps_r * epsilon_0
		sig_ey = self.mesh[i, j].sig_e.y
		return -self._Cfg(dx, epsy, sig_ey)

	def _Cezhy(self, i, j):
		dx = self.delta_x
		epsz = self.mesh[i, j].eps_r * epsilon_0
		sig_ez = self.mesh[i, j].sig_e.z
		return self._Cfg(dx, epsz, sig_ez)

	def _Cezhx(self, i, j):
		dy = self.delta_y
		epsz = self.mesh[i, j].eps_r * epsilon_0
		sig_ez = self.mesh[i, j].sig_e.z
		return -self._Cfg(dy, epsz, sig_ez)

	def _Chxez(self, i, j):
		dy = self.delta_y
		mux = self.mesh[i, j].mu_r * mu_0
		sig_mx = self.mesh[i, j].sig_m.x
		return -self._Cfg(dy, mux, sig_mx)

	def _Chyez(self, i, j):
		dx = self.delta_x
		muy = self.mesh[i, j].mu_r * mu_0
		sig_my = self.mesh[i, j].sig_m.y
		return self._Cfg(dx, muy, sig_my)

	def _Chzey(self, i, j):
		dx = self.delta_x
		muz = self.mesh[i, j].mu_r * mu_0
		sig_mz = self.mesh[i, j].sig_m.z
		return -self._Cfg(dx, muz, sig_mz)

	def _Chzex(self, i, j):
		dy = self.delta_y
		muz = self.mesh[i, j].mu_r * mu_0
		sig_mz = self.mesh[i, j].sig_m.z
		return self._Cfg(dy, muz, sig_mz)

	def _Cfc(self, p, sig):
		dt = self.delta_t
		return -2 * dt / (2 * p + dt * sig)

	def _Cexj(self, i, j):
		epsx = self.mesh[i, j].eps_r * epsilon_0
		sig_ex = self.mesh[i, j].sig_e.x
		return self._Cfc(epsx, sig_ex)

	def _Ceyj(self, i, j):
		epsy = self.mesh[i, j].eps_r * epsilon_0
		sig_ey = self.mesh[i, j].sig_e.y
		return self._Cfc(epsy, sig_ey)

	def _Cezj(self, i, j):
		epsz = self.mesh[i, j].eps_r * epsilon_0
		sig_ez = self.mesh[i, j].sig_e.z
		return self._Cfc(epsz, sig_ez)

	def _Chxm(self, i, j):
		mux = self.mesh[i, j].mu_r * mu_0
		sig_mx = self.mesh[i, j].sig_m.x
		return self._Cfc(mux, sig_mx)

	def _Chym(self, i, j):
		muy = self.mesh[i, j].mu_r * mu_0
		sig_my = self.mesh[i, j].sig_m.y
		return self._Cfc(muy, sig_my)

	def _Chzm(self, i, j):
		muz = self.mesh[i, j].mu_r * mu_0
		sig_mz = self.mesh[i, j].sig_m.z
		return self._Cfc(muz, sig_mz)
