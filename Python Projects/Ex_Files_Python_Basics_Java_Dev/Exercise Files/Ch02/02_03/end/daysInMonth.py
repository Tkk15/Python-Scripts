month = int (input ("Please enter the number of the month you want to know about" ))
OddOrEven = month % 2
if (month ==2):
	print ("there are 28 days in the month")
elif (OddOrEven ==0):
	print ("there are 30 days in the month")
else:
	print ("there are 31 days in the month")