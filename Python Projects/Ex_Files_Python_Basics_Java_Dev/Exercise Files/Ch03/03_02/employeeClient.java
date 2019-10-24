import java.util.*;
public class employeeClient 
{

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		employee emp1 = new employee ("Pat", 4000);
		employee emp2 = new employee ("Matt",8000);
			
		System.out.println(emp1);
		System.out.println(emp2);
		
		System.out.println("The number of employees created so far " + employee.employeeCount);
				
	}

}
