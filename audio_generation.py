import librosa, librosa.display
import pyDOE
import numpy as np
import os
import glob

ingredients_path = os.path.abspath("./ISMIR16-EM-Patterns-Audio/dataset")
data_filepaths = glob.glob(ingredients_path + "/*.wav")
filepath_info = [os.path.splitext(os.path.basename(filepath))[0].split("_") for filepath in data_filepaths]
tempos, genres, instrs = zip(*filepath_info)
music_envs = [tempos[i]+"_"+genres[i] for i in range(len(tempos))]
audio_library = {music_env: [instrs[j] for j in range(len(instrs)) if music_env==music_envs[j]] for music_env in music_envs}

def generate_song_plan(nloops = 10, ntracks = 4, plantype="random", seed=0):
	"""
	This function drafts a layout for the song.
	Tracks 0--3 are: "bass", "drum", "fx", "melody".
	The layout for the example shown on https://www.audiolabs-erlangen.de/resources/MIR/2016-ISMIR-EMLoop is:
		Track 1 (bass):	X XX
		Track 2 (drum): XXX XX
		Track 3 (f.x.):        [empty]
		Track 4 (mel.):  XXXX 
	
	To make this, create a plan in an np.array as so:
	plan = np.array([[0, 0, 1, 0, 1, 1],
					 [1, 1, 1, 0, 1, 1]
					 [0, 0, 0, 0, 0, 0]
					 [0, 1, 1, 1, 1, 0]])
	
	The plan for the stimuli in Lopez-Serrano's paper is:
	plan = np.array([[0, 0, 1, 1, 0, 1, 0, 1],
					 [1, 1, 1, 1, 0, 1, 1, 1],
					 [0, 0, 0, 1, 0, 1, 1, 0],
					 [0, 1, 1, 1, 1, 1, 1, 0]])
	This is generated by generate_song_plan(plantype="lopez_serrano")
	
	The factorial plan is generated by generate_song_plan(plantype="factorial"):
	np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	          [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
	          [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
	          [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
	
	And the factorial_random plan is generate_song_plan(plantype="factorial_random",seed=0):
	np.array([[0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
			  [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
			  [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1],
			  [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1]])
	"""
	assert plantype in ["random", "lopez_serrano", "factorial", "factorial_random"]
	np.random.seed(seed)
	if plantype=="random":
		plan = np.random.randint(2,size=(ntracks,nloops))
		# If any columns all 0, convert to all 1:
		empty_cols = np.where(np.sum(plan,0)==0)
		for i in empty_cols[0]:
			plan[:,i] = 1
		# If any rows all 0, convert to all 1:
		empty_rows = np.where(np.sum(plan,1)==0)
		for i in empty_rows[0]:
			plan[i,:] = 1
	elif plantype=="lopez_serrano":
		plan = np.array([[0,0,1,1,0,1,0,1], [1,1,1,1,0,1,1,1], [0,0,0,1,0,1,1,0], [0,1,1,1,1,1,1,0]])
	elif plantype=="factorial":
		plan = pyDOE.fullfact([2]*ntracks).transpose()
		plan = plan.astype(int)
		plan = plan[:,1:]
	elif plantype=="factorial_random":
		# Use seed = 0 to get plan used in the paper!
		plan = pyDOE.fullfact([2]*ntracks).transpose()
		plan = plan.astype(int)
		plan = plan[:,1:]
		np.random.shuffle(plan.transpose())			
	return plan

def load_audio_clips(audio_type):
	audio_clips_X = []
	for clipname in audio_library[audio_type]:
		clip_audio, fs = librosa.core.load(ingredients_path + "/" + audio_type + "_" + clipname + ".wav", sr=22050, mono=True)
		audio_clips_X.append(clip_audio)
	return audio_clips_X, fs

# Create an audio file based on a layout and an audio type:
def implement_song_plan(plan, audio_clips, solo_index=None):
	if plan.shape[0]>len(audio_clips):
		print "Error! Fewer clip types exist than called for in the plan. We will loop over clip types."
	if solo_index is not None:
		one_hot = np.zeros((plan.shape[0],1)).astype(int)
		one_hot[solo_index] = 1
		new_plan = plan * one_hot
	else:
		new_plan = plan
	loop_length = np.max([len(clip) for clip in audio_clips])
	output_audio = np.zeros(new_plan.shape[1]*loop_length)
	downbeat_times = [i*loop_length for i in range(new_plan.shape[1]+1)]
	for i in range(new_plan.shape[0]):
		for j in range(new_plan.shape[1]):
			if new_plan[i,j]==1:
				output_audio[downbeat_times[j]:downbeat_times[j+1]] += audio_clips[i]
	return output_audio

def generate_tutti_datasets():
	for plantype in ["lopez_serrano", "factorial", "factorial_random"]:
		print "Making " + plantype + " set..."
		plan = generate_song_plan(15,4,plantype)
		target_path = os.path.abspath("./arranged_clips/" + plantype)
		if not os.path.exists(target_path):
			os.makedirs(target_path)
		for genre in audio_library.keys():
			clips, audio_fs = load_audio_clips(genre)
			audio_X = implement_song_plan(plan, clips)
			local_filename = target_path + "/" + genre + ".wav"
			librosa.output.write_wav(local_filename,y=audio_X,sr=audio_fs)

def generate_solo_datasets():
	for plantype in ["lopez_serrano", "factorial", "factorial_random"]:
		print "Making " + plantype + " set..."
		plan = generate_song_plan(15,4,plantype)
		target_path = os.path.abspath("./solo_clips/" + plantype)
		if not os.path.exists(target_path):
			os.makedirs(target_path)
		for genre in audio_library.keys():
			clips, audio_fs = load_audio_clips(genre)
			for i in range(plan.shape[0]):
				audio_X = implement_song_plan(plan, clips, solo_index=i)
				local_filename = target_path + "/" + genre + "_" + str(i) + ".wav"
				librosa.output.write_wav(local_filename,y=audio_X,sr=audio_fs)
