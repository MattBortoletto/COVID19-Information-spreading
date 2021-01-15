from packages import * 
from func import * 

############# FIG 3 #############
def Fig3(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y):
    # Phi = 0 - Var Info
    grid_search("results_betaA_phi0", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 1, p, t_max, prop_Y)
    # Phi = 0 - Var Disease
    grid_search("results_betaB_phi0", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 1, p, t_max, prop_Y)
    # Phi = 2 - Var Info
    grid_search("results_betaA_phi2", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max, prop_Y)
    # Phi = 2 - Var Desease
    grid_search("results_betaB_phi2", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max, prop_Y)
    # Phi = 4 - Var Info
    grid_search("results_betaA_phi4", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 5, p, t_max, prop_Y)
    # Phi = 4 - Var Desease
    grid_search("results_betaB_phi4", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 5, p, t_max, prop_Y)
#################################

############# FIG 4 #############
def Fig4(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y):
    # b2 - Var Info
    grid_search("results_betaA_b2", niter, GA, GB, betaA, gammaA, [0.05]*len(betaA), gammaB, 3, p, t_max, prop_Y)
    # b2 - Var Disease
    grid_search("results_betaB_b2", niter, GA, GB, [0.05]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max, prop_Y)
    # b5 - Var Info
    grid_search("results_betaA_b5", niter, GA, GB, betaA, gammaA, [0.1]*len(betaA), gammaB, 3, p, t_max, prop_Y)
    # b5 - Var Desease
    grid_search("results_betaB_b5", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max, prop_Y)
    # b8 - Var Info
    grid_search("results_betaA_b8", niter, GA, GB, betaA, gammaA, [0.15]*len(betaA), gammaB, 3, p, t_max, prop_Y)
    # b8 - Var Desease
    grid_search("results_betaB_b8", niter, GA, GB, [0.15]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max, prop_Y)
#################################
