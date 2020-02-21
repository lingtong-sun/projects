### MDP Value Iteration and Policy Iteration

import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)
PROBABILITY = 0
NEXT_STATE = 1
REWARD = 2
TERMINAL =  3


def get_future_rewards(P, s, a, value_function_k_minus_1):
	next_states = P[s][a]
	reward = 0
	for next_state in next_states:
		# reward += prob s' | s, pi(s) of Vpi k-1
		reward += next_state[PROBABILITY] * value_function_k_minus_1[next_state[NEXT_STATE]]

	return reward


def get_immediate_reward(P, s, a):
	reward = 0
	next_states = P[s][a]

	for next_state in next_states:
		reward += next_state[PROBABILITY] * next_state[REWARD]

	return reward

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
	"""

	value_function = np.zeros(nS)

	############################
	# YOUR IMPLEMENTATION HERE #

	while True:
		new_value_function = np.zeros(nS)
		for s in range(nS):
			new_value_function[s] = get_immediate_reward(P, s, policy[s]) + gamma * get_future_rewards(P, s, policy[s], value_function)

		if np.linalg.norm(new_value_function - value_function) < tol:
			break

		value_function = new_value_function

	############################
	return value_function


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

	new_policy = np.zeros(nS, dtype='int')

	############################
	# YOUR IMPLEMENTATION HERE #
	Q_PI_I = np.zeros(shape=(nS,nA))

	for s in range(nS):

		for a in range(nA):
			Q_PI_I[s, a] = get_immediate_reward(P, s, a) + gamma * get_future_rewards(P, s, a, value_from_policy)

		new_policy[s] = np.argmax(Q_PI_I[s])

	############################
	return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3):
	"""Runs policy iteration.

	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)

	############################
	# YOUR IMPLEMENTATION HERE #

	while True:
		new_policy = policy_improvement(P, nS, nA, value_function, policy, gamma)

		if np.array_equal(new_policy, policy):
			break

		value_function = policy_evaluation(P, nS, nA, new_policy, gamma, tol)
		policy = new_policy


	print(policy)
	print(value_function)
	print(np.linalg.norm(value_function))
	############################
	return value_function, policy

def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3):
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	############################
	# YOUR IMPLEMENTATION HERE #

	Q_PI_I = np.zeros(shape=(nS,nA))

	while True:
		new_value = np.zeros(nS)
		new_policy = np.zeros(nS, dtype='int')
		for s in range(nS):
			for a in range(nA):
				Q_PI_I[s, a] = get_immediate_reward(P, s, a) + gamma * get_future_rewards(P, s, a, value_function)


			new_policy[s] = int(np.argmax(Q_PI_I[s]))
			new_value[s] = np.max(Q_PI_I[s])

		if np.linalg.norm(new_value - value_function) < tol:
			break

		value_function = new_value
		policy = new_policy

	print(value_function)
	print(np.linalg.norm(value_function))
	print(policy)

	############################
	return value_function, policy

def render_single(env, policy, max_steps=100):
  """
    This function does not need to be modified
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as
      attributes.
    Policy: np.array of shape [env.nS]
      The action to take at a given state
  """

  episode_reward = 0
  ob = env.reset()
  for t in range(max_steps):
    env.render()
    time.sleep(0.25)
    a = policy[ob]
    ob, rew, done, _ = env.step(a)
    episode_reward += rew
    if done:
      break
  env.render();
  if not done:
    print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
  else:
  	print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":

	# comment/uncomment these lines to switch between deterministic/stochastic environments
	# env = gym.make("Deterministic-8x8-FrozenLake-v0")
	# env = gym.make("Deterministic-4x4-FrozenLake-v0")
	env = gym.make("Stochastic-4x4-FrozenLake-v0")

	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)
	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_pi, 100)

	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)
	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_vi, 100)


