import os
import collections
from algorithm import walk_trap,infomap,fast_greedy,leading_eigenvector,\
label_propagation,multilevel,optimal_modularity,spinglass,edge_betweenness,\
extract_clusters,intersect_circles,write_file_alone
from igraph import Graph,plot
import glob
from igraph import arpack_options
from writesubmisson import write_main
from socialCircles_metric import social_evaluate
arpack_options.maxiter=300000
from sklearn.metrics import jaccard_similarity_score,f1_score

def loadFeatures_Train(filename,trainlist):
    featureMap = collections.defaultdict(dict)
    for line in open(filename):
        parts = line.strip().split()
        #print parts
        currentPerson = parts[0]
     	#quit()
        for part in parts[1:]:
            key = part[0:part.rfind(';')]
            value = part[part.rfind(';')+1:]
            featureMap[currentPerson][key] = value
        #print featureMap[currentPerson]
        for s in trainlist:
        	if s not in featureMap[currentPerson].keys():        	
        		featureMap[currentPerson][s] = '-1'
        #print featureMap[currentPerson]
        #quit()
    #print featureMap['27519']
    #quit()
    return featureMap

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
		#print node,filename
		#quit()
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
			features_list.append(data.strip().split()[0])
	#print len(features_list)
	return features_list

def input_Train_data(featureMap,filename,flag = False):
	g = Graph(directed = flag)
	with open(filename,'r') as f:
		for data in f:
			node = data.strip().split(':')[0]
			g.add_vertex(node)
			#g.vs['id'] = featureMap[node]['id']
 			#print g.vs['name']
			#quit()
			#print type(node),filename
			#quit()
			for key in featureMap[node].keys():
				#print key,featureMap[node][key]
				g.vs[key] = featureMap[node][key]
			#print g.vs['name']
			for other_node in data.split(':')[1].split():
				if other_node not in g.vs['name']:
					#print other_node,filename
					g.add_vertex(other_node)
					#print other_node
					for key in featureMap[other_node].keys():
						g.vs[key].append(featureMap[other_node][key])
					#print g.vs['name']			
				g.add_edge(node,other_node)
				#quit()
	return g.simplify()

def main():
	#quit()
	#featureMap = collections.defaultdict(dict)
	f_list = load_features_list('features_list.txt')
	#print f_list
	#quit()
	featureMap = loadFeatures_Train('new_features.txt',f_list)
	'''for s in glob.glob('facebook/*.feat'):
		#print s
		loadFeatures(featureMap,s)'''
	flag = False #False--facebook,True--twitter,gplus
	train_list = []
	train_file = open('train_test.txt','r')
	for data in train_file:
		train_list.append(data.strip().split()[0])
	#print len(train_list)
	for t in train_list:#glob.glob('twitter/*.edges'):
		f_name =  'egonets/'+t+'.egonet'
		#e
		#g = input_graph_data_fet(flag,featureMap,t)
		#g = input_graph_data(flag,t)
		g = input_Train_data(featureMap,f_name,False)
		#print g
		#quit()
		print f_name
		cl_walk = walk_trap(g,t)
		cl_info = infomap(g,t)
		inter_circle =  intersect_circles(cl_walk,cl_info)

		write_file_alone('inter_walk_info',t,list(inter_circle))
		#quit()
		#fast_greedy(g,t)
		#leading_eigenvector(g,t)
		#label_propagation(g,t)
		#mcl(g,t)
		#multilevel(g,t) # Louvain another name
		#A little slow,use it cautionly
		#print g.clusters().giant()		
		#edge_betweenness(g,t,flag)# Girvan Newman another name
		#quit()
		#Too slow,use it cautionly
		#optimal_modularity(g,t) '''
	write_main()
	for file_name in glob.glob('*/clusters_ff.txt'):
		print file_name.split('/')[0]+':\n'
		#if file_name!='walkTrap_tr/clusters_clusters_train.txt':
		social_evaluate(file_name,'groundtruth.txt')#'twitter/cluster_tw.txt')
	#delete_circle()
	#social_evaluate('inter_walk_info/clusters_clusters_train.txt','groundtruth.txt')
	#train_file.close()
if __name__ == '__main__':
	main()
