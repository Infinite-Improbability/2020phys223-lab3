from uncertainties import ufloat as uf
from math import pi

diam = uf(32/1000, 1/1000)
area = ((diam/2)**2) * pi
F = 0.1*9.81


class Experiment:
    def __init__(self, dT: int, h_len: float, h_max: float, v_len: float,
                 v_max: int, h_cyc: float, v_cyc: float, displ: float):
        """Setup experiment conditions
        ---------------------------
        dT: temperature difference (K)
        h_len: length of height axis (cm)
        h_max: maximum value of height axis (m)
        v_len: length of pressure axis (cm)
        v_max: maximum value of pressure axis (Pa)
        h_cyc: measurement of cycle on height axis (cm)
        v_cyc: measurement of cycle on pressure axis (cm)
        displ: measurement of displacement of piston during B->C (cm)
        -----------------------------
        self.dT: temperature difference (K)
        self.hu: height scale units (m/cm)
        self.vu: pressure scale units (Pa/cm)
        self.height: height change of cycle (m)
        self.volume: volume change of cycle (m^3)
        self.pressure: pressure change of cycle (Pa)
        self.displ: displacement of piston/mass (m)
        self.cyc_work: work done by cycle (Nm)
        self.useful_work: useful work done moving mass (Nm)
        """
        self.dT = dT

        self.hu = h_max / uf(h_len, 0.01)
        self.vu = v_max / uf(v_len, 0.01)

        self.height = self.hu * uf(h_cyc, 0.01)
        self.volume = self.height * area
        self.pressure = self.vu * uf(v_cyc, 0.01)

        self.displ = self.hu * uf(displ, 0.01)

        self.cyc_work = self.volume * self.pressure
        self.useful_work = F * self.displ

    def table(self):
        print('dT: {} K || W_cyc: {} J || W_pe: {} J || W_cyc-W_pe: {} J'
              .format(self.dT,
                      self.cyc_work,
                      self.useful_work,
                      self.cyc_work - self.useful_work
                      )
              )


T34 = Experiment(34, 14.4, 0.050, 3.82, 1500, 7.77, 3.52, 7.10)
T46 = Experiment(46, 14.37, 0.060, 3.80, 1500, 8.07, 3.50, 7.65)
T68 = Experiment(68, 14.55, 0.070, 5.58, 1600, 9.55, 5.16, 9.05)


for test in [T34, T46, T68]:
    test.table()
