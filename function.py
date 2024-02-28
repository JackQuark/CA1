import numpy             as np

# potentil T to T
def th_2_T(theta, P):
    
    T = theta * (P/1000) ** 0.286
    
    return(T)
    

# sketch of pressure vertical profile
def P (Ps, Ts, h):

    Cp = 1004.68506 # Constant-pressure specific heat
    g  = 9.8
    M  = 0.02897    # Molar mass of dry air
    R0 = 8.31446    # Universal gas constant	
    
    P = Ps * (1 - (g * h)/(Cp * Ts))  ** (Cp * M / R0)
    
    return(P)


# c-c equation
def cc (T):

    Lv = 2.5e6 # vaporize latent heat of water
    Rv = 461.5 # gas constant of water

    es = 6.11 * np.exp(Lv/Rv * (1/273.15 - 1/T))

    return(es)

def re_cc (es):

    Lv = 2.5e6 # vaporize latent heat of water
    Rv = 461.5 # gas constant of water

    T  = 1 / ((1/273.15) - (np.log(es / 6.11) * (Rv/Lv))) 

    return(T)


# specific humidity
def q  (T, P, RH):
    
    qv = 0.622 * cc(T) * RH / (P - cc(T))

    return(qv)

def re_q (qv, P, RH):
    
    T = re_cc(qv * P / (0.622 * RH))
    
    return(T)

# sensible and latent heat
def SH (U , Ts, Ta):

    Cp  = 1004
    d   = 1.2
    CDH = 0.0015
    SH  = Cp * d * CDH * U * (Ts - Ta) 

    return(SH)

def LH (U , qs, qa):

    Lv  = 2.5e6
    d   = 1.2
    CDE = 0.0015
    LH  = Lv * d * CDE * U * (qs - qa) 

    return(LH)

# net radiation
def Rn (RS, RL, Ts, a, Es):


    sb  = 5.67e-8
    Rn  = (1 - a) * RS + Es * (RL - sb * Ts**4)

    return(Rn)
