import pygame, sys, random, math
from pygame.locals import *
from AIv3_001 import AI

FPS = 50
WINDOWWIDTH = 450
WINDOWHEIGHT = 300
TRACKHEIGHT = WINDOWHEIGHT - 175
TRACKWIDTH = 1

center = ((WINDOWWIDTH / 2), TRACKHEIGHT)
CARTSIZE = (40, 24) #(x, y)
POLESIZE = (6, 100)
PIVOTSIZE = 4
POLEDISPLACEMENT = -((POLESIZE[1] / 2) - PIVOTSIZE)

BLACK =     (0  ,  0,  0)
WHITE =     (255,255,255)
TAN =       (210,180,140)
GREY =      (128,128,128)
LIGHTGREY = (225,225,225)

BGCOLOR = WHITE
CARTCOLOR = BLACK
POLECOLOR = TAN
PIVOTCOLOR = GREY
TRACKCOLOR = BLACK

PIXALSPERMETER = 100

#physics
GRAVITY = 9.8  # m/sec^2
POLELENGTH = (POLESIZE[1] / PIXALSPERMETER / 2)  # meters (half of actual length)
FORCEMAGNITUDE = 10  # newtons (magnitude of force each action is)
POLEMASS = 0.1  # Kg
CARTMASS = 1.0  # Kg
POLEMASSLENGTH = POLELENGTH * POLEMASS #newton meters
TOTALMASS = POLEMASS + CARTMASS  # Kg
TAU = 1 / FPS #change in time between frames

#thresholds of when to restart
X_THRESHOLD = 2.4 #meters
ANGLE_THRESHOLD = 12 * 2 * math.pi / 360 #12 degrees


class rectangle(object):
    def __init__(self, center, size, color):
        self.color = color
        self.center = (int(center[0]), int(center[1]))
        self.pointList = [(self.center[0] - (size[0] / 2), self.center[1] - (size[1] / 2)),
                          (self.center[0] + (size[0] / 2), self.center[1] - (size[1] / 2)),
                          (self.center[0] + (size[0] / 2), self.center[1] + (size[1] / 2)),
                          (self.center[0] - (size[0] / 2), self.center[1] + (size[1] / 2))]
        self.origonalPointList = list(self.pointList)

    def move(self, change):
        for i in range(len(self.pointList)):
            self.pointList[i] = ((self.pointList[i][0] + change, self.pointList[i][1]))

    def rotate(self, angle, pivotPoint):
        # translate the rectangle to origin
        for i in range(len(self.pointList)):
            self.pointList[i] = ((self.pointList[i][0] - pivotPoint[0], self.pointList[i][1] - pivotPoint[1]))

        # rotate points (x' = x*cos(angle)-y*sin(angle), y' = y*cos(angle)+x*sin(angle))
        for i in range(len(self.pointList)):
            self.pointList[i] = (((self.pointList[i][0] * math.cos(angle)) - (self.pointList[i][1] * math.sin(angle)),
                                  (self.pointList[i][1] * math.cos(angle)) + (self.pointList[i][0] * math.sin(angle))))

        # move rectangle's points back to origonal position (now rotated)
        for i in range(len(self.pointList)):
            self.pointList[i] = ((self.pointList[i][0] + pivotPoint[0], self.pointList[i][1] + pivotPoint[1]))

    def draw(self):
        # make the points whole numbers
        outputPointList = list(self.pointList)
        for i in range(len(self.pointList)):
            if (self.pointList[i][0] % 1 < 0.5) and (self.pointList[i][1] % 1 < 0.5):
                outputPointList[i] = ((int(self.pointList[i][0]), int(self.pointList[i][1])))
            elif (self.pointList[i][0] % 1 < 0.5):
                outputPointList[i] = ((int(self.pointList[i][0]), int(self.pointList[i][1]) + 1))
            elif (self.pointList[i][1] % 1 < 0.5):
                outputPointList[i] = ((int(self.pointList[i][0]) + 1, int(self.pointList[i][1])))
            else:
                outputPointList[i] = ((int(self.pointList[i][0]) + 1, int(self.pointList[i][1]) + 1))
        pygame.draw.polygon(DISPLAYSURF, self.color, outputPointList, 0)

    def reset(self):
        self.pointList = list(self.origonalPointList)

#calculates next state given current state and action
def step(state, action):
    x, x_dot, theta, theta_dot = state
    force = FORCEMAGNITUDE if action == 1 else -FORCEMAGNITUDE
    costheta = math.cos(theta)
    sintheta = math.sin(theta)

    temp = (force + POLEMASSLENGTH * theta_dot * theta_dot * sintheta) / TOTALMASS
    thetaacc = (GRAVITY * sintheta - costheta * temp) / (
    POLELENGTH * (4.0 / 3.0 - POLEMASS * costheta * costheta / TOTALMASS))
    xacc = temp - POLEMASSLENGTH * thetaacc * costheta / TOTALMASS
    x = x + TAU * x_dot
    x_dot = x_dot + TAU * xacc
    theta = theta + TAU * theta_dot
    theta_dot = theta_dot + TAU * thetaacc
    newState = (x, x_dot, theta, theta_dot)

    return newState


def draw(cartLocation, poleAngle):
    #pygame.draw.line(DISPLAYSURF, LIGHTGREY, (center[0]-((CARTSIZE[0]/2)+(X_THRESHOLD*PIXALSPERMETER)),0), (center[0]-((CARTSIZE[0]/2)+(X_THRESHOLD*PIXALSPERMETER)),WINDOWHEIGHT), 2)
    #pygame.draw.line(DISPLAYSURF, LIGHTGREY, (center[0]+((CARTSIZE[0]/2)+(X_THRESHOLD*PIXALSPERMETER)),0), (center[0]+((CARTSIZE[0]/2)+(X_THRESHOLD*PIXALSPERMETER)),WINDOWHEIGHT), 2)
    pygame.draw.line(DISPLAYSURF, TRACKCOLOR, (0, TRACKHEIGHT), (WINDOWWIDTH, TRACKHEIGHT), TRACKWIDTH)
    cart.draw()
    pole.rotate(poleAngle, (cartLocation, TRACKHEIGHT))
    pole.draw()
    pygame.draw.circle(DISPLAYSURF, PIVOTCOLOR, (int(cartLocation), TRACKHEIGHT), PIVOTSIZE, 0)


def moveCartPole(change):
    cart.move(change)
    pole.move(change)


#returns if the cart pole has passed its boundries
def isDone(state):
    return ((math.fabs(state[0]) > X_THRESHOLD) or (math.fabs(state[2]) > ANGLE_THRESHOLD))


def main():
    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CartPole')

    state = (0, 0, 0, 0)
    reward = 1
    episode = 0
    done = False
    steps = 0
    allSteps = 0
    stepsPerEpisode = []
    avg = 0

    while True:
        FPSCLOCK.tick(FPS)

        #close window when user exits
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BGCOLOR) #background surface

        steps += 1

        action = AI.getState(state, reward)
        oldState = state
        state = step(state, action)
        x_delta = (state[0] - oldState[0]) * PIXALSPERMETER
        angle_delta = state[2] - oldState[2]
        cartLocation = center[0] + (state[0] * PIXALSPERMETER)

        #display episode and avg reward
        font = pygame.font.Font(None, 20)
        epText = ("Episode: " + str(episode) + " Reward: " + str(steps) + " Average reward: " + str(avg))
        text = font.render(epText,1,(10,10,10))
        textpos = text.get_rect()
        DISPLAYSURF.blit(text, textpos)

        moveCartPole(x_delta)
        draw(cartLocation, angle_delta)
        pygame.display.flip()

        reward = 1
        done = isDone(state)
        if done:
            state = (0, 0, 0, 0)
            cart.reset()
            pole.reset()
            done = True
            episode += 1
            allSteps += steps
            stepsPerEpisode.append(steps)

            #print steps took to acheive a 195 reward avg over 100 episodes
            if episode <= 100:
                avg = int(allSteps/episode)
            else:
                for i in range(100):
                    avg += stepsPerEpisode[-i]
                avg = int(avg/100)
            if episode == 150:
                print('Avg after 150 episodes: ' + str(avg))
                avg = 0
                episode = 0
                allSteps = 0
                AI.__init__(2,4)
                
                
            steps = 0
            reward = 0


if __name__ == '__main__':
    cart = rectangle(center, CARTSIZE, CARTCOLOR)
    pole = rectangle((center[0], (center[1] + POLEDISPLACEMENT)), POLESIZE, POLECOLOR)
    AI = AI(2,4)
    main()
