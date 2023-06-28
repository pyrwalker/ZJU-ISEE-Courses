#include<stdio.h>
#include<math.h>
 int main()
 {
    double x=10;
    double eps=0.000005;
    double a1,a2,b1,b2;
    double e = 2.7182818284590452353602;
    a1 = cos(x) * eps;
    a2 = cos(x+eps) * eps;
    b1 = a1 / sin(x);
    b2 = a2 / sin(x);
    printf("%.20f,%.20f\n",a2,a1);
    printf("%.20f,%.20f\n",b2,b1);
    
 }