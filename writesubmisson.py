import os
import glob
from read_test_set import read_test_set

def writeSubmission(f, circleMap, test=False):
    line = ''
    test_set = read_test_set()
    with open(circleMap,'r') as fil:
    	seed = circleMap.strip().split('/')[1].split('.')[0]
    	f.write(seed + ',')
    	data = fil.readline()
    	while data != '':
			circle = data.strip().split(':')[1].split()
			for circles in circle:
				if True:#circles in test_set[seed]:
					if circles != circle[-1] and circles != seed:
						line += circles +' '
				   	elif circles == circle[-1] and circles != seed:
				   		line += circles
			data = fil.readline()
			if len(line) != 0 and data != '':
				line += ';'
			f.write(line)
			line = ''
def main():
	Dir_list = ['walkTrap','infoMap','fastGreedy','leadingEigen','labelPropa','multilevel','optimalModularity','spinGlass']

	for j in Dir_list:
		f = open(j+'/clusters_data.csv', 'w+')
		f.write('UserId,Predicted\n')
		for i in glob.glob(j+'/*.circles'):
			print i
			writeSubmission(f,i)
			f.write('\n')
		f.close()
if __name__ == '__main__':
	main()