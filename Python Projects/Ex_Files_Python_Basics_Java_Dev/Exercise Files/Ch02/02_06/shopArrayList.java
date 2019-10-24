import java.text.NumberFormat;
import java.util.*; 
import java.io.*;
public class shopArrayList
{
  public static void main (String[] args) 
  {
    String itemName;
    Scanner scan = new Scanner(System.in);
    ArrayList <String> cart = new ArrayList<String>();      //declare and instantiate an ArrayList object
    String keepShopping = "y";
    do
    {
      System.out.println("Please enter the name of the item you want to shop");
      itemName = scan.nextLine();
      cart.add(itemName); 
      System.out.println ("Continue shopping (y/n)? ");
      keepShopping = scan.nextLine();
      System.out.println(keepShopping);
    }
while (keepShopping.equalsIgnoreCase("y"));
for (int count = 0; count < cart.size(); count++)
{
  System.out.println(cart.get(count));
}
keepShopping ="y";
do
{
System.out.println("What would you like to do today? Press A for add an item, R for remove an item, D for display the contents of the cart.");
String response = scan.nextLine();
if (response.equalsIgnoreCase("A"))
  {
      System.out.println("Please enter the name of the item you want to shop");
      itemName = scan.nextLine();
      cart.add(itemName);
  }
if (response.equalsIgnoreCase("R"))
  {
      System.out.println("Please enter the name of the item you want to remove");
      itemName = scan.nextLine();
      cart.remove(itemName);
  }
if (response.equalsIgnoreCase("D"))
{
  for (int count = 0; count < cart.size(); count++)
  {
    System.out.println(cart.get(count));
  }
}
System.out.println ("Continue shopping (y/n)? ");
keepShopping = scan.nextLine();
System.out.println(keepShopping);
}while (keepShopping.equalsIgnoreCase("y"));
 }  
}

