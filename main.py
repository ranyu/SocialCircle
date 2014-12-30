import os
import collections
from read_test_set import read_test_set
from algorithm import walk_trap,infomap,fast_greedy,leading_eigenvector,label_propagation,multilevel,optimal_modularity,spinglass
from igraph import Graph,plot
import glob
import networkx as nx

def loadFeatures(featureMap,filename):
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
    		#print featureMap[currentPerson]
    		#quit()
    return featureMap
def input_graph_data(flag,filename):
	'''feature_list = []
	with open('featureList.txt','r') as f:
		for data in f:
			feature_list.append(data.strip())'''
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
	'''feature_list = []
	with open('featureList.txt','r') as f:
		for data in f:
			feature_list.append(data.strip())'''
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
def load_features_list(filename):
	features_list = []
	with open(filename,'r') as f:
		for data in f:
			features_list.append(data.strip().split()[1])
			#quit()
	print len(features_list)
	return features_list
def main():
	'''featureMap = collections.defaultdict(dict)
	for s in glob.glob('facebook/*.feat'):
		loadFeatures(featureMap,s)
	print featureMap['896']'''
	'''for s in glob.glob('facebook/*.featnames'):
		print load_features_list(s)
		quit()'''
	flag = False #False--facebook,True--twitter,gplus

	for t in glob.glob('facebook/*.edges'):		
		g = input_graph_data(flag,t)
		#community_walktrap
		print t
		#walk_trap(g,t)
		#layout = g.layout("kk")
		#plot(g, layout = layout)
		#quit()
		#community_infomap
		#infomap(g,t)
		fast_greedy(g,t)
		#dendogram = g.community_edge_betweenness(False) Wrong temp
		#print dendogram
		#leading_eigenvector(g,t)
		#label_propagation(g,t)
		#multilevel(g,t)
		#optimal_modularity(g,t)
		#spinglass(g,t)	Wrong temp
		#quit()
		
if __name__ == '__main__':
	main()
