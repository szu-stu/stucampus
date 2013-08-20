# The following 3 function is just used to debug
def add_line_to_file(filename,string):
    with open(filename, 'a') as f:
        f.write((string+'\n').encode('utf-8'))


def write_dic_to_txt(dic):
    with open('test.txt', 'a') as f:
        for key, val in dic.iteritems():
            f.write((key+': '+val+'\n').encode('utf-8'))
        f.write('\n')


def clear_file(filename='test.txt'):
    with open(filename, 'w'):
        pass
