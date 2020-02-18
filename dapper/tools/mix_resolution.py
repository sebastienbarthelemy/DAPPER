from dapper import *

# ~~~~~ Parameters ~~~~~ #
# Number of grid points for each side of the doamin
# High res. model
nxh = 129
# Low res. model
nxl = 65
# ~~~~~ Parameters ~~~~~ #



def true_state_lr(HMM,xx_hr,desc='Truth low res'):
  """Generate a free run"""
  f,h,chrono,X0 = HMM.Dyn, HMM.Obs, HMM.t, HMM.X0

  # Init
  xx = zeros((chrono.K+1,f.M))
  # Loop
  for k,kObs,t,dt in progbar(chrono.ticker,desc):
    xx[k] = interpolate_h2l(xx_hr[k])
  return xx


def interpolate_h2l(hr):
  X = list(range(0,nxh,2))
  hrl = hr.reshape(nxh,nxh)
  return hrl[np.ix_(X,X)].ravel()


def interpolate_l2h(lr):
  X0 = list(range(nxh))
  X2 = list(range(0,nxh,2))
  Y0 = list(range(0,nxh-1,2))
  Y1 = list(range(1,nxh,2))
  Y2 = list(range(2,nxh+1,2))
  lrh = np.zeros((nxh,nxh))
  lrh[np.ix_(X2,X2)] = lr.reshape(nxl,nxl)
  lrh[np.ix_(Y1,X0)] = (lrh[np.ix_(Y2,X0)]+lrh[np.ix_(Y0,X0)])*0.5
  lrh[np.ix_(X0,Y1)] = (lrh[np.ix_(X0,Y2)]+lrh[np.ix_(X0,Y0)])*0.5
  return lrh.ravel()

