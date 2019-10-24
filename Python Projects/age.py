print ("Please enter age you piece of shit")
age = int(input())
citizen = bool (input())

if (age>12) and (age<20):
	print("You are a teen! you can throw tantrums.")
else:
	print("You are a child! You can also")

if (age<21) or (citizen==False):
	print("Sorry no voting privileges")
else:
	print("You are an adult and you get to vote!")
