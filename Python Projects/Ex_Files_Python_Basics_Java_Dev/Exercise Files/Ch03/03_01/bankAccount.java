import java.util.*;
public class bankAccount
{
 public static double totalAmount =0.0;
 public static void main (String []args)
 {
   String action ="";
   double accountBal =0.0;
   int aNumber =0;
   String aName = "";
   double amount =0.0;
   double balance =0.0;
   Scanner scan = new Scanner (System.in);
   System.out.println ("What is the name of your bank account holder?");
   aName = scan.nextLine();
   System.out.println("What is your account number?");
   aNumber = scan.nextInt();
   System.out.println("What is your initial balance?");
   totalAmount = scan.nextDouble();
   scan.nextLine();
   System.out.println("What would you like to do today: W for Withdraw, D for Deposit, B for checkBalance");
   action = scan.nextLine();
   if (action.equalsIgnoreCase("D"))
   {
     System.out.println("How much would you like to deposit?");
     amount = scan.nextDouble();
     balance = deposit(amount);
    }
   if (action.equalsIgnoreCase("W"))
    {
     System.out.println("How much would you like to withdraw?");
     amount = scan.nextDouble();
     balance = withdraw(amount);
    }
   if (action.equalsIgnoreCase("B"))
    {
     balance = checkBalance();
    }
   System.out.println("The amount in the account is " + balance);
 }
 // main program ends here

 // static methods are listed below.
 public static double deposit(double n)
 {
   totalAmount = totalAmount + n;
   return totalAmount;
 }
 
 public static double withdraw(double n)
 {
   totalAmount = totalAmount - n;
   return totalAmount;
 }
 
 public static double checkBalance()
 {
    return totalAmount;
 }
 
}