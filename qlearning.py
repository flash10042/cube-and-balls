import game
import numpy as np
import matplotlib.pyplot as plt


env = game.Game()

# IF DEMO = 1 SHOWS AI SKILLS ELIF DEMO = 0 TRAINS AI
DEMO_MODE = 1

if DEMO_MODE:
	LEARNING_RATE = 0
	SHOW_EVERY = 1
	epsilon = 0
else:
	LEARNING_RATE = 0.1
	SHOW_EVERY = 2500
	epsilon = 0.25
DISCOUNT = 0.95
EPISODES = 25000

START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)


DISCRETE_OS_SIZE = [50, 100, 4, 4, 4]
discrete_os_win_size = (np.array(env.observation_space_high) - np.array(env.observation_space_low)) / DISCRETE_OS_SIZE

#-------------- Load existing or generate new QTable --------------------

#q_table = np.random.uniform(low=-5, high=0, size=(DISCRETE_OS_SIZE + [3]))
q_table = np.load('QTable.npy')


ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}



def get_discrete_state(state):
	discrete_state = (state - env.observation_space_low) / discrete_os_win_size
	return tuple(discrete_state.astype(np.int))


discrete_state = get_discrete_state(env.reset())


for episode in range(EPISODES):
	discrete_state = get_discrete_state(env.reset())
	if not episode % SHOW_EVERY:
		render = True
		print(episode)
	else:
		render = False
	crash = False
	while not crash:
		if np.random.random() >= epsilon:
			action = np.argmax(q_table[discrete_state])
		else:
			action = np.random.randint(0, 3)
		new_state, reward, crash = env.step(action)


		new_discrete_state = get_discrete_state(new_state)
		if render:
			env.display()

		if not crash:
			max_future_q = np.max(q_table[new_discrete_state])
			current_q = q_table[discrete_state + (action, )]
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[discrete_state+(action, )] = new_q
		else:
			q_table[discrete_state + (action,)] = -2

		discrete_state = new_discrete_state
	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		epsilon -= epsilon_decay_value

	score = env.get_score()

	ep_rewards.append(score)

	# ------------- IF YOU WANT TO SAVE Q-Table uncomment and create 'qtables' folder
	#if not episode % 1000:
	#	np.save(f"qtables/{episode}-qtable.npy", q_table)

	if not episode % SHOW_EVERY:
		average_reward = sum(ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
		aggr_ep_rewards['ep'].append(episode)
		aggr_ep_rewards['avg'].append(average_reward)
		aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))
		aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
		print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}')


plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min rewards")
plt.legend(loc=4)
plt.show()
