from sys import argv

script, first, second, third = argv

print "The script is called:", script
print "Your first variable is:", first
print "Your second variable is:", second
print "Your third variable is:", third

time = raw_input("What time is now?a.m./p.m.")
today = raw_input("What day is today?")

print "So, today is %s, and now is %s." % (today, time)