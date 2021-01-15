from packages import * 
from func import * 

############# FIG 3 #############
def Fig3(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter):
    # Phi = 0 - Var Info
    grid_search("results_betaA_phi0.csv", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 1, p, t_max)
    # Phi = 0 - Var Disease
    grid_search("results_betaB_phi0.csv", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 1, p, t_max)
    # Phi = 2 - Var Info
    grid_search("results_betaA_phi2.csv", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max)
    # Phi = 2 - Var Desease
    grid_search("results_betaB_phi2.csv", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # Phi = 4 - Var Info
    grid_search("results_betaA_phi4.csv", niter, GA, GB, betaA, gammaA, [0.075]*len(betaA), gammaB, 5, p, t_max)
    # Phi = 4 - Var Desease
    grid_search("results_betaB_phi4.csv", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 5, p, t_max)
#################################

############# FIG 4 #############
def Fig4(N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter):
    # b2 - Var Info
    grid_search("results_betaA_b2.csv", niter, GA, GB, betaA, gammaA, [0.05]*len(betaA), gammaB, 3, p, t_max)
    # b2 - Var Disease
    grid_search("results_betaB_b2.csv", niter, GA, GB, [0.05]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # b5 - Var Info
    grid_search("results_betaA_b5.csv", niter, GA, GB, betaA, gammaA, [0.1]*len(betaA), gammaB, 3, p, t_max)
    # b5 - Var Desease
    grid_search("results_betaB_b5.csv", niter, GA, GB, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # b8 - Var Info
    grid_search("results_betaA_b8.csv", niter, GA, GB, betaA, gammaA, [0.15]*len(betaA), gammaB, 3, p, t_max)
    # b8 - Var Desease
    grid_search("results_betaB_b8.csv", niter, GA, GB, [0.15]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
#################################

############# FIG 8 #############
def Fig8(N, GA_ER, GB_ER, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter):

    # SF Information Network Parameters
    GA_SF = nx.barabasi_albert_graph(N,4)
    kA_calc = mean_degree(GA_SF)
    print(kA_calc)

    # SF Disease Network Parameters
    GB_SF = nx.barabasi_albert_graph(N,4)
    kB_calc = mean_degree(GB_SF)
    print(kB_calc)

    # ERER - Var Info
    grid_search("results_betaA_ERER.csv", niter, GA_ER, GB_ER, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max)
    # ERER - Var Disease
    grid_search("results_betaB_ERER.csv", niter, GA_ER, GB_ER, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # ERSF - Var Info
    grid_search("results_betaA_ERSF.csv", niter, GA_ER, GB_SF, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max)
    # ERSF - Var Desease
    grid_search("results_betaB_ERSF.csv", niter, GA_ER, GB_SF, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # SFER - Var Info
    grid_search("results_betaA_SFER.csv", niter, GA_SF, GB_ER, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max)
    # SFER - Var Desease
    grid_search("results_betaB_SFER.csv", niter, GA_SF, GB_ER, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)
    # SFSF - Var Info
    grid_search("results_betaA_SFSF.csv", niter, GA_SF, GB_SF, betaA, gammaA, [0.075]*len(betaA), gammaB, 3, p, t_max)
    # SFSF - Var Desease
    grid_search("results_betaB_SFSF.csv", niter, GA_SF, GB_SF, [0.1]*len(betaB), gammaA, betaB, gammaB, 3, p, t_max)

#################################
