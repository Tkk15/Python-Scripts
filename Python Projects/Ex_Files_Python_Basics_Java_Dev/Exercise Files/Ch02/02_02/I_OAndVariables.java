import java.util.*;
public class I_OAndVariables
{
  public static void main (String [] args)
  {
    Scanner scan = new Scanner (System.in);
    String name = "";
    int age = 0;
    double height = 0.0;
    System.out.print("Please can you tell me your name?");
    name = scan.next ();
                     
    System.out.print("Please can you tell me what you do?");
    occupation = scan.nextInt ();
    
    System.out.print("Please can you tell me your favorite activity?");
    favActivity = scan.nextDouble ();
    
    System.out.println (" So, " + name + " " + "you are the " + occupation + "and your favorite activity is  " + favActivity   ) ;    
    
  } 
  
}