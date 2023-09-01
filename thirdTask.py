import numpy as np
import scipy.stats as si
from scipy.stats import norm

def Normsdist(x):
    PolanitzerNormsdist = si.norm.cdf(x,0.0,1.0)
    return (PolanitzerNormsdist)

def d1(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility):
    return (np.log(SpotRate/StrikeRate)+(DomesticRiskFreeRate-ForeignRiskFreeRate+0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))

def d2(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility):
    return (np.log(SpotRate/StrikeRate)+(DomesticRiskFreeRate-ForeignRiskFreeRate-0.5*Volatility**2)*Maturity)/(Volatility*np.sqrt(Maturity))

def GarmanKohlhagenCall(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility):
    d1_val = d1(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility)
    d2_val = d2(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility)
    PolanitzerGarmanKohlhagenCall = SpotRate*np.exp(-ForeignRiskFreeRate*Maturity)*Normsdist(d1_val)-StrikeRate*np.exp(-DomesticRiskFreeRate*Maturity)*Normsdist(d2_val)
    return(PolanitzerGarmanKohlhagenCall)

def GammaFdm(S, K, T, r, sigma , ds, method, ForeignRiskFreeRate):
    method = method.lower() 
    if method =='central':
        return (GarmanKohlhagenCall(S+ds , K, T, r, ForeignRiskFreeRate, sigma) -2*GarmanKohlhagenCall(S, K, T, r, ForeignRiskFreeRate, sigma) + 
                    GarmanKohlhagenCall(S-ds , K, T, r, ForeignRiskFreeRate, sigma) )/ (ds)**2

def ThetaCallFdm(S, K, T, r, sigma, dt, method, ForeignRiskFreeRate):
    method = method.lower() 
    if method =='central':
        return -(GarmanKohlhagenCall(S, K, T+dt, r, ForeignRiskFreeRate, sigma) -GarmanKohlhagenCall(S, K, T-dt, r, ForeignRiskFreeRate, sigma))/\
                        (2*dt)

SpotRate = 0.92
StrikeRate = 0.9 * SpotRate
Maturity = 1
DomesticRiskFreeRate = 0.0567
ForeignRiskFreeRate = 0.0378

monthly = [-np.log(1.58), -np.log(2.57), np.log(0.86), np.log(5.28), np.log(2.85), np.log(1.50), -np.log(2.63), np.log(2.49), np.log(1.67), -np.log(3.01), np.log(2.08), np.log(0.76), -np.log(1.38)]
Volatility = np.std(monthly)

gammas = GammaFdm(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, Volatility, 1e-5, 'central', ForeignRiskFreeRate)
theta = ThetaCallFdm(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, Volatility, 1e-5, 'central', ForeignRiskFreeRate)

print("The fair value of a First European Call option based on the Garman & Kohlhagen (1983) Model is: ${:.5}".format((GarmanKohlhagenCall(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility))))
print("Gamma First Call ", gammas)
print("Theta First Call ", theta)

StrikeRate = 1.1 * SpotRate
gammas = GammaFdm(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, Volatility, 1e-5, 'central', ForeignRiskFreeRate)
theta = ThetaCallFdm(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, Volatility, 1e-5, 'central', ForeignRiskFreeRate)

print("The fair value of a Second European Call option based on the Garman & Kohlhagen (1983) Model is: ${:.5}".format((GarmanKohlhagenCall(SpotRate, StrikeRate, Maturity, DomesticRiskFreeRate, ForeignRiskFreeRate, Volatility))))
print("Gamma Second Call ", gammas)
print("Theta Second Call ", theta)
