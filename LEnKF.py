# Illustrate how to use DAPPER:
# Basic benchmarking of DA methods.

# Load DAPPER. Assumes pwd is <path-to-dapper>
from dapper import *

# Load "twin experiment" setup from QG_HR model
from dapper.mods.QG_HR.sak08 import HMM
from dapper.mods.QG_HR.core import model_config


dt = 1.25 * 10 # 10 steps between obs (also requires dkObs=1)
HMM.t = Chronology(dt=dt,dkObs=1,T=100*dt,BurnIn=1)

HMM.t.T = 1250

Nd = 20
loc_rad = 17.7
infl = 1.10
taper = 'Gauss'
# Three different analysis schemes: EnKF, DEnKF and ETKF ~~> Sakov et al., 2010
upd_a = 'DEnKF'
liveplotting = True
rot = False
mp = True

seed_true = 0
seed_da   = 5


# Simulate synthetic truth (xx) and noisy obs (yy)
# 'RKH2':2.0e-12 is the viscosity of the true state
numpy.random.seed(seed_true)
HMM.Dyn.model = model_config("truth",{"dtout":dt, "dt":1.25, 'RKH2':2.0e-12}).step
xx,yy = simulate(HMM)

# 'RKH2':2.0e-11 is the viscosity of the numerical experiment
HMM.Dyn.model = model_config("ens",{"dtout":dt, "dt":1.25, 'RKH2':2.0e-11}).step


numpy.random.seed(seed_da)
config = LEnKF(N=Nd, infl=infl, loc_rad=loc_rad, upd_a=upd_a, taper=taper, 
               rot=False, mp=True, liveplotting=liveplotting)
stats = config.assimilate(HMM,xx,yy)




















