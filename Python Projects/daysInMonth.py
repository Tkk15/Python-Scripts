month = int (input ("Please enter the number of the month you want to know about"))
if (month ==2):
	print("There are 28 days in this month")
elif (month % 2 == 0):
	print ("There are 30 days in this month")
else:
	print ("There are 31 days in this month")

