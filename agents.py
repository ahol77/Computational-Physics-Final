import numpy as np
from matplotlib import pyplot as plt

np.random.seed(3)
#Size of Square Grid, acts as a sphere with no boundary conditions
n = 50

#Number of moves we will allow
ticks = 5000

#Probability of Reproduction (1- x)
sheep_produce = 0.97
wolf_produce = 0.99

#Initial Energies 
wolf_energy_i = 40
sheep_energy_i = 25

#Initial Positions of Animals
def create_agent(number,typ):
    if typ == 0:
        energy = wolf_energy_i
    elif typ == 1:
        energy = sheep_energy_i
    xy = np.random.randint(1,n+1,(number,2))
    agent = []
    for i in range(number):
        agent.append([list(xy[i]), energy])
    return agent
sheep = create_agent(20,1)
wolf = create_agent(20,0)

#Energy from eating various things
energy_from_eating_sheep = 40
energy_from_eating_grass = 2
ticks_for_grass_to_grow = 60

def new_pos(agent):
    pos = [i[0] for i in agent]
    ent = len(pos)
    dp = np.random.randint(0,3,(ent,2)) - 1
    new = pos+dp
    new[new < 1] = n
    new[new > n] = 1
    for i in range(len(agent)):
        agent[i][0] = list(new[i])
    return agent

def generate_grass(n):
    coordinates = [[x,y] for x in range(1, n+1) for y in range(1, n+1)]
    grass = {}
    for i in range(len(coordinates)):
        z = ''.join(str(e) for e in coordinates[i])
        grass[z] = ticks_for_grass_to_grow        
    return grass

def grass_grow(grass):
    for g in grass:
        grass[g] += 1
    return grass

def decrease_energy(agent):
    for i in range(len(agent)):
        agent[i][1] = agent[i][1] - 1
    return agent

def wolf_eat_sheep(wolf, sheep):
    for i in range(len(wolf)):
        for j in range(len(sheep)):
            if wolf[i][0] == sheep[j][0] and sheep[j][1] != 0:
                wolf[i][1] += energy_from_eating_sheep
                sheep[j][1] = 0
                break
    return wolf, sheep

def sheep_eat_grass(sheep,grass):
    for i in range(len(sheep)):
        key = ''.join(str(e) for e in sheep[i][0])
        if grass[key] >= ticks_for_grass_to_grow:
            sheep[i][1] += energy_from_eating_grass
            grass[key] = 0
    return sheep, grass
    
def death(agent):
    death_list = []
    for i in range(len(agent)):
        if agent[i][1] == 0:
            death_list.append(i)
    for j in range(len(death_list)):
        spot = death_list[j]
        del agent[spot - j]
    return agent

def reproduce_wolf(wolf):
    for i in range(len(wolf)):
        rand = np.random.random()
        if rand > wolf_produce:
            wolf.append([wolf[i][0],wolf_energy_i])
    return wolf

def reproduce_sheep(sheep):
    for i in range(len(sheep)):
        rand = np.random.random()
        if rand > sheep_produce:
            sheep.append([sheep[i][0],sheep_energy_i])
    return sheep

def simulation(sheep, wolf):
    new_grass = generate_grass(n)
    tick_list = []
    sheep_total = []
    wolf_total = []
    grass_total = []
    for i in range(ticks):
        tick_list.append(i+1)
        #Grow grass
        grass = grass_grow(new_grass)
        #Move animals
        sheep = new_pos(sheep)
        wolf = new_pos(wolf)
        #Decrease energy of animals
        wolf = decrease_energy(wolf)
        sheep = decrease_energy(sheep)
        
        #Check if wolf dies from lack of energy
        wolf = death(wolf)
        #Check if the wolf eats a sheep
        wolf, sheep = wolf_eat_sheep(wolf, sheep)
        
        #Check if sheep dies from lack of energy
        sheep = death(sheep)
        #Check if remaining sheep eat grass
        sheep, grass = sheep_eat_grass(sheep, grass)

        #Check if sheep reproduces
        sheep = reproduce_sheep(sheep)
        #Check if wolf reproduces
        wolf = reproduce_wolf(wolf)
        
        #Check total number of sheep/wolves in the system at end of tick
        sheep_total.append(len(sheep))
        wolf_total.append(len(wolf))
        grass_total.append(len([k for k,v in grass.items() if float(v) >= ticks_for_grass_to_grow]))
        
        if len(sheep) == 0 or len(wolf) == 0:
            return tick_list, sheep_total, wolf_total, grass_total
        
    return tick_list, sheep_total, wolf_total, grass_total

t,s,w,g = simulation(sheep, wolf)
f = plt.figure()
f.set_figheight(6)
f.set_figwidth(10)
plt.title('Wolf and Sheep Population Through an Agent Based Model', fontsize = 22)
plt.xlabel('Number of Time Ticks', fontsize = 20)
plt.ylabel('Number of Agents', fontsize = 20)
plt.plot(t,s, label = 'Sheep')
plt.plot(t,w, label = 'Wolves')
#plt.plot(t,np.array(g)/50, label = 'Grass')
plt.legend(fontsize = 14)