#algorithm.py
from itertools import izip
from sklearn.metrics import jaccard_similarity_score,f1_score,consensus_score

def delete_circle():
	pass
def write_file(flag,node,cl):
	'''Dir_list = ['walkTrap_twitter','infoMap_twitter','fastGreedy_twitter','leadingEigen_twitter','labelPropa_twitter',\
	'multilevel_twitter','optimalModularity_twitter','spinGlass_twitter','edgeBetweenness_twitter']
	'''
	Dir_list = ['walkTrap_tr','infoMap_tr','fastGreedy_tr','leadingEigen_tr','labelPropa_tr',\
	'multilevel_tr','optimalModularity_tr','spinGlass_tr','edgeBetweenness_tr']
	
	with open(Dir_list[flag]+'/'+node+'.circles','w') as f:
		for i in cl:
			f.write('circle:')
			for j in i:
				f.write(str(j)+' ')
			f.write('\n')
def write_file_alone(filename,node,cl):	
	with open(filename+'/'+node+'.circles','w') as f:
		for i in cl:
			f.write('circle:')
			for j in i:
				f.write(str(j)+' ')
			f.write('\n')
def extract_clusters(clusters, reverseIdMap):
    new_clusters = []
    for i in range(len(clusters)):
        next_cluster = [reverseIdMap[j] for j in clusters[i]]
        new_clusters.append(next_cluster)
    return new_clusters
def fix_dendrogram(graph, cl):
    already_merged = set()
    for merge in cl.merges:
        already_merged.update(merge)

    num_dendrogram_nodes = graph.vcount() + len(cl.merges)
    not_merged_yet = sorted(set(xrange(num_dendrogram_nodes)) - already_merged)
    if len(not_merged_yet) < 2:
        return

    v1, v2 = not_merged_yet[:2]
    cl._merges.append((v1, v2))
    del not_merged_yet[:2]

    missing_nodes = xrange(num_dendrogram_nodes,
            num_dendrogram_nodes + len(not_merged_yet))
    cl._merges.extend(izip(not_merged_yet, missing_nodes))
    cl._nmerges = graph.vcount()-1

def real_data(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1	
	#print g
	#quit()
	dendogram = g.community_walktrap(steps=4)
	#print '~~~',dendogram.graph()
	#quit()
	cl = dendogram.as_clustering()
	#print cl._formatted_cluster_iterator
	quit()
	walktrapmap_clusters = extract_clusters(cl, reverseIdMap)
	filename =  t.split('/')[1].split('.')[0]
	return cl

def walk_trap(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	vertex_weights_list = []
	dendogram = g.community_walktrap(steps=4)		
	with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))
	cl = dendogram.as_clustering()
	new_clusters = []
	for cluster in cl:
		if len(cluster) > 7:
			new_clusters.append(cluster)
	#print new_clusters
	#quit()
	walktrapmap_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print walktrapmap_clusters
	write_file(0,t,walktrapmap_clusters)
	return walktrapmap_clusters
	#quit()

def infomap(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	vertex_weights_list = []	
	with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))
	dendogram = g.community_infomap(trials=10)#,vertex_weights=vertex_weights_list)
	new_clusters = []
	for cluster in list(dendogram):
		if len(cluster) > 7:
			new_clusters.append(cluster)	
	if len(new_clusters) == 0:
		new_clusters.append(list(dendogram)[0])
	infomap_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print infomap_clusters
	write_file(1,t,list(infomap_clusters))
	return infomap_clusters
	#quit()

def fast_greedy(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	vertex_weights_list = []	
	'''with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))'''
	dendogram = g.community_fastgreedy()
	cl = dendogram.as_clustering()
	new_clusters = []
	for cluster in cl:
		if len(cluster) > 3:
			new_clusters.append(cluster)
	fastgreedy_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print fastgreedy_clusters
	write_file(2,t,list(fastgreedy_clusters))
	return cl
	
	#quit()

def leading_eigenvector(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	'''vertex_weights_list = []	
	with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))'''	
	dendogram = g.community_leading_eigenvector()
	new_clusters = []
	for cluster in list(dendogram):
		if len(cluster) > 3:
			new_clusters.append(cluster)	
	if len(new_clusters) == 0:
		new_clusters.append(list(dendogram)[0])
	leading_eigenvector_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print leading_eigenvector_clusters
	write_file(3,t,list(leading_eigenvector_clusters))
	#quit()
def label_propagation(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	'''vertex_weights_list = []	
	with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))'''	
	dendogram = g.community_label_propagation()
	new_clusters = []
	for cluster in list(dendogram):
		if len(cluster) > 3:
			new_clusters.append(cluster)	
	if len(new_clusters) == 0:
		new_clusters.append(list(dendogram)[0])
	label_propagation_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print label_propagation_clusters
	write_file(4,t,list(label_propagation_clusters))

def multilevel(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1
	vertex_weights_list = []	
	'''with open('feature_weights.txt','r') as f:
		for data in f:
			vertex_weights_list.append(int(data.strip().split('--')[1]))'''
	dendogram = g.community_multilevel()
	new_clusters = []
	for cluster in list(dendogram):
		if len(cluster) > 3:
			new_clusters.append(cluster)	
	if len(new_clusters) == 0:
		new_clusters.append(list(dendogram)[0])
	multilevel_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print multilevel_clusters
	write_file(5,t,list(multilevel_clusters))
	return dendogram

def optimal_modularity(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1	
	dendogram = g.community_optimal_modularity()
	optimal_modularity_clusters = extract_clusters(dendogram, reverseIdMap)
	#write_file(6,t,list(optimal_modularity_clusters))

def spinglass(g,t):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1	
	dendogram = g.community_spinglass()
	#print dendogram
	#quit()
	spinglass_clusters = extract_clusters(dendogram, reverseIdMap)
	#print multilevel_clusters
	write_file(7,t,list(spinglass_clusters))

def edge_betweenness(g,t,flag):
	reverseIdMap = {}
	idMap = {}
	currentId = 0
	for friend in g.vs['name']:
		idMap[friend] = currentId
		reverseIdMap[currentId] = friend
		currentId += 1	
	dendogram = g.community_edge_betweenness(directed=flag)
	fix_dendrogram(g,dendogram)
	cl = dendogram.as_clustering()
	new_clusters = []
	for cluster in cl:
		if len(cluster) > 3:
			new_clusters.append(cluster)
	edge_betweenness_clusters = extract_clusters(new_clusters, reverseIdMap)
	#print edge_betweenness_clusters
	write_file(8,t,list(edge_betweenness_clusters))

def intersect_circles(cl1,cl2):
	matrix = []
	matrix_ele = []
	jar_max = 0
	max_tuple = (0,0)
	inter_circle = []
	for i in cl1:
		for j in cl2:
			jaccard = f1_score([i],[j],average='micro')#jaccard_similarity_score#
			if jar_max < jaccard:
				jar_max = jaccard
				max_tuple = (i,j)
		c3 = set(i) | set(j)
		inter_circle.append(list(c3))
	return cl2