#include<stdio.h>
#include<math.h>

double fn(double x){
    return 1/(log(x)*x);
}

//romberg intergration to count R_{3,3}
int main(){
    double R33,R32,R31,R22,R21,R11;
    double h;
    double a,b;
    a=exp(1),b=exp(1)+1;
    //count R11
    h=b-a;
    R11=(h/2)*(fn(a)+fn(b));
    //count R21
    R21=(h/4)*(fn(a)+2*fn(a+h/2)+fn(b));
    //count R31
    R31=(h/8)*(fn(a)+2*(fn(a+h/4)+fn(a+h/2)+fn(a+3*h/4))+fn(b));
    //count R32
    R32=R31+(R31-R21)/3;
    //count R22
    R22=R21+(R21-R11)/3;
    //count R33
    R33=R32+(R32-R22)/15;
    printf("R_{33}=%f\n",R33);
}