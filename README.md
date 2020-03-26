# CUBE AND BALLS
# Reinforcement Learning and (soon) Deep Reinforcement Learning

## Introduction
The goal of this project is to create a game and develop an AI Bot able to play it from scratch. We use Q-Learning to train 
agent for "easy" version of the game and soon I'll create a DQN that will be able to play in "hard" mode where balls start 
fall faster with time.

## Install
This project requires Python 3.6, Pygame, Numpy and Matplotlib (optional, needs for progress visualization after game session).
Soon this project will be using Keras with Tensorflow backend.

``` bash
git clone https://github.com/flash10042/cube-and-balls.git
```

## Run
To run just a game without an agent type at Terminal:
```
python game.py
```
To run game with agent playing it type next command:
```
python qlearning.py
```
Agent is already trained and working in 'demo' mode. To train him more switch DEMO_MODE value to 0 at line 9 of qlearning.py.
To use new random Q-Table comment line 33 and uncomment line 32 at qlearining.py

Also, you can play around SHOW_EVERY values to see more or less often agent gameplay.
