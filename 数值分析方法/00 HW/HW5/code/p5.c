
#include<stdio.h>
#include<math.h>

//use Eluer's method to approximate the solution for each of the following initial conditions value

double fn(double t,double w){
    return 1+w/t+pow(w/t,2);
}
int main(){
        double w=0;
    double n=10;
    double h=0.2;
    double t=1;
    for(int i=0;i<n;i++){
        w=w+h*fn(t,w);
        t=t+h;
    }
    printf("w=%f\n",w);
}