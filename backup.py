import os
import collections
from read_test_set import read_test_set
from algorithm import walk_trap,infomap,fast_greedy,leading_eigenvector,label_propagation,multilevel,optimal_modularity,spinglass
from igraph import Graph

def get_filename(rootDir): 
    document_dir = []
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        document_dir.append(lists)
        if os.path.isdir(path): 
            get_filename(path)
    return document_dir
def loadFeatures(filename):
    featureMap = collections.defaultdict(dict)
    for line in open(filename):
        parts = line.strip().split()
        currentPerson = parts[0]
        for part in parts[1:]:
            key = part[0:part.rfind(';')]
            value = part[part.rfind(';')+1:]
            featureMap[currentPerson][key] = value
    #print featureMap['27519']
    return featureMap
def input_graph_data(featureMap,filename):
	feature_list = []
	with open('featureList.txt','r') as f:
		for data in f:
			feature_list.append(data.strip())
	g = Graph(directed = False)
	with open('egonets/'+filename,'r') as f:
		for data in f:
			node = data.strip().split(':')[0]
			if node not in g.vs:
				g.add_vertex(node,birthday = featureMap[node].get('birthday',0),education_classes_description = featureMap[node].get(feature_list[1],0)\
				,education_classes_from_id = featureMap[node].get(feature_list[2],0),education_classes_from_name = featureMap[node].get(feature_list[3],0))
				for i in xrange(1,len(data.strip().split())):
					other_node =  data.strip().split()[i]
					if other_node not in g.vs:
						g.add_vertex(other_node, birthday = featureMap[other_node].get('birthday',0),education_classes_description = featureMap[other_node].get(feature_list[1],0)\
				,education_classes_from_id = featureMap[other_node].get(feature_list[2],0),education_classes_from_name = featureMap[other_node].get(feature_list[3],0))
						g.add_edge(node,other_node)
		return g.simplify()


def main():
	test_number_list = []
	with open('test_file_number.txt','r') as f:
		for data in f:
			test_number_list.append(data.split('\n')[0])
	featureMap = loadFeatures('features.txt')
	#document_dir = get_filename('egonets')
	for t in test_number_list:		
		d = t +'.egonet'
		print d
		g = input_graph_data(featureMap,'10395.egonet')		
		#community_walktrap
		walk_trap(g,t)
		quit()
		#community_infomap
		#infomap(g,t)
		#fast_greedy(g,t)
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
