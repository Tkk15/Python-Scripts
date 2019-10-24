import java.util.*;
public class agePrivileges
{
 public static void main (String [] args)
 {
   //greater than 12 AND less than 20 - teen . 
   // else you are an adult or a child
   // less than 20 or !A US Citizen - you don't get to vote
   //else you get to vote
   Scanner scan = new Scanner (System.in);
   System.out.println("Please enter your age");
   int age = scan.nextInt();
   System.out.println("Are you a US Citizen?(Enter Yes or No)");
   String citizen = scan.next();
   if ((age >12) && (age <20))
     System.out.println ("You are a teen. You get to throw tantrums!");
   else
     System.out.println("You are a child. You get to throw tantrums!");
   if (( age < 20) || (!citizen.equalsIgnoreCase ("Yes")) )   
     System.out.println ("Sorry! No voting privileges");
   else
     System.out.println("You are an adult and you get to vote!");
 }
}