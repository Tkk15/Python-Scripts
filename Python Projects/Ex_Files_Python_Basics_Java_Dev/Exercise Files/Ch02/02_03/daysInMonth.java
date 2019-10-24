/**
 * 
 */
package daysInMonth;

/**
 * @author Deepa Muralidhar
 *
 */
import java.util.*;
public class daysInMonth
{
	public static void main(String[] args)
	{
	// TODO Auto-generated method stub
		  Scanner scan = new Scanner (System.in);
		  int month=0;
		  int OddOrEven=0;
		  System.out.println("Please enter the number of the month you want the days for");
		  month = scan.nextInt();
		  OddOrEven = month % 2;
		  /*
		  if (month == 2)
		    System.out.println("there are 28 days in this month");
		  else 
		  if (OddOrEven ==0)
		    System.out.println("there are 30 days in this month");
		  else
		    System.out.println("there are 31 days in this month");
		  */
		  if (month == 2)
		  {
		    System.out.println("there are 28 days in this month");
		  }
		  else if (OddOrEven ==0)
		    System.out.println("there are 30 days in this month");
		  else
		    System.out.println("there are 31 days in this month");
		  
	   }
}
