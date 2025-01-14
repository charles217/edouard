import numpy as np
from tqdm import tqdm
import cmath
import math


# range for loops, from start, to finish with increment as the stepsize
def myRange(start, finish, increment):
    myZero = 1e-17
    while (start <= finish+myZero):
        yield start
        start += increment
        
        

# Periodic Linear Extension
def paramMapping(x, c, d):

    if ((x>=c) & (x<=d)):
        
        y = x

    else:
        
        range = d-c
        n = math.floor((x-c)/range)
        if (n%2 == 0):
            y = x - n*range;
        else:
            y = d + n*range - (x-c)
            
    return y

#def eValue(params, marketPrices, maturities, strikes, r, q, S0, alpha, eta, n, model):
def eValue(params, *args):
    
    marketPrices = args[0]
    maturities = args[1]
    strikes = args[2]
    r = args[3]
    q = args[4]
    S0 = args[5]
    alpha = args[6]
    eta = args[7]
    n = args[8]
    model = args[9]

    lenT = len(maturities)
    lenK = len(strikes)
    
    modelPrices = np.zeros((lenT, lenK))
    #print(marketPrices.shape)
    #print(modelPrices.shape)

    count = 0
    mae = 0
    for i in range(lenT):
        for j in range(lenK):
            count  = count+1
            T = maturities[i]
            K = strikes[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices[i,j] = cT_km[0]
            tmp = marketPrices[i,j]-modelPrices[i,j]
            mae += tmp**2
    
    rmse = math.sqrt(mae/count)
    print(rmse)
    return rmse

def eValue_w(params, *args):
    
    marketPrices = args[0]
    maturities = args[1]
    strikes = args[2]
    r = args[3]
    q = args[4]
    S0 = args[5]
    alpha = args[6]
    eta = args[7]
    n = args[8]
    model = args[9]
    w = args[10]

    lenT = len(maturities)
    lenK = len(strikes)
    
    modelPrices = np.zeros((lenT, lenK))
    #print(marketPrices.shape)
    #print(modelPrices.shape)

    count = np.sum(w)
    mae = 0
    for i in range(lenT):
        for j in range(lenK):
            #count  = count+1
            T = maturities[i]
            K = strikes[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices[i,j] = cT_km[0] 
            tmp = marketPrices[i,j]-modelPrices[i,j]
            mae += w[i,j]*tmp**2
    
    rmse = math.sqrt(mae/count)
    print(rmse)
    return rmse

def eValuefull(params, *args):
    
    marketPrices = args[0]
    marketPrices_Put = args[1]
    maturities = args[2]
    maturities_Put = args[3]
    strikes = args[4]
    strikes_Put = args[5]
    r = args[6]
    q = args[7]
    S0 = args[8]
    alpha = args[9]
    eta = args[10]
    n = args[11]
    model = args[12]

    lenT = len(maturities)
    lenK = len(strikes)
    lenT_Put = len(maturities_Put)
    lenK_Put = len(strikes_Put)

    modelPrices = np.zeros((lenT, lenK))
    modelPrices_Put = np.zeros((lenT_Put, lenK_Put))

    count = 0
    mae = 0
    for i in range(lenT):
        for j in range(lenK):
            count  = count+1
            T = maturities[i]
            K = strikes[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices[i,j] = cT_km[0]
            tmp = marketPrices[i,j]-modelPrices[i,j]
            mae += tmp**2

    for i in range(lenT_Put):
        for j in range(lenK_Put):
            count  = count+1
            T = maturities_Put[i]
            K = strikes_Put[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices_Put[i,j] = cT_km[0]+K*np.exp(-r*T)-S0*np.exp(-q*T)
            tmp = marketPrices_Put[i,j]-modelPrices_Put[i,j]
            mae += tmp**2
    
    rmse = math.sqrt(mae/count)
    return rmse

def eValuefull_w(params, *args):
    
    marketPrices = args[0]
    marketPrices_Put = args[1]
    
    maturities = args[2]
    maturities_Put = args[3]
    
    strikes = args[4]
    strikes_Put = args[5]
    
    r = args[6]
    q = args[7]
    S0 = args[8]
    alpha = args[9]
    eta = args[10]
    n = args[11]
    model = args[12]
    w_call = args[13]
    w_put = args[14]

    lenT = len(maturities)
    lenK = len(strikes)
    
    lenT_Put = len(maturities_Put)
    lenK_Put = len(strikes_Put)
    
    modelPrices = np.zeros((lenT, lenK))
    modelPrices_Put = np.zeros((lenT_Put, lenK_Put))
    #print(marketPrices.shape)

    count = 0
    mae = 0
    for i in range(lenT):
        for j in range(lenK):
            count  = count+1
            T = maturities[i]
            K = strikes[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices[i,j] = cT_km[0]
            tmp = marketPrices[i,j]-modelPrices[i,j]
            mae += w_call[i,j]*(tmp**2)
    
    for i in range(lenT_Put):
        for j in range(lenK_Put):
            count  = count+1
            T = maturities_Put[i]
            K = strikes_Put[j]
            [km, cT_km] = genericFFT(params, S0, K, r, q, T, alpha, eta, n, model)
            modelPrices_Put[i,j] = cT_km[0]+K*np.exp(-r*T)-S0*np.exp(-q*T)
            tmp = marketPrices_Put[i,j]-modelPrices_Put[i,j]
            mae += w_put[i,j]*(tmp**2)
    
    rmse = math.sqrt(mae/count)
    return rmse

def generic_CF(u, params, S0, r, q, T, model):
    
    if (model == 'GBM'):
        
        sig = params[0]
        mu = np.log(S0) + (r-q-sig**2/2)*T
        a = sig*np.sqrt(T)
        phi = np.exp(1j*mu*u-(a*u)**2/2)
        
    elif(model == 'Heston'):
        
        kappa  = params[0]
        theta  = params[1]
        sigma  = params[2]
        rho    = params[3]
        v0     = params[4]
        
        kappa = paramMapping(kappa,0.1, 20)
        theta = paramMapping(theta,0.001, 0.4)
        sigma = paramMapping(sigma,0.01, 0.6)
        rho   = paramMapping(rho  ,-1.0, 1.0)
        v0    = paramMapping(v0   ,0.005, 0.25)
        
        tmp = (kappa-1j*rho*sigma*u)
        g = np.sqrt((sigma**2)*(u**2+1j*u)+tmp**2)
        
        pow1 = 2*kappa*theta/(sigma**2)
        
        numer1 = (kappa*theta*T*tmp)/(sigma**2) + 1j*u*T*r + 1j*u*math.log(S0)
        log_denum1 = pow1 * np.log(np.cosh(g*T/2)+(tmp/g)*np.sinh(g*T/2))
        tmp2 = ((u*u+1j*u)*v0)/(g/np.tanh(g*T/2)+tmp)
        log_phi = numer1 - log_denum1 - tmp2
        phi = np.exp(log_phi)
        
        #g = np.sqrt((kappa-1j*rho*sigma*u)**2+(u*u+1j*u)*sigma*sigma)
        #beta = kappa-rho*sigma*1j*u
        #tmp = g*T/2
        
        #temp1 = 1j*(np.log(S0)+(r-q)*T)*u + kappa*theta*T*beta/(sigma*sigma)
        #temp2 = -(u*u+1j*u)*v0/(g/np.tanh(tmp)+beta)
        #temp3 = (2*kappa*theta/(sigma*sigma))*np.log(np.cosh(tmp)+(beta/g)*np.sinh(tmp))
        
        #phi = np.exp(temp1+temp2-temp3);
        

    elif (model == 'VG'):
        
        sigma  = params[0];
        nu     = params[1];
        theta  = params[2];

        if (nu == 0):
            mu = math.log(S0) + (r-q - theta -0.5*sigma**2)*T
            phi  = math.exp(1j*u*mu) * math.exp((1j*theta*u-0.5*sigma**2*u**2)*T)
        else:
            mu  = math.log(S0) + (r-q + math.log(1-theta*nu-0.5*sigma**2*nu)/nu)*T
            phi = cmath.exp(1j*u*mu)*((1-1j*nu*theta*u+0.5*nu*sigma**2*u**2)**(-T/nu))
    
    elif (model == 'VGSA'):
        
        sigma  = params[0];
        nu     = params[1];
        theta  = params[2];
        kappa  = params[3]; 
        eta    = params[4];
        lbda   = params[5];
        
        #cf if mu = 0 ce qu'on fait
        #if (nu == 0):
        psi_VG_i = - np.log(1-theta*nu-sigma**2*nu*0.5)/nu
        psi_VG_u = - np.log(1-1j*u*theta*nu+sigma**2*nu*u**2*0.5)/nu
        
        tp = 1j*u * (np.log(S0) + (r-q)*T)
        
        def A(v):
            ga = np.sqrt(kappa**2 - 2*lbda**2*1j*v)
            A_t = np.exp(kappa**2*eta*T/(lbda**2))/((np.cosh(ga*T/2)+(kappa/ga)*np.sinh(ga*T/2))**(kappa*2*eta/(lbda**2)))
            return(A_t)
        def B(v):
            ga = np.sqrt(kappa**2 - 2*lbda**2*1j*v)
            B_t = 2*1j*v / (kappa+ ga/np.tanh(ga*T/2))
            return(B_t)
        
        phi_up = A(-1j*psi_VG_u)*np.exp(B(-1j*psi_VG_u)/nu)
        phi_down = A(-1j*psi_VG_i)*np.exp(B(-1j*psi_VG_i)/nu)
        
        phi = np.exp(tp)*phi_up/(phi_down)
        
    return phi

def genericFFT(params, S0, K, r, q, T, alpha, eta, n, model):
    
    N = 2**n
    
    # step-size in log strike space
    lda = (2*np.pi/N)/eta
    
    #Choice of beta
    #beta = np.log(S0)-N*lda/2
    beta = np.log(K)
    
    # forming vector x and strikes km for m=1,...,N
    km = np.zeros((N))
    xX = np.zeros((N))
    
    # discount factor
    df = math.exp(-r*T)
    
    nuJ = np.arange(N)*eta
    psi_nuJ = generic_CF(nuJ-(alpha+1)*1j, params, S0, r, q, T, model)/((alpha + 1j*nuJ)*(alpha+1+1j*nuJ))
    
    for j in range(N):  
        km[j] = beta+j*lda
        if j == 0:
            wJ = (eta/2)
        else:
            wJ = eta
        xX[j] = cmath.exp(-1j*beta*nuJ[j])*df*psi_nuJ[j]*wJ
     
    yY = np.fft.fft(xX)
    cT_km = np.zeros((N))  
    for i in range(N):
        multiplier = math.exp(-alpha*km[i])/math.pi
        cT_km[i] = multiplier*np.real(yY[i])
    
    return km, cT_km