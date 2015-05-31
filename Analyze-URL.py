import string

class UrlRef(object):
	def __init__(self,url):
		self.url = url
		self.refcount = 1
	def increase_count(self):
		self.refcount = self.refcount +1

class StartUrlList(object):

	def __init__(self):
		self.url_list = []

	def append(self,url):
		found = False
		for i in range(len(self.url_list)):
			if self.url_list[i].url == url:
				self.url_list[i].increase_count()
				found = True
				break
		if found == False:
			self.url_list.append(UrlRef(url))	

	def getMaxRefUrl(self):
		maxRef = self.url_list[0].refcount
		maxIndex = 0
		for i in range(1,len(self.url_list)):
				if self.url_list[i].refcount > maxRef:
					maxRef = self.url_list[i].refcount
					maxIndex = i
		return self.url_list[maxIndex].url					

def parse_logfile(filepath,url_list,similar_data):
	f = open(filepath,'r')
	for line in f.readlines() :
		if line.startswith('request'):
			attr = line.split(':')
			url_list.append(attr[4])
		elif line.startswith('similar'):
			attr = line.split(':')
			similar = string.atof(attr[1])
			similar_data.append(similar)

def find_start_url(url_list,similar_data,threshold):
	length = len(similar_data)
	if threshold > length :
		threshold = length
	minVaule = similar_data[0]
	minIndex = 0
	for i in range(1,threshold):
		if similar_data[i] < minVaule :
			minVaule = similar_data[i]
			minIndex = i
	return url_list[minIndex]

def find_repeat_urls(src_list_a,src_list_b,dst_list):
	length_b = len(src_list_b)
	for i in range(0,length_b):
		if src_list_b[i] in src_list_a :
			dst_list.append(src_list_b[i])

def find_end_url(url_list):
	while(1):
		end_url = url_list.pop()
		if end_url not in url_list:
			break
	return end_url

	

if __name__ == '__main__':
	start_url_list = StartUrlList()


	url_list_a = []
	similar_data_a = []
	parse_logfile('/home/alex/Downloads/CNN-Driver-master/mitmproxy-results/0/http-log',url_list_a,similar_data_a)
	start_url = find_start_url(url_list_a,similar_data_a,20)
	start_url_list.append(start_url)	
	print start_url

	dst_list=[]

	for i in range(1,5):
		url_list_b = []
		similar_data_b = []
		log_file_path = '/home/alex/Downloads/CNN-Driver-master/mitmproxy-results/%d/http-log' % i
		parse_logfile(log_file_path,url_list_b,similar_data_b)
		start_url = find_start_url(url_list_b,similar_data_b,20)
		start_url_list.append(start_url)	
		print start_url
		find_repeat_urls(url_list_a,url_list_b,dst_list)
		url_list_a = dst_list
		dst_list = []		
		
	
	print start_url_list.getMaxRefUrl()
	print url_list_a
	print find_end_url(url_list_a)

