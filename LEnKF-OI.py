# Illustrate how to use DAPPER:
# Basic benchmarking of DA methods.

# Load DAPPER. Assumes pwd is <path-to-dapper>
from dapper import *

resolution = 'HR'

# Load "twin experiment" setup from QG_HR model
if resolution == 'HR':
  from dapper.mods.QG_HR.sak08 import HMM
  from dapper.mods.QG_HR.core import model_config
elif resolution == 'LR':
  from dapper.mods.QG_LR.sak08 import HMM
  from dapper.mods.QG_LR.core import model_config

dt = 1.25 * 10 # 10 steps between obs (also requires dkObs=1)
HMM.t = Chronology(dt=dt,dkObs=1,T=100*dt,BurnIn=1)

HMM.t.T = 1250

Nd = 20
Ns = 200
loc_rad = 17.7
alpha = 0.04
beta = 0.3
infl = 1.1
taper = 'Gauss'
upd_a = 'DEnKF'
liveplotting = False
rot = False
mp = True

seed_true = 0
seed_da   = 5

# Simulate synthetic truth (xx) and noisy obs (yy)
# 'RKH2':2.0e-12 is the viscosity of the true state
numpy.random.seed(seed_true)
HMM.Dyn.model = model_config("truth",{"dtout":dt, "dt":1.25, 'RKH2':2.0e-12}).step
xx,yy = simulate(HMM)


HMM.Dyn.model = model_config("ens",{"dtout":dt, "dt":1.25, 'RKH2':2.0e-11}).step


numpy.random.seed(seed_da)

config = LEnKFOI(upd_a=upd_a, N=Nd, Ns=Ns, loc_rad=loc_rad, alpha=alpha, beta=beta, 
                 infl=infl, taper=taper, rot=rot, mp=mp)

config.liveplotting = liveplotting

# Assimilate yy (knowing the twin HMM). Assess vis-a-vis xx.
stats = config.assimilate(HMM,xx,yy)















