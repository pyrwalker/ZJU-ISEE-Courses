<div class="cover" style="page-break-after:always;font-family:方正公文仿宋;width:100%;height:100%;border:none;margin: 0 auto;text-align:center;">
    <div style="width:60%;margin: 0 auto;height:0;padding-bottom:10%;">
        </br>
        <img src="https://raw.githubusercontent.com/Keldos-Li/pictures/main/typora-latex-theme/ZJU-name.svg" alt="校名" style="width:100%;"/>
    </div>
    </br></br></br></br></br>
    <div style="width:60%;margin: 0 auto;height:0;padding-bottom:40%;">
        <img src="https://raw.githubusercontent.com/Keldos-Li/pictures/main/typora-latex-theme/ZJU-logo.svg" alt="校徽" style="width:100%;"/>
	</div>
    </br></br></br></br></br></br></br></br>
    <span style="font-family:华文黑体Bold;text-align:center;font-size:20pt;margin: 10pt auto;line-height:30pt;">Numerical Analysis Assignment #2</span>
    <p style="text-align:center;font-size:14pt;margin: 0 auto"> </p>
    </br>
    </br>
    <table style="border:none;text-align:center;width:72%;font-family:仿宋;font-size:14px; margin: 0 auto;">
    <tbody style="font-family:方正公文仿宋;font-size:12pt;"> 
    	<tr style="font-weight:normal;"> 
    		<td style="width:20%;text-align:right;">授课教师</td>
    		<td style="width:2%">：</td> 
    		<td style="width:40%;font-weight:normal;border-bottom: 1px solid;text-align:center;font-family:华文仿宋">余官定</td>     </tr>
    	<tr style="font-weight:normal;"> 
    		<td style="width:20%;text-align:right;">姓名　</td>
    		<td style="width:2%">：</td> 
    		<td style="width:40%;font-weight:normal;border-bottom: 1px solid;text-align:center;font-family:华文仿宋">叶炳涛</td>     </tr>
    	<tr style="font-weight:normal;"> 
    		<td style="width:20%;text-align:right;">学　　号</td>
    		<td style="width:2%">：</td> 
    		<td style="width:40%;font-weight:normal;border-bottom: 1px solid;text-align:center;font-family:华文仿宋">3210103529</td>     </tr>
    	<tr style="font-weight:normal;"> 
    		<td style="width:20%;text-align:right;">日　　期</td>
    		<td style="width:2%">：</td> 
    		<td style="width:40%;font-weight:normal;border-bottom: 1px solid;text-align:center;font-family:华文仿宋">2002-10-16</td>     </tr>
    </tbody>              
    </table>
</div>

[TOC]



##  Problem 1

牛顿方法如下：
$$
p_{n+1}=p_n-\frac{f(p_n)}{f'(p_n)}
$$
所以，经过两次迭代，$p_2=-0.8656841632$.
$p_0$会导致$f'(p_0)=0$，不能使用。
## Problem 2
(Ⅰ) 
$$
 x_{k+1} = 2x_{k}-bx_{k}^2\\
 \epsilon _{k+1}=\frac{\frac{1}{b}-x_{k+1}}{\frac{1}{b}} =1-bx_{k+1}=1-2bx_k+b^2x_k^2=(1-bx_k)^2=\epsilon_k^2
$$

 （Ⅱ) 
$$
 x_{k+1} = 2x_{k}-bx_{k}^2\quad x\in(0,\frac{2}{b})
$$

so we can find $x_1\in(0,\frac{1}{b})$
对于
$$
f(x)=2x-bx^2
$$
故存在$k\in(0,1)$，我们有$|g'(x)|=|1-2bx|<k$，根据MVT，x收敛至$f(x)$的不动点$\frac{1}{b}$.

## Problem 3

**the code is in the file, here only present the results. By the way, I try to make the procedure run more times,which can find the final root**

### a.

![image-20221018003216074](D:/my%20knowledge%20base/typora_photo/image-20221018003216074.png)

### b.

![image-20221018003129793](D:/my%20knowledge%20base/typora_photo/image-20221018003129793.png)

## Problem 4

试了多个初值，结果处于没有收敛和迭代速度很慢两种情况，可能是由于步长设置不合理导致，代码已附在文件夹中

## Problem 5

### a.


$$
J\left(x_{1}, x_{2}\right)=\left(\begin{array}{cc}
\frac{x_{1}}{5} & \frac{x_{2}}{5} \\
\frac{1+x_{2}^{2}}{10} & \frac{x_{1} x_{2}}{5}
\end{array}\right)取$K=0.95$，则
当 $x_{i} \in D $时,
$$

$$
\left|\frac{\partial g_{i}(x)}{\partial x_{j}}\right| \leq\left|\frac{\partial g_{2}(x)}{\partial x_{2}}\right|=\left|\frac{x_{1} x_{2}}{5}\right| \leq \frac{9}{20}<\frac{0.95}{2}
$$

由上述定理, 在  D  上不动点唯一.

### b.

代入计算有：
$$
\begin{array}{c}
x^{(0)}=[0,1]^{t} \\
x^{(1)}=\left[\frac{9}{10}, \frac{8}{10}\right]^{t} \\
x^{(2)}=[1.045,0.9046]^{t}
\end{array}
$$

