import os
import collections
from algorithm import walk_trap,infomap,fast_greedy,leading_eigenvector,\
label_propagation,multilevel,optimal_modularity,spinglass,edge_betweenness,\
extract_clusters
from igraph import Graph,plot
import glob
from igraph import arpack_options
from writesubmisson import write_main
from socialCircles_metric import social_evaluate
arpack_options.maxiter=300000


def loadFeatures(featureMap,filename):
    with open(filename,'r') as f:    	
    	for data in f:
    		parts = data.strip().split()
    		currentPerson = parts[0]
    		for part in xrange(1,len(parts[1:])):
	    		value = parts[part]
	    		featureMap[currentPerson][part-1] = value
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
		#print s
		loadFeatures(featureMap,s)

	flag = False #False--facebook,True--twitter,gplus

	for t in glob.glob('facebook/0.edges'):
		g = input_graph_data_fet(flag,featureMap,t)
		print t
		walk_trap(g,t)
		infomap(g,t)
		fast_greedy(g,t)
		leading_eigenvector(g,t)
		label_propagation(g,t)
		multilevel(g,t) # Louvain another name
		#A little slow,use it cautionly
		edge_betweenness(g,t,flag)# Girvan Newman another name
		#Too slow,use it cautionly
		optimal_modularity(g,t) 
	write_main()
	for file_name in glob.glob('*/clusters_data.txt'):
		print file_name.split('/')[0]+':\n'
		social_evaluate(file_name,'facebook/clusters_data.txt')
if __name__ == '__main__':
	main()
