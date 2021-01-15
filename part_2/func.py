from packages import * 

# Communities Graph
def cmm(N,pYY,pOO,pYO,prop_Y):

    label_Y = [i for i in range(int(N*prop_Y))]
    label_O = [int(N*prop_Y)+i for i in range(int(N*(1-prop_Y))+1)]

    G = nx.Graph() 
    G.add_nodes_from(label_Y)
    G.add_nodes_from(label_O)
    
    kYY = 0
    kOO = 0
    kYO = 0
    
    node_labels = G.nodes()
    edges = set()
    
    for i in range(N): 
        for j in range(N): 
            if i != j:               
                if ((i <= int(N*prop_Y)) and (j <= int(N*prop_Y))):
                    if random.random() < pYY:  
                        edges.add((i,j))
                        kYY += 1
                if ((i > int(N*prop_Y)) and (j > int(N*prop_Y))):
                    if random.random() < pOO:                
                        edges.add((i,j))
                        kOO += 1
                if (((i <= int(N*prop_Y)) and (j > int(N*prop_Y))) or ((i > int(N*prop_Y)) and (j <= int(N*prop_Y)))):
                    if random.random() < pYO:                
                        edges.add((i,j))
                        kYO += 1          
                        
    norm = kYY + kOO + kYO

    G.add_edges_from(edges)
    
    return G, kYY/norm, kOO/norm, kYO/norm


def SIARV(age_state, old_stateA, old_stateB, GB, betaB, gammaB, phi, p):
     
    new_stateB = old_stateB.copy()
    
    # Infection phase                
    for node in range(len(old_stateB)):
                    
        if (old_stateB[node] == 'IBS' or old_stateB[node] == 'IBA'):
        
            l = GB.neighbors(node)

            for i in l:                
                if old_stateB[i] == 'SB':                    
                    x = random.random() 
                    y = random.random()
                    if age_state[i] == 'Y':
                        pA = 0.68
                    else: pA = 0.59
                    
                    if x < betaB:
                        if y < pA:
                            new_stateB[i] = 'IBA'
                        else: new_stateB[i] = 'IBS'
    
    # Recovery phase                
    for node in range(len(old_stateB)):
        
        if (old_stateB[node] == 'IBA' or old_stateB[node] == 'IBS'):
            x = random.random()
            if x < gammaB:
                new_stateB[node] = 'RB'
                
    # Vaccination phase                
    for node in range(len(old_stateB)):
                    
        if (old_stateB[node] == 'SB' and old_stateA[node] == 'IA'):
        
            l = GB.neighbors(node)
            
            count = 0
            for i in l:                
                if old_stateB[i] == 'IBS': 
                    count += 1
            if count >= phi:
                x = random.random()                    
                if x < p:
                    new_stateB[node] = 'VB'
       
    return new_stateB


def SIR(age_state, old_stateA, old_stateB, GA, betaA, gammaA):
    
    new_stateA = old_stateA.copy()
    
    # Infection phase                
    for node in range(len(old_stateA)):
                    
        if old_stateA[node] == 'IA':
        
            l = GA.neighbors(node)

            for i in l:                
                if old_stateA[i] == 'SA':                    
                    x = random.random()
                    
                    if age_state[i] == "O":
                        var = 0.8
                    else: var = 1
                    
                    if x < betaA*var:
                        new_stateA[i] = 'IA'
    
    # Recovery phase                
    for node in range(len(old_stateA)):
        if old_stateA[node] == 'IA':
            x = random.random()
            if x < gammaA:
                new_stateA[node] = 'RA'
                
    # Information phase                
    for node in range(len(old_stateA)):
        if (old_stateA[node] == 'SA' and old_stateB[node] == 'IBS'):
            new_stateA[node] = 'IA'
            
    return new_stateA


def propagator(which_out, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, prop_Y):

    dt = 0
    
    NB = GB.number_of_nodes()
    NA = GA.number_of_nodes()
    node_labelsB = GB.nodes()
    node_labelsA = GA.nodes()
    
    old_stateA = ['SA' for i in node_labelsA]
    old_stateB = ['SB' for i in node_labelsB]
    
    label_Y = ['Y' for i in range(int(NA*prop_Y))]
    label_O = ['O' for i in range(int(NA*(1-prop_Y))+1)]
    
    age_state = label_Y + label_O 
   
    for i in range(10):
        seed = random.choice(range(NB))
        old_stateA[seed] = 'IA' 
        old_stateB[seed] = 'IBS' 
    
    if which_out == "c":
        SAY_frac = []
        IAY_frac = []
        RAY_frac = []
        SBY_frac = []
        IBSY_frac = []
        IBAY_frac = []
        RBY_frac = []
        VBY_frac = []
        
        SAO_frac = []
        IAO_frac = []
        RAO_frac = []
        SBO_frac = []
        IBSO_frac = []
        IBAO_frac = []
        RBO_frac = []
        VBO_frac = []
        
    while dt < t_max:
        
        new_stateA = SIR(age_state, old_stateA, old_stateB, GA, betaA, gammaA) 
        new_stateB = SIARV(age_state, old_stateA, old_stateB, GB, betaB, gammaB, phi, p)

        old_stateA = new_stateA.copy()
        old_stateB = new_stateB.copy()

        data = zip(new_stateA, new_stateB, age_state)
        df = pd.DataFrame(data, columns = ["new_stateA", "new_stateB", "age_state"])
        df_Y = df[df["age_state"] == "Y"]
        df_O = df[df["age_state"] == "O"]
            
        if which_out == "c":
            SAY_frac.append(df_Y[df_Y["new_stateA"] == "SA"].count()[1]/(NA*prop_Y))
            IAY_frac.append(df_Y[df_Y["new_stateA"] == "IA"].count()[1]/(NA*prop_Y))
            RAY_frac.append(df_Y[df_Y["new_stateA"] == "RA"].count()[1]/(NA*prop_Y))
            
            SBY_frac.append(df_Y[df_Y["new_stateB"] == "SB"].count()[1]/(NB*prop_Y))
            IBSY_frac.append(df_Y[df_Y["new_stateB"] == "IBS"].count()[1]/(NB*prop_Y))
            IBAY_frac.append(df_Y[df_Y["new_stateB"] == "IBA"].count()[1]/(NB*prop_Y))
            RBY_frac.append(df_Y[df_Y["new_stateB"] == "RB"].count()[1]/(NB*prop_Y))
            VBY_frac.append(df_Y[df_Y["new_stateB"] == "VB"].count()[1]/(NB*prop_Y))
            
            SAO_frac.append(df_O[df_O["new_stateA"] == "SA"].count()[1]/(NA*(1-prop_Y)))
            IAO_frac.append(df_O[df_O["new_stateA"] == "IA"].count()[1]/(NA*(1-prop_Y)))
            RAO_frac.append(df_O[df_O["new_stateA"] == "RA"].count()[1]/(NA*(1-prop_Y)))
            
            SBO_frac.append(df_O[df_O["new_stateB"] == "SB"].count()[1]/(NB*(1-prop_Y)))
            IBSO_frac.append(df_O[df_O["new_stateB"] == "IBS"].count()[1]/(NB*(1-prop_Y)))
            IBAO_frac.append(df_O[df_O["new_stateB"] == "IBA"].count()[1]/(NB*(1-prop_Y)))
            RBO_frac.append(df_O[df_O["new_stateB"] == "RB"].count()[1]/(NB*(1-prop_Y)))
            VBO_frac.append(df_O[df_O["new_stateB"] == "VB"].count()[1]/(NB*(1-prop_Y)))

        elif which_out == "f":
            SAY_frac = df_Y[df_Y["new_stateA"] == "SA"].count()[1]/(NA*prop_Y)
            IAY_frac = df_Y[df_Y["new_stateA"] == "IA"].count()[1]/(NA*prop_Y)
            RAY_frac = df_Y[df_Y["new_stateA"] == "RA"].count()[1]/(NA*prop_Y)
            
            SBY_frac = df_Y[df_Y["new_stateB"] == "SB"].count()[1]/(NB*prop_Y)
            IBSY_frac = df_Y[df_Y["new_stateB"] == "IBS"].count()[1]/(NB*prop_Y)
            IBAY_frac = df_Y[df_Y["new_stateB"] == "IBA"].count()[1]/(NB*prop_Y)
            RBY_frac = df_Y[df_Y["new_stateB"] == "RB"].count()[1]/(NB*prop_Y)
            VBY_frac = df_Y[df_Y["new_stateB"] == "VB"].count()[1]/(NB*prop_Y)
            
            SAO_frac = df_O[df_O["new_stateA"] == "SA"].count()[1]/(NA*(1-prop_Y))
            IAO_frac = df_O[df_O["new_stateA"] == "IA"].count()[1]/(NA*(1-prop_Y))
            RAO_frac = df_O[df_O["new_stateA"] == "RA"].count()[1]/(NA*(1-prop_Y))
            
            SBO_frac = df_O[df_O["new_stateB"] == "SB"].count()[1]/(NB*(1-prop_Y))
            IBSO_frac = df_O[df_O["new_stateB"] == "IBS"].count()[1]/(NB*(1-prop_Y))
            IBAO_frac = df_O[df_O["new_stateB"] == "IBA"].count()[1]/(NB*(1-prop_Y))
            RBO_frac = df_O[df_O["new_stateB"] == "RB"].count()[1]/(NB*(1-prop_Y))
            VBO_frac = df_O[df_O["new_stateB"] == "VB"].count()[1]/(NB*(1-prop_Y))

        else:
            print("Not valid option!")
        
        dt += 1
    
    Y_list = (SAY_frac, IAY_frac, RAY_frac, SBY_frac, IBSY_frac, IBAY_frac, RBY_frac, VBY_frac)
    O_list = (SAO_frac, IAO_frac, RAO_frac, SBO_frac, IBSO_frac, IBAO_frac, RBO_frac, VBO_frac)
   
    return (Y_list, O_list)


def grid_search(filename, niterations, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, prop_Y):

    RA_mean_Y = []
    RB_mean_Y = []
    VB_mean_Y = []
    
    RA_mean_O = []
    RB_mean_O = []
    VB_mean_O = []

    for i in range(len(betaA)):
        # Change number of workers
        res = Parallel(n_jobs=-1, verbose=0)(delayed(propagator)("f", GA, GB, betaA[i], gammaA, betaB[i], gammaB, phi, p, t_max, prop_Y) for k in range(niterations))
        
        df_Y = pd.DataFrame(res[0], columns=["SA", "IA", "RA", "SB", "IBS", "IBA","RB", "VB"])
        RA_mean_Y.append(df_Y["RA"].mean())
        RB_mean_Y.append(df_Y["RB"].mean())
        VB_mean_Y.append(df_Y["VB"].mean())
        
        df_O = pd.DataFrame(res[1], columns=["SA", "IA", "RA", "SB", "IBS", "IBA","RB", "VB"])
        RA_mean_O.append(df_O["RA"].mean())
        RB_mean_O.append(df_O["RB"].mean())
        VB_mean_O.append(df_O["VB"].mean())
        
        
    rows_Y = zip(betaA, betaB, RA_mean_Y, RB_mean_Y, VB_mean_Y) 
    rows_O = zip(betaA, betaB, RA_mean_O, RB_mean_O, VB_mean_O)
    
    with open(filename+"_Y.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows_Y:
            writer.writerow(row)
            
    with open(filename+"_O.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows_O:
            writer.writerow(row)


def mean_degree_YO(G, prop_Y):
    kY = 0
    kO = 0
    N = G.number_of_nodes()
    
    for i in range(int(N*prop_Y)):
        kY += G.degree[i]

    for i in range(int(N*prop_Y),N): 
        kO += G.degree[i]
        
    kY_mean = kY/int(N*prop_Y)
    kO_mean = kO/int(N*(1-prop_Y))
    
    return kY_mean, kO_mean


def SIR_AB(age_state, old_stateA, old_stateAA, old_stateB, GA, betaA, gammaA):
    
    new_stateA = old_stateA.copy()
    new_stateAA = old_stateAA.copy()
    
    # Infection phase                
    for node in range(len(old_stateA)):
                    
        if old_stateA[node] == 'IA':
        
            l = GA.neighbors(node)

            for i in l:                
                if old_stateA[i] == 'SA':                    
                    x = random.random()
                    
                    if age_state[i] == "O":
                        var = 0.8
                    else: var = 1
                    
                    if x < betaA*var:
                        new_stateA[i] = 'IA'
                        new_stateAA[i] = 'IAA'
    
    # Recovery phase                
    for node in range(len(old_stateA)):
        
        if old_stateA[node] == 'IA':
            x = random.random()
            if x < gammaA:
                new_stateA[node] = 'RA'
                new_stateAA[node] = 'RA'
                
     # Information phase                
    for node in range(len(old_stateA)):
        if (old_stateA[node] == 'SA' and old_stateB[node] == 'IBS'):
            new_stateA[node] = 'IA'
            new_stateAA[node] = 'IAB'
            
    return new_stateA, new_stateAA


def propagator_AB(which_out, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, prop_Y):

    dt = 0
    
    NB = GB.number_of_nodes()
    NA = GA.number_of_nodes()
    node_labelsB = GB.nodes()
    node_labelsA = GA.nodes()
    
    old_stateA = ['SA' for i in node_labelsA]
    old_stateB = ['SB' for i in node_labelsB]
     
    label_Y = ['Y' for i in range(int(NA*prop_Y))]
    label_O = ['O' for i in range(int(NA*(1-prop_Y)))]
    
    age_state = label_Y + label_O 
   
    for i in range(10):
        seed = random.choice(range(NB))
        old_stateA[seed] = 'IA' 
        old_stateB[seed] = 'IBS' 
    
    if which_out == "c":
        SAY_frac = []
        IAY_frac = []
        RAY_frac = []
        SBY_frac = []
        IBSY_frac = []
        IBAY_frac = []
        RBY_frac = []
        VBY_frac = []
        
        SAO_frac = []
        IAO_frac = []
        RAO_frac = []
        SBO_frac = []
        IBSO_frac = []
        IBAO_frac = []
        RBO_frac = []
        VBO_frac = []

    rhoAA_Y = []
    rhoAB_Y = []
    rhoAA_O = []
    rhoAB_O = []
    
    old_stateAA = old_stateA.copy()
        
    while dt < t_max:
        
        new_stateA, new_stateAA = SIR_AB(age_state, old_stateA, old_stateAA, old_stateB, GA, betaA, gammaA) 
        new_stateB = SIARV(age_state, old_stateA, old_stateB, GB, betaB, gammaB, phi, p)

        old_stateA = new_stateA.copy()
        old_stateAA = new_stateAA.copy()
        old_stateB = new_stateB.copy()

        data = zip(new_stateA, new_stateB, new_stateAA, age_state)
        df = pd.DataFrame(data, columns = ["new_stateA", "new_stateB", "new_stateAA", "age_state"])
        df_Y = df[df["age_state"] == "Y"]
        df_O = df[df["age_state"] == "O"]
            
        if which_out == "c":
            SAY_frac.append(df_Y[df_Y["new_stateA"] == "SA"].count()[1]/(NA*prop_Y))
            IAY_frac.append(df_Y[df_Y["new_stateA"] == "IA"].count()[1]/(NA*prop_Y))
            RAY_frac.append(df_Y[df_Y["new_stateA"] == "RA"].count()[1]/(NA*prop_Y))
            
            SBY_frac.append(df_Y[df_Y["new_stateB"] == "SB"].count()[1]/(NB*prop_Y))
            IBSY_frac.append(df_Y[df_Y["new_stateB"] == "IBS"].count()[1]/(NB*prop_Y))
            IBAY_frac.append(df_Y[df_Y["new_stateB"] == "IBA"].count()[1]/(NB*prop_Y))
            RBY_frac.append(df_Y[df_Y["new_stateB"] == "RB"].count()[1]/(NB*prop_Y))
            VBY_frac.append(df_Y[df_Y["new_stateB"] == "VB"].count()[1]/(NB*prop_Y))

            rhoAA_Y.append(df_Y[df_Y["new_stateAA"] == "IAA"].count()[1]/(NB*prop_Y))
            rhoAB_Y.append(df_Y[df_Y["new_stateAA"] == "IAB"].count()[1]/(NB*prop_Y))
            
            SAO_frac.append(df_O[df_O["new_stateA"] == "SA"].count()[1]/(NA*(1-prop_Y)))
            IAO_frac.append(df_O[df_O["new_stateA"] == "IA"].count()[1]/(NA*(1-prop_Y)))
            RAO_frac.append(df_O[df_O["new_stateA"] == "RA"].count()[1]/(NA*(1-prop_Y)))
            
            SBO_frac.append(df_O[df_O["new_stateB"] == "SB"].count()[1]/(NB*(1-prop_Y)))
            IBSO_frac.append(df_O[df_O["new_stateB"] == "IBS"].count()[1]/(NB*(1-prop_Y)))
            IBAO_frac.append(df_O[df_O["new_stateB"] == "IBA"].count()[1]/(NB*(1-prop_Y)))
            RBO_frac.append(df_O[df_O["new_stateB"] == "RB"].count()[1]/(NB*(1-prop_Y)))
            VBO_frac.append(df_O[df_O["new_stateB"] == "VB"].count()[1]/(NB*(1-prop_Y)))

            rhoAA_O.append(df_O[df_O["new_stateAA"] == "IAA"].count()[1]/(NB*(1-prop_Y)))
            rhoAB_O.append(df_O[df_O["new_stateAA"] == "IAB"].count()[1]/(NB*(1-prop_Y)))

        elif which_out == "f":
            SAY_frac = df_Y[df_Y["new_stateA"] == "SA"].count()[1]/(NA*prop_Y)
            IAY_frac = df_Y[df_Y["new_stateA"] == "IA"].count()[1]/(NA*prop_Y)
            RAY_frac = df_Y[df_Y["new_stateA"] == "RA"].count()[1]/(NA*prop_Y)
            
            SBY_frac = df_Y[df_Y["new_stateB"] == "SB"].count()[1]/(NB*prop_Y)
            IBSY_frac = df_Y[df_Y["new_stateB"] == "IBS"].count()[1]/(NB*prop_Y)
            IBAY_frac = df_Y[df_Y["new_stateB"] == "IBA"].count()[1]/(NB*prop_Y)
            RBY_frac = df_Y[df_Y["new_stateB"] == "RB"].count()[1]/(NB*prop_Y)
            VBY_frac = df_Y[df_Y["new_stateB"] == "VB"].count()[1]/(NB*prop_Y)
            
            SAO_frac = df_O[df_O["new_stateA"] == "SA"].count()[1]/(NA*(1-prop_Y))
            IAO_frac = df_O[df_O["new_stateA"] == "IA"].count()[1]/(NA*(1-prop_Y))
            RAO_frac = df_O[df_O["new_stateA"] == "RA"].count()[1]/(NA*(1-prop_Y))
            
            SBO_frac = df_O[df_O["new_stateB"] == "SB"].count()[1]/(NB*(1-prop_Y))
            IBSO_frac = df_O[df_O["new_stateB"] == "IBS"].count()[1]/(NB*(1-prop_Y))
            IBAO_frac = df_O[df_O["new_stateB"] == "IBA"].count()[1]/(NB*(1-prop_Y))
            RBO_frac = df_O[df_O["new_stateB"] == "RB"].count()[1]/(NB*(1-prop_Y))
            VBO_frac = df_O[df_O["new_stateB"] == "VB"].count()[1]/(NB*(1-prop_Y))

        else:
            print("Not valid option!")
        
        dt += 1
    
    Y_list = ([sum(x) for x in zip(IBSY_frac, IBAY_frac)], rhoAA_Y, rhoAB_Y)
    O_list = ([sum(x) for x in zip(IBSO_frac, IBAO_frac)], rhoAA_O, rhoAB_O)
   
    return (Y_list, O_list)


def init():

    N = 10000
    pYY = 0.0016 
    pOO = 0.00089 
    pYO = 0.00038 
    prop_Y = 0.55

    # Information Network Parameters
    GA, frac_YYA, frac_OOA, frac_YOA = cmm(N,pYY,pOO,pYO,prop_Y)
    kY_mean_A, kO_mean_A = mean_degree_YO(GA, prop_Y)
    k_mean_A = kY_mean_A*prop_Y + kO_mean_A*(1-prop_Y)

    # Disease Network Parameters
    GB, frac_YYB, frac_OOB, frac_YOB = cmm(N,pYY,pOO,pYO,prop_Y)
    kY_mean_B, kO_mean_B = mean_degree_YO(GB, prop_Y)
    k_mean_B = kY_mean_B*prop_Y + kO_mean_B*(1-prop_Y)

    betaA = np.linspace(0, 0.2, 20)
    gammaA = 0.2
    R0YA = kY_mean_A * betaA / gammaA
    R0OA = kO_mean_A * betaA / gammaA
    
    betaB = np.linspace(0, 0.2, 20) 
    gammaB = 0.2 
    R0YB = kY_mean_B * betaB / gammaB
    R0OB = kO_mean_B * betaB / gammaB

    phi = 3
    p = 0.8

    t_max = 100
    niter = 100

    with open("parameters.txt", "a") as f:
        f.write("----------------------------------" + "\n")
        f.write("N:"        + str(N)         + "\n")
        f.write("kAY mean:" + str(kY_mean_A) + "\n")
        f.write("kAO mean:" + str(kO_mean_A) + "\n")
        f.write("kA mean:" + str(k_mean_A) + "\n")
        f.write("frac_YYA:"     + str(frac_YYA)      + "\n")
        f.write("frac_OOA:"     + str(frac_OOA)      + "\n")
        f.write("frac_YOA:"     + str(frac_YOA)      + "\n")
        f.write("kBY mean:" + str(kY_mean_B) + "\n")
        f.write("kBO mean:" + str(kO_mean_B) + "\n")
        f.write("kB mean:" + str(k_mean_B) + "\n")
        f.write("frac_YYB:"     + str(frac_YYB)      + "\n")
        f.write("frac_OOB:"     + str(frac_OOB)      + "\n")
        f.write("frac_YOB:"     + str(frac_YOB)      + "\n") 
        f.write("R0YA:"     + str(R0YA)      + "\n")
        f.write("R0OA:"     + str(R0OA)      + "\n")
        f.write("R0YB:"     + str(R0YB)      + "\n")
        f.write("R0OB:"     + str(R0OB)      + "\n")
        f.write("betaA:"    + str(betaA)     + "\n")
        f.write("betaB:"    + str(betaB)     + "\n")
        f.write("gammaA:"   + str(gammaA)    + "\n")
        f.write("gammaB:"   + str(gammaB)    + "\n")
        f.write("----------------------------------" + "\n")
    f.close()
    
    return N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter, prop_Y 
 
