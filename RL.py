# import tensorflow.compat.v1 as tf
import tensorflow as tf
import cv2 #read in pixel data
import spaceinvaders #our game class
import numpy as np #math computation
import random #random number generator
from collections import deque #queue data structure. fast appends. and pops. replay memory
from numpy.random import choice

# tf.disable_v2_behavior()

#hyper parameters
ACTIONS = 4 #stay-action[0], shoot-action[1], left-action[2], right-action[3]
#define our learning rate
GAMMA = 0.99
#for updating our gradient or training over time
INITIAL_EPSILON = 1.0
FINAL_EPSILON = 0.01
#how many frames to anneal epsilon
EXPLORE = 10000
OBSERVE = 300
USE_MODEL = True

SAVE_STEP = 5000 #store our experience after every 5000 steps
REPLAY_MEMORY = 200000

BATCH = 100 #randomly select a batch of 100 to train on from the replay memory

#create tensorflow graph
def createGraph():
	with tf.device('/gpu:0'):
		#convolutional layers. bias vector
		#creates an empty tensor with all elements set to zero with a shape
		W_conv1 = tf.Variable(tf.zeros([6, 6, 4, 32]))
		b_conv1 = tf.Variable(tf.constant(0.01, shape=[32]))

		W_conv2 = tf.Variable(tf.zeros([4, 4, 32, 64]))
		b_conv2 = tf.Variable(tf.constant(0.01, shape=[64]))

		W_conv3 = tf.Variable(tf.zeros([3, 3, 64, 64]))
		b_conv3 = tf.Variable(tf.constant(0.01, shape=[64]))

		W_fc4 = tf.Variable(tf.zeros([1024, 512]))
		b_fc4 = tf.Variable(tf.constant(0.01, shape=[512]))

		W_fc5 = tf.Variable(tf.zeros([512, ACTIONS]))
		b_fc5 = tf.Variable(tf.constant(0.01, shape=[ACTIONS]))

		#input for pixel data
		s = tf.placeholder("float", [None, 60, 60, 4])

		#Computes rectified linear unit activation function on a 2-D convolution given 4-D input and filter tensors.
		conv1 = tf.nn.relu(tf.nn.conv2d(s, W_conv1, strides = [1, 4, 4, 1], padding = "SAME") + b_conv1)
		pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
		conv2 = tf.nn.relu(tf.nn.conv2d(pool1, W_conv2, strides = [1, 2, 2, 1], padding = "SAME") + b_conv2)
		conv3 = tf.nn.relu(tf.nn.conv2d(conv2, W_conv3, strides = [1, 1, 1, 1], padding = "SAME") + b_conv3)

		conv3_flat = tf.reshape(conv3, [-1, 1024])

		fc4 = tf.nn.relu(tf.matmul(conv3_flat, W_fc4) + b_fc4)

		fc5 = tf.matmul(fc4, W_fc5) + b_fc5

		return s, fc5


#deep q network. feed in pixel data to graph session 
def trainGraph(inp, out):
	#to calculate the argmax, we multiply the predicted output with a vector with one value 1 and rest as 0
	argmax = tf.placeholder("float", [None, ACTIONS])
	gt = tf.placeholder("float", [None]) #ground truth
	global_step = tf.Variable(0, name='global_step')

	#action
	action = tf.reduce_sum(tf.multiply(out, argmax), reduction_indices = 1)
	#cost function we will reduce through back-propagation
	cost = tf.reduce_mean(tf.square(action - gt))
	#optimization function to reduce our minimize our cost function
	train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

	#initialize our game
	game = spaceinvaders.SpaceInvaders()

	#create a queue to store policies for experience replay
	D = deque()

	#initial frame
	frame = game.getPresentFrame()

	#convert rgb to grayscale for processing
	frame = cv2.cvtColor(cv2.resize(frame, (60, 60)), cv2.COLOR_BGR2GRAY)
	#binary colors, black or white
	ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
	#stack frames, that is our input tensor
	inp_t = np.stack((frame, frame, frame, frame), axis = 2)

	#saver
	saver = tf.train.Saver(tf.global_variables())
	# use a SessionManager to help with automatic variable restoration    
	sess = tf.InteractiveSession(config=tf.ConfigProto(log_device_placement=True))

	checkpoint = tf.train.latest_checkpoint('./checkpoints')
	if checkpoint != None:
		print('Restore Checkpoint %s'%(checkpoint))
		saver.restore(sess, checkpoint)
		print("Model restored.")
	else:
		init = tf.global_variables_initializer()
		sess.run(init)
		print("Initialized new Graph")

	t = global_step.eval()
	c= 0

	epsilon = INITIAL_EPSILON

	#training
	while(1):
		#output tensor
		out_t = out.eval(feed_dict = {inp : [inp_t]})[0]
		#argmax function
		argmax_t = np.zeros([ACTIONS])

		#
		if random.random() <= epsilon and not USE_MODEL:
			# make 0 the most chosen action for realistic randomness
			maxIndex = choice((0,1,2,3), 1, p=(0.60, 0.20, 0.10,0.10))
		else:
			maxIndex = np.argmax(out_t)
		argmax_t[maxIndex] = 1

		if epsilon > FINAL_EPSILON:
			epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

		mode = 'observing'
		if t > OBSERVE:
			mode = 'training'
		if USE_MODEL:
			mode = 'model only'

		#reward tensor if score is positive
		reward_t, frame = game.getNextFrame(argmax_t, [t, np.max(out_t), epsilon, mode])
		#get frame pixel data
		frame = cv2.cvtColor(cv2.resize(frame, (60, 60)), cv2.COLOR_BGR2GRAY)
		ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
		frame = np.reshape(frame, (60, 60, 1))
		#new input tensor
		inp_t1 = np.append(frame, inp_t[:, :, 0:3], axis = 2)

		#add our input tensor, argmax tensor, reward and updated input tensor tos tack of experiences
		D.append((inp_t, argmax_t, reward_t, inp_t1))

		#if we run out of replay memory, make room
		if len(D) > REPLAY_MEMORY:
			D.popleft()

		#training iteration
		if c > OBSERVE and not USE_MODEL:

			#get values from our replay memory
			minibatch = random.sample(D, BATCH)

			inp_batch = [d[0] for d in minibatch]
			argmax_batch = [d[1] for d in minibatch]
			reward_batch = [d[2] for d in minibatch]
			inp_t1_batch = [d[3] for d in minibatch]

			gt_batch = []
			out_batch = out.eval(feed_dict = {inp : inp_t1_batch})

			#add values to our batch
			for i in range(0, len(minibatch)):
				gt_batch.append(reward_batch[i] + GAMMA * np.max(out_batch[i]))

			#train on that 
			train_step.run(feed_dict = {
				gt : gt_batch,
				argmax : argmax_batch,
				inp : inp_batch
			})

		#update our input tensor the the next frame
		inp_t = inp_t1
		t = t + 1
		c = c + 1

		#print our where we are after saving where we are
		if t % SAVE_STEP == 0 and not USE_MODEL or game.gameOver:
			sess.run(global_step.assign(t))
			saver.save(sess, './checkpoints/model.ckpt', global_step=t)

		print("TIMESTEP", t, "/ SCORE", str(game.score), "/ EPSILON", epsilon, "/ ACTION", maxIndex, "/ REWARD", reward_t, "/ Q_MAX %e" % np.max(out_t))
