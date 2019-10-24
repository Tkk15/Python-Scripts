print ("Please enter your age")
age = int (input ())
print ("Are you a US Citizen?")
citizen = bool (input ())

if (age > 12) and (age < 20):
	print ("You are a teen! You can throw tantrums.") 
else:
	print ("You are a child! You can also throw tantrums")

if (age <21) or (citizen == False):
	print ("Sorry no voting privileges")
else:
	print ("You are an adult and you get to vote!")
