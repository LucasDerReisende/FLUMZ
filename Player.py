import random
from collections import deque

import numpy as np
from keras import Sequential
from keras.layers import Dense, LSTM, ConvLSTM2D
from keras.optimizers import Adam


class Player:
    _actions = ['shoot', 'right', 'left', 'do_nothing']
    _learning_rate = 0.003
    _gamma = 0.95
    _epsilon = 1.0
    _epsilon_min = 0.01
    _epsilon_decay = 0.995

    def __init__(self, player_type):
        self.player_type = player_type
        if player_type == 'DQN' or player_type == 'DQN-Training':
            self.model = self._build_model()
            self.memory = deque(maxlen=2000)

    def _build_model(self):
        model = Sequential()
        model.add(LSTM(units=100, return_sequences=True))
        model.add(Dense(100, activation='sigmoid'))
        model.add(Dense(100, activation='sigmoid'))
        model.add(Dense(4, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self._learning_rate))
        return model

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)

    def act(self, state):
        rand = random.random()
        if rand <= self._epsilon:
            return self._actions[random.randrange(len(self._actions))]
        else:
            actions = self.model.predict(state)
            best_action = np.argmax(actions[0]) % 4
            return self._actions[best_action]

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        mini_batch = random.sample(self.memory, batch_size)
        for (state, action, reward, next_state, done) in mini_batch:
            target = reward
            if not done:
                target = reward + self._gamma * np.amax(self.model.predict(state))
            target_f = self.model.predict(state)
            target_f[0][0][self._actions.index(action)] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self._epsilon > self._epsilon_min:
            self._epsilon *= self._epsilon_decay

    def random_move(self, prob_shoot, prob_turn):
        epsilon = random.random()
        if epsilon < prob_shoot:
            return self._actions[0]
        elif prob_shoot <= epsilon < prob_shoot + prob_turn:
            return self._actions[1]
        elif prob_shoot + prob_turn <= epsilon < prob_shoot + (2 * prob_turn):
            return self._actions[2]
        else:
            return self._actions[3]

    def do_move(self, state, move):
        if self.player_type == 'random player':
            return self.random_move(0.1, 0.1)
        elif self.player_type == 'DQN-Training':
            return move
        elif self.player_type == 'DQN':
            return self.act(state)