print ("Let us go shopping today!")
list = []
shopMore = "Y"
while ( shopMore == "Y"):
	item = input ("Pick the item that you are buying")
	list.append(item)
	print ("Do you have any more items to buy?")
	shopMore = input ()
i=0
for i in  range (len(list)):
	print (list[i])
i-0
print ("What would you like to do today? Press A for adding an item, R for removing an item, L for the number of items in the cart,,D for Displaying the items in the cart,  X for Exit the system.")
listManip = input ()
while (listManip != "X" ):
	if (listManip == "A"):
		item = input("What is the item you would like to add to the cart?")
		list.append(item)
	elif (listManip == "R"):
		item = input("What is the item you would like to remove from the cart?")
		list.remove(item)
	elif (listManip == "L"):
		print ("The number of items in the cart is" + str (len(list)))
	elif (listManip == "D"):
		for i in  range (len(list)):
			print (list[i])	
	else:
		print ("Want to try again?")
	listManip = input("What would you like to do today? Press A for adding an item, R for removing an item, D for Displaying the items in the cart, L for the number of items in the cart, X for Exit the system.")
