from fig_func import *

if not os.path.exists("realizations"):
    os.mkdir("realizations")
   
os.chdir("realizations")

n_realizations = 20      
for i in range(n_realizations): 
    print("-------- realization n°", i, "--------")
    N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y = init()
    dir = os.path.join("net_realization_"+str(i+1)) 
    if not os.path.exists(dir):
        os.mkdir(dir)
    os.chdir(dir) 
    print("---- Fig3 ----")
    Fig3(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y)
    print("---- Fig4 ----")
    Fig4(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y)
    os.chdir("../")
