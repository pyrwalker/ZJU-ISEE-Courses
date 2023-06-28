#include<stdio.h>
#include<math.h>

double f(double x){
    return (exp(x) - x * x +3 * x - 2);
}
int main()
{
    double a = 0;
    double b = 1;
    double eps = 0.00001;
    int i = 1;
    
    if(fabs(f(a)) < eps){
        printf("solution: %lg\n", a);
    }else if(fabs(f(b)) < eps){
        printf("solution: %lg\n", b);
    }else{
        double c = (a + b) / 2;

        while(fabs(f(c) >= eps)){
            printf("mid%d:%lg\n",i,c);
            if(f(a) * f(c) < 0)
                b = c;
            else
                a = c;
            c = (a + b) / 2;
            i++;
            if(i > 100){
                break;
            }
        }
        if( i > 100)
            printf("can not found!");
        else
            printf("solution:%lg\n",c);
    }
    return 0;

}