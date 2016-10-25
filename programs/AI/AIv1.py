import random, math

class AI():
    def __init__(self):
        self.deviation = [0.5, 0.2, 0.08, 0.03]
        self.devMultiplier = 6.5
        self.rewardThreshold = 20
        self.allSteps = []
        self.episodeSteps = []
        self.minTries = 2

    #find similar stats
    def getSimStates(self, state, deviation):
        simStates = []
        for states in range(len(self.allSteps)):
            if (math.fabs(state[0] - self.allSteps[states][0]) < deviation[0] and
                math.fabs(state[1] - self.allSteps[states][1]) < deviation[1] and
                math.fabs(state[2] - self.allSteps[states][2]) < deviation[2] and
                math.fabs(state[3] - self.allSteps[states][3]) < deviation[3] and
                math.copysign(1.0,state[0])==math.copysign(1.0,self.allSteps[states][0]) and
                math.copysign(1.0,state[1])==math.copysign(1.0,self.allSteps[states][1]) and
                math.copysign(1.0,state[2])==math.copysign(1.0,self.allSteps[states][2]) and
                math.copysign(1.0,state[3])==math.copysign(1.0,self.allSteps[states][3])):
                simStates.append(self.allSteps[states])
        else:
            return simStates

    #detemins next action
    def getAction(self, state):
        simStates = self.getSimStates(state, self.deviation)

        if len(simStates) < 10:
            deviation = list(self.deviation)
            for i in range(len(self.deviation)):
                deviation[i] = self.devMultiplier*self.deviation[i]
            simStates = self.getSimStates(state, deviation)
        if len(simStates) < 10:
            #print('Less than 10 sim states')
            return random.randint(0,1)
        else:
            #ensure that each action has been tried at least self.minTries
            act1 = simStates[0][4]
            act2count = 0
            for states in range(len(simStates)):
                if simStates[states][4] != act1:
                    act2count += 1
            if act2count < self.minTries:
                if act1 == 0:
                    return 1
                else:
                    return 0

        #calculate avg reward of each action for the sim states
        state0 = []
        state1 = []
        state0Reward = 0
        state1Reward = 0
        lenState0 = 0
        lenState1 = 0
        for i in range(len(simStates)):
            if simStates[i][4] == 0:
                state0.append(simStates[i])
                state0Reward += simStates[i][5]
                lenState0 += 1
            else:
                state1.append(simStates[i])
                state1Reward += simStates[i][5]
                lenState1 += 1
        state0Reward /= lenState0
        state1Reward /= lenState1

        #the higher the diff in reward, the less likely a random action will be taken
        if (state1Reward >= state0Reward):
            if random.randint(0,100)>((100/self.rewardThreshold)*state1Reward-state0Reward):
                #print('Random 1')
                return random.randint(0,1)
            else:
                return 1
        else:
            if random.randint(0,100)>((100/self.rewardThreshold)*state0Reward-state1Reward):
                #print('Random 2')
                return random.randint(0,1)
            else:
                return 0

    #function called by environment     
    def getState(self, state, reward):
        state = list(state) #convert state tupple to list
        action = self.getAction(state) #get action
        state.append(action) #add action
        state.append(0) #add reward
        self.episodeSteps.append(state) #add state to list of states in episode

        if reward == 1:
            #add 1 to reward of each state in episode
            #for any given state, the reward increases as the episode continues
            for states in range(len(self.episodeSteps)):
                self.episodeSteps[states][5] += reward
        else:
            #add data from all states in episode when episode ends
            for states in range(len(self.episodeSteps)):
                self.allSteps.append(self.episodeSteps[states])
            self.episodeSteps = []

        return action

