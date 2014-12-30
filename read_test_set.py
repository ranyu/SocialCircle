def read_test_set():
	test_set = {}
	with open('testSet_users_friends.csv','r') as f:
		for data in f:
			node = data.split(':')
			test_set.setdefault(node[0],node[1].strip().split('\r\n')[0])
	return test_set
def main():
	print read_test_set()
if __name__ == '__main__':
	main()