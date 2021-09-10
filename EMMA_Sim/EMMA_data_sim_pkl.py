import os
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil import parser
# from scipy.interpolate import NearestNDInterpolator
import matplotlib.pyplot as plt

# from emtracks.mapinterp import get_df_interp_func
# copied interpolation here. FIXME!
from mapinterp import get_df_interp_func

# Note: see docdb-#6908 for geometry details

# data directory
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
print(datadir)

# create map interpolation functions
DS_cyl = get_df_interp_func(filename=datadir+'Mu2e_DSMap_V13.p',
                            gauss=False, mm=False,
                            Blabels=['Br', 'Bphi', 'Bz'])
DS_car = get_df_interp_func(filename=datadir+'Mu2e_DSMap_V13.p',
                            gauss=False, mm=False,
                            Blabels=['Bx', 'By', 'Bz'])


# measurement noise for field values
sigma_Bi = 0.
#sigma_Bi = 1e-4

# solenoid current
current_PS = 9200.
current_TS = 1730.
current_DS = 6114.

sigma_current = 0.
# sigma_current = 1e-4

'''
- Coordinates for now:
    - Hall probe: with Hall element and electronics facing "out of page"
        - Y points to top of card
        - X points to the right
        - Z out of page
'''

# Globals for DSFM locations and probe orientations
# reflector radius
# counter-clockwise
# Phi is w.r.t. BP up (i.e. defines Phi=0)
Rs_reflect_BP = 1e-3*np.array([1450./2., 700./2., 1450./2., 700./2.])
Phis_reflect_BP = np.pi*np.array([1., 1.5, 0., 0.5]) # CHECK
Rs_reflect_SP = 1e-3*np.array(4*[241./2.]) # CHECK NUMBER!!
Phis_reflect_SP = np.pi/4. + np.pi*np.array([1., 1.5, 0., 0.5]) # CHECK

# radius on propeller, signed by which side of the propeller
Rs_small = 1e-3*np.array([0., 54., -95.,]) # CHECK SIGNS!!
Rs_large = 1e-3*np.array([44., -319., 488., -656., 800.])
# coordinate orientations of Hall probes
# x = 0, y = 1, z = 2 -- in HP coordinates
# ATTEMPT 1
# these arrays specify which HP coordinate represents Br, Bphi, Bz
'''
Coords_small = np.array([[1, 0, -2],
                         [-1, -0, -2],
                         [1, 0, -2],
                        ]) # CHECK SIGNS XY!
Coords_large = np.array([[-1, 0, 2],
                         [1, -0, 2],
                         [1, -0, 2],
                         [1, -0, 2],
                         [1, -0, 2],
                        ])
'''
# ATTEMPT 2
_ = np.array([{'Bx': ['Bphi', 1.], 'By': ['Br', 1.], 'Bz': ['Bz', -1.]},
              {'Bx': ['Bphi', -1.], 'By': ['Br', -1.], 'Bz': ['Bz', -1.]},
              {'Bx': ['Bphi', 1.], 'By': ['Br', 1.], 'Bz': ['Bz', -1.]},
             ])
Coords_SP_dict = _
_ = np.array([{'Bx': ['Bphi', 1.], 'By': ['Br', -1.], 'Bz': ['Bz', 1.]},
              {'Bx': ['Bphi', -1.], 'By': ['Br', 1.], 'Bz': ['Bz', 1.]},
              {'Bx': ['Bphi', -1.], 'By': ['Br', 1.], 'Bz': ['Bz', 1.]},
              {'Bx': ['Bphi', -1.], 'By': ['Br', 1.], 'Bz': ['Bz', 1.]},
              {'Bx': ['Bphi', -1.], 'By': ['Br', 1.], 'Bz': ['Bz', 1.]},
             ])
Coords_BP_dict = _

# all probes
Rs = np.concatenate([Rs_small, Rs_large])
# location label & hardware ID
HP_labs = np.array(['SP1', 'SP2', 'SP3', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5'])
HP_IDs = np.array(['4C0000000D55C93A', '8E0000000D51483A', '6A0000000D61333A',
                   'C50000000D5E473A', 'DF0000000D5E803A', 'C90000000D53983A',
                   'FA0000000D60163A', '2F0000000D5EC73A']) # using probes 1-8
# coefficients for simple voltage model: V_i = slope * B_i + off
# from real measurements (NOT MATCHED TO PROBE ID!!)
# to get realistic voltages
HP_V_slope = np.array([2.871e6, 2.813e6, 2.940e6, 2.973e6,
                       2.957e6, 2.863e6, 2.875e6, 2.831e6])
HP_V_off = np.array([-6.169e4, -6.300e4, -6.546e4, -6.136e4,
                     -6.346e4, -6.160e4, -5.939e4, -5.737e4])

# split into big an small propeller where necessary
HP_labs_SP = HP_labs[0:3]
HP_labs_BP = HP_labs[3:]
HP_IDs_SP = HP_IDs[0:3]
HP_IDs_BP = HP_IDs[3:]
HP_V_slope_SP = HP_V_slope[0:3]
HP_V_slope_BP = HP_V_slope[3:]
HP_V_off_SP = HP_V_off[0:3]
HP_V_off_BP = HP_V_off[3:]

# Define steps for DSFM. Big propeller "top" along +X defines Phi=0
# Small propeller offset by +45 deg = pi/4 rad by design
Phis = np.linspace(0, 2*np.pi, 17)[:-1]
Phis_SP = Phis + np.pi/4.

# NMR always at the same location in XY plane
NMR_Phi = np.pi/2.
# probe on BP at R=-319 mm, want it in -y direction
NMR_R = -319. * 1e-3 # m
X_NMR = NMR_R * np.cos(NMR_Phi)
Y_NMR = NMR_R * np.sin(NMR_Phi)

print(f'NMR Location: x = {X_NMR:0.3f} m, y = {Y_NMR:0.3f}')

# RR_BP, PP_BP = np.meshgrid(Rs_large, Phis)
# RR_SP, PP_SP = np.meshgrid(Rs_small, Phis_SP)

# Calculating Z locations for SP, BP, NMR
END_MEAS_SP = 2980. * 1e-3
START_MEAS_SP = 13685. * 1e-3
step_Z = 0.05 # 5 cm step, for now
Zs_SP = np.arange(START_MEAS_SP, END_MEAS_SP, -step_Z)
delta_Z_BP_SP = -1335. * 1e-3
Zs_BP = Zs_SP - delta_Z_BP_SP
delta_Z_NMR_SP = -1557.87 * 1e-3
Zs_NMR = Zs_SP - delta_Z_NMR_SP

# columns to write to file

# Draft:
# TIMESTAMP, X_NMR, Y_NMR, Z_NMR, HP_1_#, HP_1_ID, HP_1_X, HP_1_Y, HP_1_Z, ...
# HP_1_Bx_Meas, HP_1_Bx_Mu2e, HP_1_By_Meas, HP_1_By_Mu2e, HP_1_Bz_Meas, HP_1_Bz_Mu2e,
# HP_1_V1, HP_1_V2, HP_1_V3, ... ALL Hall probes - 7 , 8 , 9

single_reflect_cols = ['rho', 'theta', 'z']
_ = list(np.concatenate([[f'Reflect_SP_{j}_{i}' for i in single_reflect_cols]
                        for j in ['A', 'B', 'C', 'D']]))
reflect_SP_col_list = _
_ = list(np.concatenate([[f'Reflect_BP_{j}_{i}' for i in single_reflect_cols]
                        for j in ['A', 'B', 'C', 'D']]))
reflect_BP_col_list = _

# print(reflect_SP_col_list)
# print(reflect_BP_col_list)

single_HP_cols = ['ID', 'X', 'Y', 'Z', 'Vx', 'Vy', 'Vz', 'Temperature',
                  'Bx_Meas', 'By_Meas', 'Bz_Meas', 'Br', 'Bphi', 'Bz']
HP_SP_col_list = list(np.concatenate([[f'HP_SP{j}_{i}' for i in single_HP_cols]
                                      for j in [1, 2, 3]]))
HP_BP_col_list = list(np.concatenate([[f'HP_BP{j}_{i}' for i in single_HP_cols]
                                      for j in [1, 2, 3, 4, 5]]))
col_list = ['TIMESTAMP', 'Mapper_Angle', 'Mapper_Z', 'X_NMR', 'Y_NMR', 'Z_NMR',
            'B_NMR'] + HP_SP_col_list + HP_BP_col_list \
            + reflect_BP_col_list + reflect_SP_col_list

# define an empty dataframe
# df_EMMA = pd.DataFrame(columns=col_list)

# pick a starttime
t0 = parser.parse('2021-07-21 12:00:00')
# define time between steps
dt_Phi = timedelta(seconds=120) # assume 2 minutes per step for azimuthal move
dt_Z = timedelta(seconds=240) # 4 minutes when moving z

# define an insteresting temperature scalar field throughout the DS
def temp_DS(pos):
    return 22. - 0.1 * (pos[2] - 4.) + 1. * (pos[1])

# function to return one row for the dataframe where each row is a "step"
# of EMMA
def return_row(time, Z_ind, Phi_ind, ):
    row = {}
    # phi
    Phi = Phis[Phi_ind]
    Phi_BP = Phi
    Phi_SP = Phis_SP[Phi_ind]
    # time
    row['TIMESTAMP'] = str(time)
    # mapper
    row['Mapper_Angle'] = Phi
    row['Mapper_Z'] = Zs_NMR[Z_ind]
    # NMR
    row['X_NMR'] = X_NMR
    row['Y_NMR'] = Y_NMR
    row['Z_NMR'] = Zs_NMR[Z_ind]
    B_NMR = np.linalg.norm(DS_car([X_NMR, Y_NMR, Zs_NMR[Z_ind]]))
    if B_NMR < 0.7: # NMR cutoff
        B_NMR = 0.0
    row['B_NMR'] = B_NMR
    # Hall probes
    # small propeller
    #print('SP')
    for i in range(len(HP_IDs_SP)):
        #print(i)
        pre = f'HP_{HP_labs_SP[i]}'
        row[f'{pre}_ID'] = HP_IDs_SP[i]
        # coords
        X_ = Rs_small[i] * np.cos(Phi_SP)
        Y_ = Rs_small[i] * np.sin(Phi_SP)
        Z_ = Zs_SP[Z_ind]
        row[f'{pre}_X'] = X_
        row[f'{pre}_Y'] = Y_
        row[f'{pre}_Z'] = Z_
        # field
        Br, Bphi, Bz = DS_cyl([X_, Y_, Z_])
        if sigma_Bi > 0.:
            Br += np.random.normal(loc=0.0, scale=sigma_Bi)
            Bphi += np.random.normal(loc=0.0, scale=sigma_Bi)
            Bz += np.random.normal(loc=0.0, scale=sigma_Bi)
        B_dict = {'Br': Br, 'Bphi': Bphi, 'Bz': Bz}
        Bx_ = Coords_SP_dict[i]['Bx'][1] * B_dict[Coords_SP_dict[i]['Bx'][0]]
        By_ = Coords_SP_dict[i]['By'][1] * B_dict[Coords_SP_dict[i]['By'][0]]
        Bz_ = Coords_SP_dict[i]['Bz'][1] * B_dict[Coords_SP_dict[i]['Bz'][0]]
        # voltages
        Vx_ = HP_V_off_SP[i] + HP_V_slope_SP[i] * Bx_
        Vy_ = HP_V_off_SP[i] + HP_V_slope_SP[i] * By_
        Vz_ = HP_V_off_SP[i] + HP_V_slope_SP[i] * Bz_
        # temperature
        Temp_ = temp_DS([X_, Y_, Z_])
        # write to row
        row[f'{pre}_Vx'] = int(Vx_)
        row[f'{pre}_Vy'] = int(Vy_)
        row[f'{pre}_Vz'] = int(Vz_)
        row[f'{pre}_Temperature'] = Temp_
        row[f'{pre}_Bx_Meas'] = Bx_
        row[f'{pre}_By_Meas'] = By_
        row[f'{pre}_Bz_Meas'] = Bz_
        row[f'{pre}_Br'] = Br
        row[f'{pre}_Bphi'] = Bphi
        row[f'{pre}_Bz'] = Bz
    # big propeller
    #print('BP')
    for i in range(len(HP_IDs_BP)):
        #print(i)
        pre = f'HP_{HP_labs_BP[i]}'
        row[f'{pre}_ID'] = HP_IDs_BP[i]
        # coords
        X_ = Rs_large[i] * np.cos(Phi_BP)
        Y_ = Rs_large[i] * np.sin(Phi_BP)
        Z_ = Zs_BP[Z_ind]
        row[f'{pre}_X'] = X_
        row[f'{pre}_Y'] = Y_
        row[f'{pre}_Z'] = Z_
        # field
        Br, Bphi, Bz = DS_cyl([X_, Y_, Z_])
        if sigma_Bi > 0.:
            Br += np.random.normal(loc=0.0, scale=sigma_Bi)
            Bphi += np.random.normal(loc=0.0, scale=sigma_Bi)
            Bz += np.random.normal(loc=0.0, scale=sigma_Bi)
        B_dict = {'Br': Br, 'Bphi': Bphi, 'Bz': Bz}
        Bx_ = Coords_BP_dict[i]['Bx'][1] * B_dict[Coords_BP_dict[i]['Bx'][0]]
        By_ = Coords_BP_dict[i]['By'][1] * B_dict[Coords_BP_dict[i]['By'][0]]
        Bz_ = Coords_BP_dict[i]['Bz'][1] * B_dict[Coords_BP_dict[i]['Bz'][0]]
        # voltages
        Vx_ = HP_V_off_BP[i] + HP_V_slope_BP[i] * Bx_
        Vy_ = HP_V_off_BP[i] + HP_V_slope_BP[i] * By_
        Vz_ = HP_V_off_BP[i] + HP_V_slope_BP[i] * Bz_
        # temperature
        Temp_ = temp_DS([X_, Y_, Z_])
        # write to row
        row[f'{pre}_Vx'] = int(Vx_)
        row[f'{pre}_Vy'] = int(Vy_)
        row[f'{pre}_Vz'] = int(Vz_)
        row[f'{pre}_Temperature'] = Temp_
        row[f'{pre}_Bx_Meas'] = Bx_
        row[f'{pre}_By_Meas'] = By_
        row[f'{pre}_Bz_Meas'] = Bz_
        row[f'{pre}_Br'] = Br
        row[f'{pre}_Bphi'] = Bphi
        row[f'{pre}_Bz'] = Bz
    # reflectors
    ref_labs = ['A', 'B', 'C', 'D']
    base_width = 75. # [mm], ESTIMATE!! CHECK BASE WIDTH
    # BP
    for i, lab in enumerate(ref_labs):
        r = Rs_reflect_BP[i]*1e3
        t = Phi + Phis_reflect_BP[i]
        z = Zs_NMR[Z_ind]*1e3
        x = r * np.cos(t)
        y = r * np.sin(t)
        if (x > -base_width/2) and (x < base_width/2) and (y < 0):
            r = np.nan
            t = np.nan
            z = np.nan
        row[f'Reflect_BP_{lab}_rho'] = r # [mm] in TDMS
        row[f'Reflect_BP_{lab}_theta'] = t # [rad] in TDMS
        row[f'Reflect_BP_{lab}_z'] = z # [mm] in TDMS
    # SP
    for i, lab in enumerate(ref_labs):
        r = Rs_reflect_SP[i]*1e3
        t = Phi + Phis_reflect_SP[i]
        z = Zs_SP[Z_ind]*1e3
        x = r * np.cos(t)
        y = r * np.sin(t)
        if (x > -base_width/2) and (x < base_width/2) and (y < 0):
            r = np.nan
            t = np.nan
            z = np.nan
        row[f'Reflect_SP_{lab}_rho'] = r # [mm] in TDMS
        row[f'Reflect_SP_{lab}_theta'] = t # [rad] in TDMS
        row[f'Reflect_SP_{lab}_z'] = z # [mm] in TDMS
    # current
    if sigma_current > 0.:
        c_PS = current_PS + np.random.normal(loc=0.0, scale=sigma_current)
        c_TS = current_TS + np.random.normal(loc=0.0, scale=sigma_current)
        c_DS = current_DS + np.random.normal(loc=0.0, scale=sigma_current)
    else:
        c_PS = current_PS
        c_TS = current_TS
        c_DS = current_DS
    row['PS_Current'] = c_PS
    row['TS_Current'] = c_TS
    row['DS_Current'] = c_DS
    return row


if __name__ == '__main__':
    # generate dataframe looping through Z and Phi steps
    rows_list = []
    t = t0
    for Z_ind in range(len(Zs_NMR)):
        # t += dt_Z
        for Phi_ind in range(len(Phis)):
            row = return_row(t, Z_ind, Phi_ind)
            rows_list.append(row)
            t += dt_Phi
        t += dt_Z

    df_EMMA = pd.DataFrame(rows_list)

    print(df_EMMA)

    i = 0
    print('Missing Columns:')
    for col in col_list:
        if not col in df_EMMA.columns:
            i += 1
            print(col)
    print(f'Total Missing: {i}')

    # df_EMMA.to_pickle(datadir+'TEST.pkl')
    # df_EMMA.to_csv(datadir+'TEST.csv')
    # save
    # testfile_version = "3"
    # testfile_version = "4"
    #testfile_version = "5"
    testfile_version = "6"
    # noise = "1e-4_noise"
    noise = "no_noise"
    df_EMMA.to_pickle(datadir+f'DSFM_test_data_{noise}_v{testfile_version}.pkl')
    df_EMMA.to_csv(datadir+f'DSFM_test_data_{noise}_v{testfile_version}.csv')

    # some basic plots
    # NMR vs. Z
    fig, ax = plt.subplots()
    ax.scatter(df_EMMA.Z_NMR, df_EMMA.B_NMR, s=1)
    ax.set_xlabel('Z [m]')
    ax.set_ylabel(r'$|B|_{\mathrm{NMR}}$ [T]')
    # NMR vs. measurment number
    fig, ax = plt.subplots()
    ax.scatter(df_EMMA.index, df_EMMA.B_NMR, s=1)
    ax.set_xlabel('Measurement #')
    ax.set_ylabel(r'$|B|_{\mathrm{NMR}}$ [T]')
    # Plane of temperature data
    #df_ = df_EMMA.query('Z_NMR == 10.74287')
    df_ = df_EMMA[np.isclose(df_EMMA.Z_NMR, 10.74287)]
    fig, ax = plt.subplots(figsize=(10,10))
    Xs = []
    Ys = []
    Ts = []
    for i in [1, 2, 3, 4, 5]:
        Xs.append(df_[f'HP_BP{i}_X'].values)
        Ys.append(df_[f'HP_BP{i}_Y'].values)
        Ts.append(df_[f'HP_BP{i}_Temperature'].values)
    Xs = np.concatenate(Xs)
    Ys = np.concatenate(Ys)
    Ts = np.concatenate(Ts)
    sc = ax.scatter(Xs, Ys, c=Ts)
    cb = fig.colorbar(sc, label='Temperature [deg C]')
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.axis('equal');

    # show all plots
    plt.show()
