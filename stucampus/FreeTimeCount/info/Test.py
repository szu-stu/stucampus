file = open("students.txt", "r")
content = file.read()
file.close()

pieces = content.split("|")

i = 2
c = 5
while i < len(pieces):
	if len(pieces[i].strip()) != 0:
		c = c + 1
	if c == 6:
		c = 0
		print pieces[i]
	print "------" + pieces[i] + " len=" + str(len(pieces[i]))
	i = i + 1
