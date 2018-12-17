import numpy as np
import matplotlib.pyplot as plt


#Multi-Armed Bandit Problem
#each bandit has one action (ex. bandit 1 is action 1, etc.)
#we will create 10 bandit objects, Every bandit gives rewards and these rewards have an average of Q(a) and a standard_deviation of 1
class Bandit:
	def __init__(self, average, standard_deviation=1):
		self.average = average
		self.standard_deviation = standard_deviation

	def give_reward(self):
		rewards = np.random.normal(self.average, self.standard_deviation)
		return rewards

#create 10 bandits with mean of 0 and a variance of 1
def create_bandits(num_bandits=10, average=0, standard_deviation=1):
	
	#create a vector of averages
	averages = np.random.normal(average,standard_deviation,num_bandits)
	
	#create a vector of standart deviation 
	standard_deviations = [standard_deviation]*num_bandits
	
	#create the bandits with a for cycle and store them into a bandits array. You need to give a value [i] to both averages and stardard_deviations
	bandits = []
	for i in range(num_bandits):
		bandits.append(Bandit(averages[i],standard_deviations[i]))
	return bandits, averages

#Silvia has only a number of estimates
#create your estimate Q = initial estimate
def initial_estimate(num_bandits, value_estimate):
	average_estimate = [value_estimate]*num_bandits #Q
	number_bandit_choices = [0]*num_bandits #N
	return average_estimate, number_bandit_choices

#greedy is someone that eats a lot, Silvia wants to take the max reward, but she doesn't know what it is, so she uses the estimates (what she think it is, now silvia has only 0)
def greedy(average_estimate, bandits, number_bandit_choices):
	choice = np.random.choice(np.argwhere(average_estimate == np.amax(average_estimate)).flatten().tolist()) #flatten the results
	reward = bandits[choice].give_reward()
	number_bandit_choices[choice] += 1
	average_estimate[choice] = (number_bandit_choices[choice]-1)/number_bandit_choices[choice]*average_estimate[choice]+1/number_bandit_choices[choice]*reward
	return reward, number_bandit_choices, average_estimate

def epsilon_greedy(average_estimate, bandits, number_bandit_choices, epsilon):
	p = np.random.uniform()#this will give me a number between 0 and 1 equally distributed
	if p>epsilon:
		choice = np.random.choice(np.argwhere(average_estimate == np.amax(average_estimate)).flatten().tolist()) #exploitation
	else:
		choice = np.random.choice(len(bandits)) #exploration
	reward = bandits[choice].give_reward()
	number_bandit_choices[choice] += 1
	average_estimate[choice] = (number_bandit_choices[choice]-1)/number_bandit_choices[choice]*average_estimate[choice]+1/number_bandit_choices[choice]*reward
	return reward, number_bandit_choices, average_estimate

# Chooses the action with the highest margin of error => the more you choose one action the least it chooses it
def UCB(average_estimate, bandits, number_bandit_choices, c, potentials, i): #c is a constant
	choice = np.random.choice(np.argwhere(potentials == np.amax(potentials)).flatten().tolist()) #flatten the results #instead of putting the average estimate I put the ucb values 
	reward = bandits[choice].give_reward()
	number_bandit_choices[choice] += 1
	average_estimate[choice] = (number_bandit_choices[choice]-1)/number_bandit_choices[choice]*average_estimate[choice]+1/number_bandit_choices[choice]*reward
	for j in range(num_bandits):
		if number_bandit_choices[j] > 0:
			potentials[j] = average_estimate[j]+c*np.sqrt((np.log(i))/number_bandit_choices[j])#i is the time, j is all the bandits (the positions of the bandits)
	return reward, number_bandit_choices, average_estimate, potentials

def question_one():
    average_rewards = [0]*1000
    for j in range(1,2001):
        bandits, averages = create_bandits()
        average_estimate, number_bandit_choices = initial_estimate(10, 0) #Q(a)=0
        rewards = []
        for i in range(1000):
            reward, number_bandit_choices, average_estimate = greedy(average_estimate, bandits, number_bandit_choices)
            rewards.append(reward)
        average_rewards = np.multiply((j-1)/j,average_rewards)+np.multiply(1/j,rewards)
    plt.plot(average_rewards)
question_one()

def question_two():
    average_rewards = [0]*1000
    for j in range(1,2001):
        bandits, averages = create_bandits()
        average_estimate, number_bandit_choices = initial_estimate(10, 5) #Q(a)=5
        rewards = []
        for i in range(1000):
            reward, number_bandit_choices, average_estimate = greedy(average_estimate, bandits, number_bandit_choices)
            rewards.append(reward)
        average_rewards = np.multiply((j-1)/j,average_rewards)+np.multiply(1/j,rewards)
    plt.plot(average_rewards)
question_two()

def question_three():
    average_rewards = [0]*1000
    epsilon = 0.1
    for j in range(1,2001):
        bandits, averages = create_bandits()
        average_estimate, number_bandit_choices = initial_estimate(10, 0) #Q(a)=0
        rewards = []
        for i in range(1000):
            reward, number_bandit_choices, average_estimate = epsilon_greedy(average_estimate, bandits, number_bandit_choices, epsilon)
            rewards.append(reward)
        average_rewards = np.multiply((j-1)/j,average_rewards)+np.multiply(1/j,rewards)
    plt.plot(average_rewards)
question_three()

def question_four():
    average_rewards = [0]*1000
    epsilon = 0.01
    for j in range(1,2001):
        bandits, averages = create_bandits()
        average_estimate, number_bandit_choices = initial_estimate(10, 0) #Q(a)=0
        rewards = []
        for i in range(1000):
            reward, number_bandit_choices, average_estimate = epsilon_greedy(average_estimate, bandits, number_bandit_choices, epsilon)
            rewards.append(reward)
        average_rewards = np.multiply((j-1)/j,average_rewards)+np.multiply(1/j,rewards)
    plt.plot(average_rewards)
question_four()

def question_five():
    average_rewards = [0]*1000
    for j in range(1,2001):
        bandits, averages = create_bandits()
        average_estimate, number_bandit_choices = initial_estimate(10, 0) #will be 5 here
        potentials = [float('inf')]*num_bandits
        rewards = []
        for i in range(1000):
            reward, number_bandit_choices, average_estimate, potentials = UCB(average_estimate, bandits, number_bandit_choices, c, potentials, i)
            rewards.append(reward)
        average_rewards = np.multiply((j-1)/j,average_rewards)+np.multiply(1/j,rewards)
    plt.plot(average_rewards)
question_five()


def plot(average_rewards, label, title, filename):
	fig = plt.figure()
	ax = plt.subplot(111)
	ax.xticks = np.arange(average_rewards[0])
	for i in range(average_rewards):
		ax.plot(average_rewards[i], label = label[i])
	plt.xlabel('number of trial')
	plt.ylabel('averaged time step reward')
	plt.title(title)
	ax.legend()
	fig.savefig(filename+'.png')
	ptl.close()
