import os
import glob

def writeSubmission(f, circleMap, test=False):
    line = ''
    with open(circleMap,'r') as fil:
    	seed = circleMap.strip().split('/')[1].split('.')[0]
    	f.write(seed + ',')
    	data = fil.readline()
    	while data != '':
			if circleMap.strip().split('/')[0] == 'facebook':
				circle = data.strip().split()[1:]
			else:
				circle = data.strip().split(':')[1].split()
			for circles in circle:
				if circles != circle[-1] and circles != seed:
					line += circles +' '
			   	elif circles == circle[-1] and circles != seed:
			   		line += circles
			data = fil.readline()
			if len(line) != 0 and data != '':
				line += ';'
			f.write(line)
			line = ''
def write_main():
	Dir_list = ['facebook','walkTrap','infoMap','fastGreedy',\
	'leadingEigen','labelPropa','multilevel','cesna','edgeBetweenness','nips']
	for j in Dir_list:
		f = open(j+'/clusters_data.txt', 'w')
		f.write('UserId,Predicted\n')
		for i in glob.glob(j+'/*.circles'):
			print i
			writeSubmission(f,i)
			f.write('\n')
		f.close()
if __name__ == '__main__':
	write_main()