import string


def parse_file(file_path,time_list):
	f = open(file_path,'r')
	for line in f.readlines():
		time = string.atof(line)
		if time not in time_list :
			time_list.append(time)


def parse_time_list(time_list):
	length = len(time_list)
	for i in range(length-1):
		if time_list[i+1] - time_list[i] >= 6:
			return i
	return length-1

def main():
	time_list = []	
	parse_file('/home/ramsey/delay-time',time_list)
	time_list.sort()
	index = parse_time_list(time_list)
	delay = time_list[index]-time_list[0]
	print delay

main()
