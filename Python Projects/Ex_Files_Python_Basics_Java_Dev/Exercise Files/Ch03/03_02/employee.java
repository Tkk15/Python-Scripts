public class employee 
{
public static int employeeCount;
private String empName;
private double empSalary;

public employee()
{
	employeeCount = employeeCount + 1;
	empName ="";
	empSalary =0.0;
}

public employee(String eName, double eSal)
{
	employeeCount = employeeCount + 1;
	empName =eName;
	empSalary = eSal;
}

public String toString()
{
	return "Employee Name " + empName + " Employee Salary " + empSalary ;
}

}



