from packages import * 

# Erdos-Renyi Graph
def er(N,p):
   
    G = nx.Graph()    
    G.add_nodes_from(range(N))    
    edges = set()
    
    for i in range(N):        
        for j in range(N):            
            if i != j:            
                if random.random() < p:                
                    edges.add((i,j))
    
    G.add_edges_from(edges)
    
    return G


# Scale-free network employing the Barabasi-Albert algorithm
def ba(N,m):

    G = nx.Graph()    
    m0= 4 # Initial nodes
    G.add_nodes_from(range(m0))    
    edges = []
    
    for i in range(m0): # Add inizial edges       
        for j in range(i,m0):                            
                if i != j:                
                    edges.append((i,j))    
    G.add_edges_from(edges)
    
    prob = []
    
    for i in range(m0,N):
        
        G.add_node(i)
        
        for j in range(m):
            for k in list(G.nodes):
                for z in range(nx.degree(G,k)):
                    prob.append(k)
                    
            node = random.choice(prob)
            
            G.add_edge(node,i)
        
            prob.clear()
            
    return G


def SIRV(old_stateA, old_stateB, GB, betaB, gammaB, phi, p):
     
    new_stateB = old_stateB.copy()
    
    # Infection phase                
    for node in range(len(old_stateB)):
                    
        if old_stateB[node] == 'IB':
        
            l = GB.neighbors(node)

            for i in l:                
                if old_stateB[i] == 'SB':                    
                    x = random.random()                    
                    if x < betaB:
                        new_stateB[i] = 'IB'
    
    # Recovery phase                
    for node in range(len(old_stateB)):
        
        if old_stateB[node] == 'IB':
            x = random.random()
            if x < gammaB:
                new_stateB[node] = 'RB'
                
    # Vaccination phase                
    for node in range(len(old_stateB)):
                    
        if (old_stateB[node] == 'SB' and old_stateA[node] == 'IA'):
        
            l = GB.neighbors(node)
            
            count = 0
            for i in l:                
                if old_stateB[i] == 'IB': 
                    count += 1
            if count >= phi:
                x = random.random()                    
                if x < p:
                    new_stateB[node] = 'VB'
       
    return new_stateB


def SIR(old_stateA, old_stateB, GA, betaA, gammaA):
    
    new_stateA = old_stateA.copy()
    
    # Infection phase                
    for node in range(len(old_stateA)):
                    
        if old_stateA[node] == 'IA':
        
            l = GA.neighbors(node)

            for i in l:                
                if old_stateA[i] == 'SA':                    
                    x = random.random()                    
                    if x < betaA:
                        new_stateA[i] = 'IA'
    
    # Recovery phase                
    for node in range(len(old_stateA)):
        
        if old_stateA[node] == 'IA':
            x = random.random()
            if x < gammaA:
                new_stateA[node] = 'RA'
                
     # Information phase                
    for node in range(len(old_stateA)):
        if (old_stateA[node] == 'SA' and old_stateB[node] == 'IB'):
            new_stateA[node] = 'IA'
            
    return new_stateA


def propagator(which_out, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max):

    dt = 0
    
    NB = GB.number_of_nodes()
    NA = GA.number_of_nodes()
    node_labelsB = GB.nodes()
    node_labelsA = GA.nodes()
    
    old_stateA = ['SA' for i in node_labelsA]
    old_stateB = ['SB' for i in node_labelsB]
   
    for i in range(10):
        seed = random.choice(range(NB))
        old_stateA[seed] = 'IA' 
        old_stateB[seed] = 'IB' 
    
    if which_out == "c":
        SA_frac = []
        IA_frac = []
        RA_frac = []
        SB_frac = []
        IB_frac = []
        RB_frac = []
        VB_frac = []
        
    while dt < t_max:
        
        new_stateA = SIR(old_stateA, old_stateB, GA, betaA, gammaA) 
        new_stateB = SIRV(old_stateA, old_stateB, GB, betaB, gammaB, phi, p)

        old_stateA = new_stateA.copy()
        old_stateB = new_stateB.copy()

        if which_out == "c":
            SA_frac.append(new_stateA.count('SA')/NA)
            IA_frac.append(new_stateA.count('IA')/NA)
            RA_frac.append(new_stateA.count('RA')/NA)
            SB_frac.append(new_stateB.count('SB')/NB)
            IB_frac.append(new_stateB.count('IB')/NB)
            RB_frac.append(new_stateB.count('RB')/NB)
            VB_frac.append(new_stateB.count('VB')/NB)

        elif which_out == "f":
            SA_frac = new_stateA.count('SA')/NA
            IA_frac = new_stateA.count('IA')/NA
            RA_frac = new_stateA.count('RA')/NA
            SB_frac = new_stateB.count('SB')/NB
            IB_frac = new_stateB.count('IB')/NB
            RB_frac = new_stateB.count('RB')/NB
            VB_frac = new_stateB.count('VB')/NB

        else:
            print("Not valid option!")
        
        dt += 1
    
    return (SA_frac, IA_frac, RA_frac, SB_frac, IB_frac, RB_frac, VB_frac)


def grid_search(filename, niterations, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max):

    RA_mean = []
    RB_mean = []
    VB_mean = []

    for i in range(len(betaA)):
        # Change number of workers
        res = Parallel(n_jobs=-1, verbose=0)(delayed(propagator)("f", GA, GB, betaA[i], gammaA, betaB[i], gammaB, phi, p, t_max) for k in range(niterations))
        df = pd.DataFrame(res, columns=["SA", "IA", "RA", "SB", "IB", "RB", "VB"])
        RA_mean.append(df["RA"].mean())
        RB_mean.append(df["RB"].mean())
        VB_mean.append(df["VB"].mean())
        
    rows = zip(betaA, betaB, RA_mean, RB_mean, VB_mean) 
    
    with open(filename, "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    return


def mean_degree(G):
    k = 0
    N = G.number_of_nodes()
    for i in range(N):
        k += G.degree[i]
    k_mean = k/N
    
    return k_mean 


def SIR_AB(old_stateA, old_stateAA, old_stateB, GA, betaA, gammaA):
    
    new_stateA = old_stateA.copy()
    new_stateAA = old_stateAA.copy()
    
    # Infection phase                
    for node in range(len(old_stateA)):
                    
        if old_stateA[node] == 'IA':
        
            l = GA.neighbors(node)

            for i in l:                
                if old_stateA[i] == 'SA':                    
                    x = random.random()                    
                    if x < betaA:
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
        if (old_stateA[node] == 'SA' and old_stateB[node] == 'IB'):
            new_stateA[node] = 'IA'
            new_stateAA[node] = 'IAB'
            
    return new_stateA, new_stateAA


def propagator_AB(which_out, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max):

    dt = 0
    
    NB = GB.number_of_nodes()
    NA = GA.number_of_nodes()
    node_labelsB = GB.nodes()
    node_labelsA = GA.nodes()
    
    old_stateA = ['SA' for i in node_labelsA]
    old_stateB = ['SB' for i in node_labelsB]
   
    for i in range(10):
        seed = random.choice(range(NB))
        old_stateA[seed] = 'IA' 
        old_stateB[seed] = 'IB' 
    
    if which_out == "c":
        SA_frac = []
        IA_frac = []
        RA_frac = []
        SB_frac = []
        IB_frac = []
        RB_frac = []
        VB_frac = []
    
    rhoAA = []
    rhoAB = []
    
    old_stateAA = old_stateA.copy()
    
    while dt < t_max:
        
        new_stateA, new_stateAA = SIR_AB(old_stateA, old_stateAA, old_stateB, GA, betaA, gammaA) 
        new_stateB = SIRV(old_stateA, old_stateB, GB, betaB, gammaB, phi, p)
        
        old_stateA = new_stateA.copy()
        old_stateAA = new_stateAA.copy()
        old_stateB = new_stateB.copy()

        if which_out == "c":
            SA_frac.append(new_stateA.count('SA')/NA)
            IA_frac.append(new_stateA.count('IA')/NA)
            RA_frac.append(new_stateA.count('RA')/NA)
            SB_frac.append(new_stateB.count('SB')/NB)
            IB_frac.append(new_stateB.count('IB')/NB)
            RB_frac.append(new_stateB.count('RB')/NB)
            VB_frac.append(new_stateB.count('VB')/NB)
            rhoAA.append(new_stateAA.count('IAA')/NA)
            rhoAB.append(new_stateAA.count('IAB')/NA)

        elif which_out == "f":
            SA_frac = new_stateA.count('SA')/NA
            IA_frac = new_stateA.count('IA')/NA
            RA_frac = new_stateA.count('RA')/NA
            SB_frac = new_stateB.count('SB')/NB
            IB_frac = new_stateB.count('IB')/NB
            RB_frac = new_stateB.count('RB')/NB
            VB_frac = new_stateB.count('VB')/NB

        else:
            print("Not valid option!")
        
        dt += 1
        
    return (IB_frac, rhoAA, rhoAB)


def init():

    N = 10000

    # Information Network Parameters
    kA = 8
    pA = kA/(N-1)
    GA = nx.erdos_renyi_graph(N,pA)
    kA_calc = mean_degree(GA)

    # Disease Network Parameters
    kB = 8
    pB = kB/(N-1)
    GB = nx.erdos_renyi_graph(N,pB)
    kB_calc = mean_degree(GB)

    betaA = np.linspace(0, 0.2, 20)
    gammaA = 0.2
    R0A = kA_calc * betaA / gammaA
    betaB = np.linspace(0, 0.2, 20) 
    gammaB = 0.2
    R0B = kB_calc * betaB / gammaB

    phi = 3
    p = 0.8

    t_max = 100
    niter = 100

    with open("parameters.txt", "a") as f:
        f.write("--------" + "\n")
        f.write("N:"       + str(N)       + "\n")
        f.write("kA mean:" + str(kA_calc) + "\n")
        f.write("kB mean:" + str(kB_calc) + "\n")
        f.write("R0A:"     + str(R0A)     + "\n")
        f.write("R0B:"     + str(R0B)     + "\n")
        f.write("betaA:"   + str(betaA)   + "\n")
        f.write("betaB:"   + str(betaB)   + "\n")
        f.write("gammaA:"  + str(gammaA)  + "\n")
        f.write("gammaB:"  + str(gammaB)  + "\n")
        f.write("--------" + "\n")
    f.close()

    return N, GA, GB, betaA, gammaA, betaB, gammaB, phi, p, t_max, niter 
