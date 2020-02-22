from Player import Player
from Playground import Playground
import tqdm
import numpy as np

episodes = 50
time_steps = 500

agent = Player('DQN-Training')
playgound = Playground(100.0, 100.0, False, agent, Player('random player'))
done = False
batch_size = 32

def train():
    for e in range(episodes):
        playgound.reset_game()
        state = playgound.get_state(agent)
        reward_average = np.zeros(time_steps)
        for t in tqdm.tqdm(range(time_steps)):
            action = agent.act(state)
            next_state, reward, done = playgound.simulate_time_step(agent, action)
            #reward = reward if not done else -10
            reward_average[t] = reward
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            if done:
                #print("episode: {}/{}, score: {}".format(e, episodes, t))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        print('episode {}/{}'.format(e, episodes), ' average reward', reward_average.mean())
        #if e % 10 == 0:
        #    playgound2 = Playground(200.0, 200.0, True, agent, Player('random player'))
        #    playgound2.start_game()
        agent.save('test1.h5')