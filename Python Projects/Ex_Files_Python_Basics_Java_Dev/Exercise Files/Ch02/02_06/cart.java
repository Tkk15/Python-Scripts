import java.util.*;
public class cart 
{

	public static void main(String[] args)
	{
		// TODO Auto-generated method stub
		String [] sC = new String [10];
		Scanner scan = new Scanner (System.in);
		int itemCount =0;
		int noOfItems =0;
		String itemManip="";
		String again = "Yes";
		while (again.equalsIgnoreCase("Yes"))
		{
			System.out.println("Please enter the  item you want to buy" );
			sC[itemCount] = scan.nextLine();
			itemCount++;
			System.out.println("Do you have one more item to buy?");
			again = scan.nextLine();
		//	scan.nextLine();
		}
		noOfItems =itemCount;
		itemCount=0;
		while (itemCount < sC.length)
		{
			System.out.println("The contents of the cart are " + sC[itemCount] );
			itemCount++;
		}
		do
		{
			System.out.println("What would you like to do? Press A for Add, R for Remove, D for Display ");
			itemManip = scan.nextLine();
			if (itemManip.equalsIgnoreCase("A"))
			{
				if ( noOfItems < sC.length )
				{
					System.out.println("Please enter the item you would like to buy");
					sC[noOfItems]= scan.nextLine();
				}
				else
					System.out.println("No more room in cart");
			}
			if (itemManip.equalsIgnoreCase("R"))
			{
				System.out.println("Please enter the item you would like to remove");
				String rItem = scan.next();
				for (int i =0; i < sC.length; i++)
				{
					String temp = sC[i];
					System.out.println(rItem);
					if (temp.equalsIgnoreCase("Milk") )
						sC[i] = "";
				}
			}
			if (itemManip.equalsIgnoreCase("D"))
				{
					for (int i =0; i < sC.length; i++)
						System.out.println(sC[i]);
				}
			System.out.println("Would you like to shop again?");
			itemManip = scan.nextLine();
		}while (itemManip.equalsIgnoreCase("Yes"));	
		System.out.println("Thank you for shopping!");
	}
	
}