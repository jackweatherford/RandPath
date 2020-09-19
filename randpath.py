import numpy as np

from sys import maxsize
from random import seed, randrange, choice
from imageio import imwrite


def getSeed():
	
	# Get a seed to initialize randomness, allows for image reproduction
	seed_val = str(input('Enter a seed (Enter nothing for a random seed): '))
	if seed_val == '':
		seed_val = randrange(maxsize)
	seed(seed_val)
	
	return seed_val

def oneFails(grid, head, prev_dir):
	# If direction one leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]-1] == 0 or \
		grid[head[1]-1, head[0]] == 0 or \
		grid[head[1]-1, head[0]+1] == 0 or \
		(grid[head[1]+1, head[0]+1] == 0 and (prev_dir == 4 or prev_dir == 6)) or \
		grid[head[1]+1, head[0]-1] == 0 or \
		grid[head[1], head[0]-1] == 0

def twoFails(grid, head, prev_dir):
	# If direction two leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]-1] == 0 or \
		grid[head[1]-1, head[0]] == 0 or \
		grid[head[1]-1, head[0]+1] == 0 or \
		grid[head[1], head[0]+1] == 0 or \
		(grid[head[1]+1, head[0]] == 0 and (prev_dir == 5 or prev_dir == 7)) or \
		grid[head[1], head[0]-1] == 0

def threeFails(grid, head, prev_dir):
	# If direction three leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]-1] == 0 or \
		grid[head[1]-1, head[0]] == 0 or \
		grid[head[1]-1, head[0]+1] == 0 or \
		grid[head[1], head[0]+1] == 0 or \
		grid[head[1]+1, head[0]+1] == 0 or \
		(grid[head[1]+1, head[0]-1] == 0 and (prev_dir == 6 or prev_dir == 8))

def fourFails(grid, head, prev_dir):
	# If direction four leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]] == 0 or \
		grid[head[1]-1, head[0]+1] == 0 or \
		grid[head[1], head[0]+1] == 0 or \
		grid[head[1]+1, head[0]+1] == 0 or \
		grid[head[1]+1, head[0]] == 0 or \
		(grid[head[1], head[0]-1] == 0 and (prev_dir == 1 or prev_dir == 7))

def fiveFails(grid, head, prev_dir):
	# If direction five leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		(grid[head[1]-1, head[0]-1] == 0 and (prev_dir == 2 or prev_dir == 8)) or \
		grid[head[1]-1, head[0]+1] == 0 or \
		grid[head[1], head[0]+1] == 0 or \
		grid[head[1]+1, head[0]+1] == 0 or \
		grid[head[1]+1, head[0]] == 0 or \
		grid[head[1]+1, head[0]-1] == 0

def sixFails(grid, head, prev_dir):
	# If direction six leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		(grid[head[1]-1, head[0]] == 0 and (prev_dir == 1 or prev_dir == 3)) or \
		grid[head[1], head[0]+1] == 0 or \
		grid[head[1]+1, head[0]+1] == 0 or \
		grid[head[1]+1, head[0]] == 0 or \
		grid[head[1]+1, head[0]-1] == 0 or \
		grid[head[1], head[0]-1] == 0

def sevenFails(grid, head, prev_dir):
	# If direction seven leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]-1] == 0 or \
		(grid[head[1]-1, head[0]+1] == 0 and (prev_dir == 2 or prev_dir == 4)) or \
		grid[head[1]+1, head[0]+1] == 0 or \
		grid[head[1]+1, head[0]] == 0 or \
		grid[head[1]+1, head[0]-1] == 0 or \
		grid[head[1], head[0]-1] == 0

def eightFails(grid, head, prev_dir):
	# If direction eight leads to an intersection
	return grid[head[1], head[0]] == 0 or \
		grid[head[1]-1, head[0]-1] == 0 or \
		grid[head[1]-1, head[0]] == 0 or \
		(grid[head[1], head[0]+1] == 0 and (prev_dir == 3 or prev_dir == 5)) or \
		grid[head[1]+1, head[0]] == 0 or \
		grid[head[1]+1, head[0]-1] == 0 or \
		grid[head[1], head[0]-1] == 0

def generateGrid(w, h, path_length):
	
	# Initialize to fully white image
	grid = np.ones((h, w))
	
	# Initialize head to center
	head = [h//2, w//2]
	# Draw first black point at center
	grid[head[1], head[0]] = 0

	# Keeps track of number of black pixels in the image
	points = 0
	# Keeps track of previous head
	prev_head = head.copy()
	# Possible choices when chosing which direction to go next, 1-8 clockwise starting from top left
	dirs = [_ for _ in range(1,9)]
	# Keeps track of complete path
	path = [head.copy()]
	# Keeps track of previous dir
	prev_dir = 0
	# Keeps track of all previous dirs
	prev_dirs = [0]
	# Keeps track of which heads will lead to failure
	failed = []
	
	max_points = 0
	max_grid = []
	max_failed = []

	# Main loop
	while points < path_length:
		# If all directions fail
		if len(dirs) == 0:
			if points > max_points:
				max_points = points
				max_grid = grid.copy()
				max_failed = failed.copy()
			
			grid[head[1], head[0]] = 1
			# TODO: - remove failed paths adjacent to head.
			# - if in a chain of fails, remove previous fail from fails.
			prev_dirs.pop()
			try:
				prev_dir = prev_dirs[-1]
			except IndexError:
				return max_grid, max_failed
			failed.append(path.pop())
			dirs = [_ for _ in range(1,9)]
			head = path[-1].copy()
			prev_head = head.copy()
			points -= 1
		
		# Choose a random direction
		dir = choice(dirs)
		if dir == 1: # Top-Left
			head[0] -= 1
			head[1] -= 1
			if oneFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(1)
				continue
		elif dir == 2: # Top-Middle
			head[1] -= 1
			if twoFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(2)
				continue
		elif dir == 3: # Top-Right
			head[0] += 1
			head[1] -= 1
			if threeFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(3)
				continue
		elif dir == 4: # Right-Middle
			head[0] += 1
			if fourFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(4)
				continue
		elif dir == 5: # Bottom-Right
			head[0] += 1
			head[1] += 1
			if fiveFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(5)
				continue
		elif dir == 6: # Bottom-Middle
			head[1] += 1
			if sixFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(6)
				continue
		elif dir == 7: # Bottom-Left
			head[0] -= 1
			head[1] += 1
			if sevenFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(7)
				continue
		else: # Left-Middle
			head[0] -= 1
			if eightFails(grid, head, prev_dir):
				head = prev_head.copy()
				dirs.remove(8)
				continue
		
		# If head goes out of bounds
		if head[1]+1 >= h-1 or head[1]-1 <= 0 or head[0]+1 >= w-1 or head[0]-1 <= 0:
			head = prev_head.copy()
			dirs.remove(dir)
			continue
		
		# If head will lead to failure
		if head in failed:
			head = prev_head.copy()
			dirs.remove(dir)
			continue
		
		# If the code gets to here, its a valid head
		grid[head[1], head[0]] = 0
		points += 1
		prev_head = head.copy()
		if len(dirs) < 8:
			dirs = [_ for _ in range(1,9)]
		path.append(head.copy())
		prev_dirs.append(dir)
		prev_dir = dir
	
	return grid

def saveToFile(filename, grid):
	
	# Write to file from numpy array (grid)
	imwrite(filename, grid)
	
	print('Image saved as', filename)

if __name__ == '__main__':
	
	seed_val = getSeed()
	
	# w: Width, h: Height of image
	w, h = 101, 101
	# How many black pixels to use in the path
	path_length = 2000
	
	filename = input('Enter a filename: ') + '.png'
	
	print('Generating image...')
	
	grid, failed = generateGrid(w, h, path_length)

	new_grid = np.zeros((h, w, 3), dtype=np.uint8)
	
	for i in range(w):
		for j in range(h):
			p = grid[j][i]
			if p == 0:
				new_p = [0, 0, 0]
			elif p == 1:
				if [i, j] in failed:
					new_p = [255, 0, 0]
				else:
					new_p = [255, 255, 255]
			new_grid[j][i] = new_p

	# grid = grid * 255
	# grid = grid.astype(np.uint8)

	print('Image generated!')
	
	saveToFile(filename, new_grid)
