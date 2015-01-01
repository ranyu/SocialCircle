import os
import collections
from algorithm import walk_trap,infomap,fast_greedy,leading_eigenvector,\
label_propagation,multilevel,optimal_modularity,spinglass,edge_betweenness
from igraph import Graph,plot
import glob
from igraph import arpack_options

arpack_options.maxiter=300000

def loadFeatures(featureMap,filename):
    #filename = 'facebook/0.feat'
    with open(filename,'r') as f:    	
    	for data in f:
    		parts = data.strip().split()
    		#print len(parts[1:])
    		#print parts[1:]
    		currentPerson = parts[0]
    		for part in xrange(1,len(parts[1:])):
	    		value = parts[part]
	    		featureMap[currentPerson][part-1] = value
	    		#print key,value,featureMap[currentPerson]
    		#print currentPerson#,featureMap[currentPerson]
    		#quit()
    return featureMap

def input_graph_data(flag,filename):
	g = Graph(directed = flag)
	with open(filename,'r') as f:
		data = f.readline()
		node = data.strip().split()[0]
		g.add_vertex(node)
		other_node =  data.strip().split()[1]
		if other_node not in g.vs['name']:
			g.add_vertex(other_node)
		g.add_edge(node,other_node)
		for data in f:		
			node = data.strip().split()[0]
			if node not in g.vs['name']:
				g.add_vertex(node)
			other_node =  data.strip().split()[1]
			if other_node not in g.vs['name']:
				g.add_vertex(other_node)
			g.add_edge(node,other_node)
	return g.simplify()

def input_graph_data_fet(flag,featureMap,filename):
	g = Graph(directed = flag)
	with open(filename,'r') as f:
		data = f.readline()
		node = data.strip().split()[0]
		g.add_vertex(node)
		for attribute in xrange(len(featureMap[node])):
			g.vs['attr'+str(attribute)] = featureMap[node][attribute]
		other_node =  data.strip().split()[1]
		if other_node not in g.vs['name']:
			g.add_vertex(other_node)
			for attribute in xrange(len(featureMap[other_node])):
				g.vs['attr'+str(attribute)] = featureMap[other_node][attribute]
		g.add_edge(node,other_node)
		for data in f:		
			node = data.strip().split()[0]
			if node not in g.vs['name']:
				#print featureMap[node],len(featureMap[node])
				g.add_vertex(node)
				#quit()
				for attribute in xrange(len(featureMap[node])):
					#print featureMap[node]
					#quit()
					g.vs['attr'+str(attribute)] = featureMap[node][attribute]
					#print featureMap[node][attribute]
			other_node =  data.strip().split()[1]
			if other_node not in g.vs['name']:
				g.add_vertex(other_node)
				for attribute in xrange(len(featureMap[other_node])):
					g.vs['attr'+str(attribute)] = featureMap[other_node][attribute]
			g.add_edge(node,other_node)
	return g.simplify()

def load_features_list(filename):
	features_list = []
	with open(filename,'r') as f:
		for data in f:
			features_list.append(data.strip().split()[1])
	#print len(features_list)
	return features_list

def main():
	featureMap = collections.defaultdict(dict)
	for s in glob.glob('facebook/*.feat'):
		print s
		loadFeatures(featureMap,s)
	#print featureMap['2661']
	#quit()
	'''for s in glob.glob('facebook/*.featnames'):
		print s,load_features_list(s)
		quit()
	quit()'''

	flag = False #False--facebook,True--twitter,gplus

	for t in glob.glob('facebook/*.edges'):
		if t != 'facebook/1912.edges':
			g = input_graph_data_fet(flag,featureMap,t)
			#print t
			#print g.vs['name'],list(g.vs)
			#quit()
			#for i in xrange(10):
				#print 'attr'+str(i)#len(g.vs['attr'+str(i)])
			#quit()
			print t		
			#layout = g.layout("kk")
			#plot(g, layout = layout)
			#infomap(g,t)
			#quit()
			edge_betweenness(g,t,flag)
			#walk_trap(g,t)
			#fast_greedy(g,t)
			#leading_eigenvector(g,t)
			#label_propagation(g,t)
			#multilevel(g,t)
			#optimal_modularity(g,t)
			#spinglass(g,t)	#Wrong temp
		
if __name__ == '__main__':
	main()
