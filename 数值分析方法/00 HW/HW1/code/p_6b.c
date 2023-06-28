#include<stdio.h>
#include<math.h>

double f(double p){
    return (3*p*p - exp(p) + p)/3;
}
 int main()
 {
    double p0 = 1;
    double eps = 0.01;
    double p = 0;
    int i = 1;
    p = f(p0);
    printf("p0:%lg\n",p0);
    while(fabs(p - p0) > eps ){
        printf("p%d:%lg\n",i, p);
        p0 = p;
        p = f(p0);
        
        i++;
        if(i > 10000 ){
            break;
        }
    }
    if(i > 1000 ){
        printf("can not found a solution!\n");
    }else{
        printf("solution:%lg",p);
    }
 }