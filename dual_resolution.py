# Illustrate how to use DAPPER:
# Basic benchmarking of DA methods.

# Load DAPPER. Assumes pwd is <path-to-dapper>
from dapper import *

# Load "twin experiment" setup from QG_HR model
from dapper.mods.QG_HR.sak08 import HMM as HMM_hr
from dapper.mods.QG_HR.core import model_config as model_config_hr

from dapper.mods.QG_LR.sak08 import HMM as HMM_lr
from dapper.mods.QG_LR.core import model_config as model_config_lr


# ~~~~~ Parameters ~~~~~ #
mp = True
loc_radh = 17.7
loc_radl = 8.75
upd_a = 'DEnKF'
infl = 1.10
alpha = 0.04

taper = 'Gauss'
liveplotting = True

seed_true = 0 
seed_da  = 5
# ~~~~~~~~~~~~~~~~~~~~~~ #


dth = 1.25*10
HMM_hr.t = Chronology(dt=dth,dkObs=1,T=100*dth,BurnIn=1)
HMM_hr.t.T = 125

dtl = dth
HMM_lr.t = Chronology(dt=dtl,dkObs=1,T=100*dth,BurnIn=1)
HMM_lr.t.T = HMM_hr.t.T


# Simulate synthetic truth (xx) and noisy obs (yy)
# 'RKH2':2.0e-12 is the viscosity of the true state
numpy.random.seed(seed_true)
HMM_hr.Dyn.model = model_config_hr("truth",{"dtout":dth, 'RKH2':2.0e-12}).step
# ~~~ Generates the high resolution true state ~~~ #
xx_hr,yy_hr = simulate(HMM_hr)
# ~~~ Interpolates the high res. true state to the low res. grid ~~~ #
xx_lr = true_state_lr(HMM_lr,xx_hr)
# ~~~ Low res. and high res. observations are the same ~~~ #
yy_lr = yy_hr

# "RKH2":2.0e-11 is the viscosity of the numerical experiments
HMM_hr.Dyn.model = model_config_hr("ens",{"dtout":dth, "dt":1.25, "RKH2":2.0e-11}).step
HMM_lr.Dyn.model = model_config_lr("ens",{"dtout":dtl, "dt":2.50, "RKH2":2.0e-11}).step

Nh = 15
Nl = 8*(20-Nh)
beta1 = 0.2
beta2 = 0.6


numpy.random.seed(seed_da)
config = dual_resolution(N=Nh,Nl=Nl,beta1=beta1,beta2=beta2,
                         loc_radh=loc_radh,loc_radl=loc_radl,upd_a=upd_a,
                         infl=infl,mp=mp)
config.liveplotting = liveplotting
statsh = config.assimilate(HMM_hr,xx_hr,yy_hr,HMM_lr=HMM_lr,xx_lr=xx_lr,yy_lr=yy_lr)






