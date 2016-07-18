#i = 0
#numbers = []

#while i < 6:
#	print "At the top i is %d" % i
#	numbers.append(i)

#	i = i + 1
#	print "Numbers now: ", numbers
#	print "At the bottom i is %d" % i


#print "The numbers: "

#for num in numbers:
#	print num

from sys import argv

script, number_rise = argv

numbers = []
def number_count(x):
	"""This funtion will count the input number."""
	i = 0
	while i < x:
		print "At the top i is %d" % i
		numbers.append(i)

		i = i + int(number_rise)
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i

number_input = raw_input(">Number_input ?")
number_count(int(number_input))

print "The numbers: "

for num in numbers:
	print num