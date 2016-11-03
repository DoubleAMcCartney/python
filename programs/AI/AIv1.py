import random, math

from bisect    import insort
from itertools import islice

class AI():
    def __init__(self, actions, stateVars):
        self.maxData = 10000
        self.rewardThreshold = 5
        
        self.allSteps = []
        self.episodeSteps = []
        self.actions = actions
        self.stateVars = stateVars
        self.minTries = math.factorial(self.actions)
        self.weight = [1] * self.stateVars
        self.stdDev = [0] * self.stateVars
        #self.maxSim = math.factorial(self.stateVars) * self.actions + 1    ### only efficient for 6 stateVars
        self.maxSim = 49                                                    ### need to find an equation that works for any amount of stateVars
        self.simSlope = 1 / self.maxSim

    #find statistacal significance of each state variable
    #if there is a stateVar that has no correlation to the best action, I want this to give it a weight of 0
    def findWeight(self):
        states = len(self.allSteps)

        if states < 2:
            return
        
        #find mean action
        actMean = 0
        for i in range(states):
            actMean += self.allSteps[i][(self.stateVars)]
        actMean /= states

        #find std def of actions
        actStdDev = 0
        for i in range(states):
            actStdDev += math.pow((self.allSteps[i][(self.stateVars)]-actMean),2)
        actStdDev = math.sqrt(actStdDev/(states-1))

        if actStdDev == 0:
            return

        #find mean reward
        rewMean = 0
        for i in range(states):
            rewMean += self.allSteps[i][(self.stateVars+1)]
        rewMean /= states
        
        #find std dev of rewards
        rewStdDev = 0
        for i in range(states):
            rewStdDev += math.pow((self.allSteps[i][(self.stateVars+1)]-rewMean),2)
        rewStdDev = math.sqrt(rewStdDev/(states-1))

        if rewStdDev == 0:
            return

        #find correlation between action and reward
        rActRew = 0
        for i in range(states):
            rActRew += ((self.allSteps[i][self.stateVars]-actMean)/actStdDev)*((self.allSteps[i][self.stateVars+1]-rewMean)/rewStdDev)
        rActRew /= states
    
        #find 2-dim correlations with states
        rStateAct = [None] * self.stateVars
        rStateRew = [None] * self.stateVars
        for var in range(self.stateVars):
            
            #find mean of state element
            mean = 0
            for i in range(states):
                mean += self.allSteps[i][var]
            mean /= states

            #find std dev of state element
            self.stdDev[var] = 0
            for i in range(states):
                self.stdDev[var] += math.pow((self.allSteps[i][var]-mean),2)
            self.stdDev[var] = math.sqrt(self.stdDev[var]/(states-1))

            #find correlation of state element to action
            r = 0
            for i in range(states):
                r += ((self.allSteps[i][var]-mean)/self.stdDev[var])*((self.allSteps[i][self.stateVars]-actMean)/actStdDev)
            r /= states
            rStateAct[var] = r

            #find correlation of state element to reward
            r = 0
            for i in range(states):
                r += ((self.allSteps[i][var]-mean)/self.stdDev[var])*((self.allSteps[i][self.stateVars+1]-rewMean)/rewStdDev)
            r /= states
            rStateRew[var] = r

        # calculate correlation of each state variable and action pair to reward
        self.weight = []
        for i in range(self.stateVars):
            self.weight.append(math.sqrt(math.fabs((math.pow(rStateRew[i],2)+math.pow(rActRew,2)-2*rStateAct[i]*rStateRew[i]*rActRew)-rStateAct[i])))

        print(str(self.weight))

    #return n closest states to state given
    #uses weight and stdDev to do this
    def closestStates(self, state, n):
        simStates = []
        steps = len(self.allSteps)

        #store the difference of each recorded state to current state in a list
        diffs = []
        for i in range(steps):
            diff = 0
            for j in range(self.stateVars):
                diff += math.fabs((self.weight[j] * ((self.allSteps[i][j]-state[j])/self.stdDev[j])))
            diffs.append(diff)

        #find nth lowest diff in list
        it   = iter(diffs)
        mins = sorted(islice(it, n))
        for el in it:
            if el < mins[-1]:
                insort(mins, el)
                mins.pop()
        maxDiff = mins[-1]

        #create list of closest states
        for i in range(steps):
            if diffs[i] <= maxDiff:
                simStates.append(self.allSteps[i])
           
        return simStates


    #detemins next action
    def getAction(self, state):
        steps = len(self.allSteps)

        #formula for calculating the amount of simStates to use
        n = int((self.maxSim*((1/(self.maxSim*(1/self.simSlope)))*len(self.allSteps))/(math.sqrt((1+(1/(self.maxSim*(1/self.simSlope))*len(self.allSteps))**2)))))
        if n == 0:
            return random.randint(0,(self.actions-1))
        #print(str(n))  ### uncomment this to see output of formula
        simStates = self.closestStates(state, n)
    
        #ensure that each action has been tried at least self.minTries
        for i in range(self.actions):
            count = 0
            for j in range((len(simStates))):
                if simStates[j][self.stateVars] == i:
                    count += 1
            if count < self.minTries:
                return i

        #calculate avg reward of each action for the sim states
        statejReward = 0
        avgRewards = [0]*self.actions
        avgRew = 0
        for j in range(self.actions):
            lenStatej = 0
            for i in range(len(simStates)):
                if simStates[i][self.stateVars] == j:
                    avgRewards[j] += simStates[i][self.stateVars+1]
                    lenStatej += 1
            avgRewards[j] /= lenStatej
            avgRew += avgRewards[j]          
        avgRew /= self.actions

        if avgRew == 0:
            return random.randint(0,1)

        confidence = [0]*self.actions
        for j in range(self.actions):
            confidence[j] = 100*((avgRewards[j]-avgRew) / avgRew)
            if confidence[j] == max(confidence):
                if random.randint(0,100)>((100/self.rewardThreshold)*(confidence[j])):
                    return random.randint(0,(self.actions-1))
                else:
                    return j    
        return random.randint(0,(self.actions-1))

       
    #delete steps when maxData is reached        
    def deleteSteps(self):
        while len(self.allSteps) > self.maxData:
            del self.allSteps[random.randint(0,(len(self.allSteps)-1))]
            

    #function called by environment     
    def getState(self, state, reward):
        state = list(state) #convert state tupple to list
        action = self.getAction(state) #get action
        state.append(action) #add action
        state.append(0) #add reward
        self.episodeSteps.append(state) #add state to list of states in episode

        if reward == 0:
            #add data from all states in episode when episode ends
            for states in range(len(self.episodeSteps)):
                self.allSteps.append(self.episodeSteps[states])
            self.episodeSteps = []
            self.findWeight()
            if len(self.allSteps) > self.maxData:
                self.deleteSteps()
        else:
            #add 1 to reward of each state in episode
            #for any given state, the reward increases as the episode continues
            for states in range(len(self.episodeSteps)):
                self.episodeSteps[states][self.stateVars + 1] += reward
                
        return action

