import pickle

def save(path, newtork_size, best_enemies):	
	result = [newtork_size] + best_enemies
	with open(path, "wb") as fp:   #Pickling
		pickle.dump(result, fp)

def load(path):
	with open(path, "rb") as fp:   # Unpickling
		result = pickle.load(fp)
	return result