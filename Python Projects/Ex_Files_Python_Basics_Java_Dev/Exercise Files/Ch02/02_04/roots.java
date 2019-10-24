public class roots
{
 public static void main (String [] args)
 {
   int startNum = 1;
   int endNum = 25;
   System.out.println ("Square" +'\t'+'\t' +'\t'+'\t' + "SquareRoot" +'\t'+'\t'+'\t'+'\t' +"CubeRoot");
   while (startNum <= endNum)
   {
    double square = startNum * startNum;
    double sqRoot = Math.sqrt (startNum);
    double cbRoot = Math.cbrt(startNum);
   
    System.out.println (square + " " +'\t'+'\t' +'\t'+'\t' + sqRoot +'\t'+'\t' +'\t'+'\t' + cbRoot);
    startNum = startNum + 1;
  }
 }
}