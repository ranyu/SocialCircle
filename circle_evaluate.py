from sklearn.metrics import jaccard_similarity_score,f1_score

def load_file():
	cir_true = []
	cir_true_ele = []
	cir_pred = []
	cir_pred_ele = []
	with open('facebook/1684.circles') as f_true:
		for data in f_true:
			cir_true_ele = data.split()[1:]
			cir_true.append(cir_true_ele)
	with open('fastGreedy/1684.circles') as f_pred:
		for data in f_pred:
			cir_pred_ele = data.split(':')[1].split()
			cir_pred.append(cir_pred_ele)
	return cir_true,cir_pred

def circle_evaluate(cir_true,cir_pred):
	print 'Jarrcard',jaccard_similarity_score(cir_true,cir_pred,normalize=True)
	print 'f1_score',f1_score(cir_true,cir_pred,average='micro')
def top_k_circle(k,circle):
	record_num = {}
	circle.sort(key=lambda x:len(x),reverse=True)
	return circle[:k]
def add_equal(cir_true,cir_pred):
	s1 = len(cir_true)
	s2 = len(cir_pred)
	result = s1 - s2
	if result == 0:
		return 
	elif result > 0:
		for i in xrange(result):
			cir_pred.append([])
	else:
		for i in xrange(0-result):
			cir_true.append([])
	print len(cir_true),len(cir_pred)
	return cir_true,cir_pred
def main():
	cir_true,cir_pred = load_file()
	print cir_true,'\n------------\n',cir_pred
	#print len(cir_true),len(cir_pred)
	cir_true,cir_pred = add_equal(cir_true,cir_pred)
	print len(cir_true),len(cir_pred)
	#cir_pred = top_k_circle(len(cir_true),cir_pred)
	circle_evaluate(cir_true,cir_pred)
if __name__ == '__main__':
	main()