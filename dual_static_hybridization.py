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
Nh = 3
Nl = 32
Nhs = 200
Nls = 200
mp = True
loc_radh = 17.7
loc_radl = 8.75
upd_a = 'EnKF'
infl = 1.10
alpha = 0.04

# High resolution hybridization coefficients
betaH3 = 0.1
betaH  = 0.2
betaH1 = (1-betaH3)*(1-betaH)
betaH2 = (1-betaH3)*betaH

# Low resolution hybridization coefficients
betaL3 = 0.4
betaL  = 0.6
betaL1 = (1-betaL3)*(1-betaL)
betaL2 = (1-betaL3)*betaL

taper = 'Gauss'
liveplotting = True

seed_true = 0 
seed_da  = 5
# ~~~~~~~~~~~~~~~~~~~~~~ #

dth = 1.25*10
HMM_hr.t = Chronology(dt=dth,dkObs=1,T=100*dth,BurnIn=1)
HMM_hr.t.T = 1250

dtl = dth
HMM_lr.t = Chronology(dt=dtl,dkObs=1,T=100*dth,BurnIn=1)
HMM_lr.t.T = HMM_hr.t.T


# Simulate synthetic truth (xx) and noisy obs (yy)
# 'RKH2':2.0e-12 is the viscosity of the true state
numpy.random.seed(seed_true)
HMM_hr.Dyn.model = model_config_hr("truth",{"dtout":dth, 'RKH2':2.0e-12}).step
xx_hr,yy_hr = simulate(HMM_hr)
xx_lr = true_state_lr(HMM_lr,xx_hr)
yy_lr = yy_hr 

# 'RKH2':2.0e-11 is the viscosity of the numerical experiment
HMM_hr.Dyn.model = model_config_hr("ens",{"dtout":dth, "dt":1.25, "RKH2":2.0e-11}).step
HMM_lr.Dyn.model = model_config_lr("ens",{"dtout":dtl, "dt":2.50, "RKH2":2.0e-11}).step

  
numpy.random.seed(seed_da)
config = dual_static_hybridization(upd_a=upd_a, N=Nh, Nhs=Nhs, Nl=Nl, Nls=Nls,
                                   loc_radh=loc_radh, loc_radl=loc_radl,
                                   alpha=alpha, 
                                   betaH1=betaH1, betaH2=betaH2, betaH3=betaH3,
                                   betaL1=betaL1, betaL2=betaL2, betaL3=betaL3,
                                   infl=infl, taper=taper, rot=False, mp=True, 
                                   liveplotting=liveplotting)
statsh = config.assimilate(HMM_hr,xx_hr,yy_hr,HMM_lr=HMM_lr,xx_lr=xx_lr,yy_lr=yy_lr)










































