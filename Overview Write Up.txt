FILES:
spaceinvaders.py- game. Contains main function to run the program.
    -ship- your character.
    -enemy- single alien
    -enemygroup- the array of enemy aliens
    -blocker- rectangle object between ship and enemygroup
    -mystery- red alien ship that passes at top of window

Run game using terminal command 'python spaceinvaders.py'

RL.py- Reinforcement learning using 5-layer Convolution Neural Network.
checkpoints- directory to save progress of reinforcement learning process

WRITE UP.
CNN analyzes present and next frame of the game to make a decision.
A decision can either be to stay put, shoot, move left or move right. Stay/Do nothing is the most probable decision.
The AI agent creates a Q-table with column=all possible actions, row=all possible states.
Each cell of the Q-table is filled with the max reward for doing that action in the given state. Max reward is calculated using Bellman Equation.
Reward=1 if alien is shot, 0 if ship is killed or no alien is killed. (step function)
The AI agent fills in the Q-Table accordingly.
At the start of the game, the AI agent uses an epsilon-greedy technique- random actions.
As the AI unintentionally stumbles upon rewards or penalties, it starts to associate performing certain actions in certain states as either good or bad.
As training goes on, the weight values are readjusted such that at the end of the learning, the calculated outputs
given by an AI agent are similar to the expected outputs.
The value of epsilon (learning rate) slowly decays from one to zero as training progresses.
At zero epsilon, the AI agent has fully learnt the environment and makes the best moves possible.
The AI agent saves learning progress in a checkpoints file after every 5000 steps.

TO DO:
- make update ship tied to AI agent's four possible actions.
ACTIONS =   0-> stay (0.6 probability)
            1-> shoot(0.2 probability)
            2-> move left(0.1 probability)
            3-> move right(0.1 probability)
- Simulate space bar key pressed to start game (Press after 3 seconds). ======= DONE on spaceinvaders.py ln 607
- Initialize everything within getPresentFrame function- call spaceinvaders constructor
- Work out how to specialize getNextFrame function for this game.
- update ship after an AI selected action. LAST TO DO (UNCOMMENT ln 61-68)

REFERENCES
Chris Nicholson (2019). A Beginner's Guide to Multilayer Perceptrons (MLP). https://pathmind.com/wiki/multilayer-perceptron
Chris Nicholson (2019). A Beginner's Guide to Convolutional Neural Networks (CNNs). https://pathmind.com/wiki/convolutional-network
James Loy (May 14, 2018). How to build your own Neural Network from scratch in Python. https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6