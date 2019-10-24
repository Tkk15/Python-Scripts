class employee:
   
   empCount = 0

   def __init__(self):
      self.name= ""
      self.salary=0.0
      employee.empCount +=1

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      employee.empCount += 1
   
   def displayCount(self):
     print ("Total number of employees "  + employee.empCount)

   def displayEmployee(self):
      print ("Name : ", self.name,  ", Salary: ", self.salary)


emp1 = employee("Pat", 2000)
emp2 = employee("Matt", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print ("Total number of employees" + str(employee.empCount))

