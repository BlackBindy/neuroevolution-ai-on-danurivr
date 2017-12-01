import pickle

def save(path, best_enemies):	
	with open(path, "wb") as fp:   #Pickling
		pickle.dump(best_enemies, fp)

def load(path):
	with open(path, "rb") as fp:   # Unpickling
		best_enemies = pickle.load(fp)
	return best_enemies