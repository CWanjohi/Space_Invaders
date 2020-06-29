#Deep Q Network for Atari Space Invaders.
## OVERVIEW

This code is originally by [Lee Robinson](https://github.com/leerob/Space_Invaders) and [Siraj](https://github.com/llSourcell/pong_neural_network_live).
It is a simple implementation of a Deep Q Network which learns to play Atari Space Invaders.

## FILES:
spaceinvaders.py- game. Contains main function to run the program.
    -ship- your character.
    -enemy- single alien
    -enemygroup- the array of enemy aliens
    -blocker- rectangle object between ship and enemygroup
    -mystery- red alien ship that passes at top of window
RL.py- Reinforcement learning using 5-layer Convolution Neural Network.
checkpoints- directory to save progress of reinforcement learning process


## TO DO:
-increase screen size from (WxH) 600x800 to 800x900.
-keep ship from dying during 'observing' mode.


## ISSUES:
Some things I have changed from the original sources.
- For each of the sprites' update method, the line to blit the image to the screen eg. 'SpaceInvaders().screen.blit(self.image, self.rect)'
  originally was 'game.screen.blit(self.image, self.rect)'.
  But using the original line fired the error 'NameError: name 'game' is not defined'.
- I was running this on a non-gpu machine.
  To run on a machine with a GPU, uncomment RL.py line 31 'with tf.device('/gpu:0'):'
  Also, import tensorflow-gpu normally i.e 'import tensorflow as tf'. comment RL.py line 9 'tf.disable_v2_behavior()'

## DEPENDECIES
* tensorflow (https://www.tensorflow.org)
* cv2 (http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)
* numpy
* random
* collections
* pygame

Use [pip](https://pypi.python.org/pypi/pip) to install the dependencies.

## USAGE
Run the game using the terminal command
```bash
cd SpaceInvaders
python spaceinvaders.py
```
**Note:** If you're using Python 3, replace the command "python" with "python3".

## CREDITS
Original code source:
### Lee Robinson https://github.com/leerob/Space_Invaders for the Atari Space Invaders game.
### Siraj Raval https://github.com/llSourcell/pong_neural_network_live for the CNN network.
