from sklearn.metrics import jaccard_similarity_score,f1_score
from mean_f1 import mean_f1
import glob
import munkres

def load_file(filename,pre_dir):
	cir_true = []
	cir_true_ele = []
	cir_pred = []
	cir_pred_ele = []
	with open('facebook/'+filename) as f_true:
		for data in f_true:
			cir_true_ele = data.split()[1:]
			cir_true.append(cir_true_ele)
	with open(pre_dir+'/'+filename) as f_pred:
		for data in f_pred:
			cir_pred_ele = data.split(':')[1].split()
			cir_pred.append(cir_pred_ele)
	#with open(predir+'/'+file)
	return cir_true,cir_pred

def circle_evaluate(cir_true,cir_pred):
	Judge_list = []
	Judge_pred_list = []
	max_jaccard_list = []
	max_fscore_list = []
	max_jaccard = 0
	max_f1_score = 0
	for item in cir_true:
		for pre_item in cir_pred:
			Judge_list.append(item),Judge_pred_list.append(pre_item)
			jaccard,f_score = jaccard_fscore_caculate(Judge_list,Judge_pred_list)
			if max_jaccard < jaccard:
				max_jaccard = jaccard
				#print Judge_list,Judge_pred_list
			if max_f1_score < f_score:
				max_f1_score = f_score
				#print '???',Judge_list,Judge_pred_list
			Judge_list = []
			Judge_pred_list = []
		max_jaccard_list.append(max_jaccard)
		max_fscore_list.append(max_f1_score)
		max_jaccard = 0
		max_f1_score = 0
	return max_jaccard_list,max_fscore_list

def jaccard_fscore_caculate(cir_true,cir_pred):
	#cir_true = [[0,1,2,3]]
	#cir_pred = [[2,3,4,1,2,10]]
	jaccard = jaccard_similarity_score(cir_true,cir_pred,normalize=True)
	f_score = mean_f1(cir_true,cir_pred)
	#f1_score(cir_true,cir_pred,average='micro')
	return jaccard,f_score

def sort_circle(circle):
	circle.sort(key=lambda x:len(x),reverse=True)
	return circle

def top_k_circle(k,circle):
	circle.sort(key=lambda x:len(x),reverse=True)
	return circle[:k]

def evalution_func(element,element1,element2,element3,C_star,C):
	return (sum(element)+sum(element1))/(2*C_star),(sum(element2)+sum(element3))/(2*C)

def main():	
	result_ja = 0
	result_fs = 0
	pre_dir = ['nips','cesna']#['walkTrap','fastGreedy','multilevel','labelPropa',\
	#'leadingEigen','infoMap','edgeBetweenness','nips','cesna']
	for pre in pre_dir:
		temp = ['facebook/0.circles','facebook/698.circles']
		for filename in temp:#glob.glob('facebook/*.circles'):
			filename = filename.split('/')[1]
			cir_true,cir_pred = load_file(filename,pre)
			max_jaccard_list,max_fscore_list = circle_evaluate(cir_true,cir_pred)
			max_jaccard_reverse,max_fscore_reverse = circle_evaluate(cir_pred,cir_true)
			result_1,result_2 = evalution_func(max_jaccard_list,max_fscore_list,max_jaccard_reverse,max_fscore_reverse,len(cir_true),len(cir_pred))
			#print 'ja',result_1,'f1',result_2
			result_ja += result_1
			result_fs += result_2
			print pre,filename,'ja',result_1
			print pre,filename,'f1',result_2
		#print pre,'f1',result_fs / 10
		#print pre,'ja',result_ja / 10
		result_ja = 0
		result_fs = 0
if __name__ == '__main__':
	main()