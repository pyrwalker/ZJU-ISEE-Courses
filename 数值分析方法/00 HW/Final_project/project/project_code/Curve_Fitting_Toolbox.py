import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.font as tkFont
import numpy as np
import tkinter
import sympy
import openpyxl
from scipy import linalg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sympy import expand


# 定义全局变量
global figure_window
global flag # 控制文件选择还是手动输入,默认为手动输入
flag = 1
# global filename
# filename = ''
global x_dataset # 横坐标数据集
global y_dataset # 纵坐标数据集
x_dataset = []
y_dataset = []
global piece # 控制三次样条的函数区间
global diffleft,diffright # 紧压样条两侧的函数

# def quit():
#     global figure_window
#     figure_window.quit()  # 结束主循环
#     figure_window.destroy()  # 销毁窗口
#     # figure_window.update()

def plot(x_dataset:list , y_dataset:list, poly ,root):
    # 取出数据集合中第一个和最后一个点
    x0 = x_dataset[0]
    xn = x_dataset[-1]
    # 设置步长
    size =xn - x0
    step = abs(xn - x0) / 500
    # 定义图标大小和像素
    f = Figure(figsize=(5, 4), dpi=100)
    # print(type(f))
    a = f.add_subplot(111)  # 添加子图
    # 给出画图的x数据点
    x = np.arange(x0 - size / 5, xn + size / 5, step)
    num = len(x)
    y=[0] * num
    # 将y代入函数得到对应值
    for i in range(num):
        y[i] = poly.evalf(subs ={'x':x[i]})
    a.plot(x, y) #作图
    # 将函数名 
    a.set_title(poly.xreplace({n: round(n, 3) for n in poly.atoms(sympy.Number)}),fontsize=8,color='black')
    # b.plot(x_dataset, y_dataset,'*')
    

    # 将绘制的图形显示到root上
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()  # 显示函数
    canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)  # 随窗口大小调整而调整
    # 显示导航工具栏
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tkinter.TOP,  
                      fill=tkinter.BOTH,
                      expand=tkinter.YES)
    # # 创建一个按钮
    # button = tkinter.Button(master=root, text="退出", command = quit())
    # # 按钮放在下边
    # button.pack(side=tkinter.BOTTOM)

# 分段绘制三次样条的图像
def plot_cubic(x_dataset:list , y_dataset:list, poly ,root, k):
    # 取出分段区间的初始点和终点
    xs = x_dataset[k]
    xe = x_dataset[k+1]
    step = abs(xe - xs) / 500
    f = Figure(figsize=(5, 4), dpi=100)
    # print(type(f))
    a = f.add_subplot(111)  # 添加子图:1行1列第1个
    x = np.arange(xs , xe, step)
    y=[0] * 500
    for i in range(500):
        y[i] = poly.evalf(subs ={'x':x[i]})
    a.plot(x, y)
    a.set_title(poly.xreplace({n: round(n, 3) for n in poly.atoms(sympy.Number)}),fontsize=8,color='black')

    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master = root)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)  # 随窗口大小调整而调整
    # matplotlib的导航工具栏显示上来(默认是不会显示它的)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
                      fill=tkinter.BOTH,
                      expand=tkinter.YES)
    # # 创建一个按钮
    # button = tkinter.Button(master=root, text="quit", command = quit(root))
    # # 按钮放在下边
    # button.pack(side=tkinter.BOTTOM)

x = sympy.symbols("x")
# x_data = [1,2]
# y_data = np.ndarray([1,2])
def fun_lagrange(x_dataset:list, y_dataset:np.ndarray):
    listNum = len(x_dataset) # 给定数据散点的个数
    LagrangePoly = 0 # 函数赋初值0
    for j in range(listNum):
        # print(j)
        LagrangePoly = LagrangePoly + y_dataset[j] * fun_lagrange_base(x_dataset, j)
    return expand(LagrangePoly)
# 定义求解朗格朗日插值多项式的系数的函数
def fun_lagrange_base(x_dataset:list, j):
    # print(j)
    # print(x_data)
    xj = x_dataset[j]
    L_j = 1
    x_dataset.pop(j) # 将下标为j的点从数据列表中删除 
    for xi in x_dataset:
        L_j = L_j * (x - xi) / (xj - xi)
    x_dataset.insert(j,xj) # 将删除的点重新加入列表中
    return L_j
# 函数形式为 y = a0 + a1 x^1 + a2 x^2 +...
# 定义乘幂与累加的复合运算函数，便于后续计算
def pow_sum(list:list, order, ylist = []):# ylist is for another pow and sum
    ret = 0.0 # 初值为0
    listNum = len(list)
    # 对ylist做判断，默认函数参量为空，此时都赋值为1，不影响list的乘幂
    if(ylist == []):
        ylist = [1] * listNum
    # 循环实现乘幂与累和
    for i in range(listNum):
        ret = ret + ylist[i] * list[i] ** order
    return ret
# 最小二乘法
def fun_least_square(x_dataset:list, y_dataset:np.ndarray, order):
    x = sympy.Symbol("x")
    # a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10= sympy.symbols("a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10")
    # a_coefficient = [a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]
    # a_coefficient = a_coefficient[0 : order + 2] # take order + 1 of these elements
    # error function for every point

    # Assign values to coeff_mat and const_arr
    # 定义系数矩阵与常数向量
    coeff_mat = np.zeros((order + 1) ** 2).reshape(order + 1, order + 1)
    const_arr = np.zeros(order + 1)
    # 计算系数矩阵
    for i in range(order + 1):
        # 计算常数向量
        const_arr[i] = pow_sum(x_dataset, i, y_dataset)
        for j in range(order + 1):
            coeff_mat[i][j] = pow_sum(x_dataset, (i+j))
    # 引入线性代数库求解线性方程组
    if(linalg.det(coeff_mat) == 0): # 如果系数矩阵不满秩，即没有唯一解
        return "there is no unique solution!" 
    a_coefficient_solution = linalg.solve(coeff_mat, const_arr)
    # output 
    # 函数初始为零
    least_square_polynomial = 0
    for i in range(order + 1):# 将系数矩阵与x的幂相乘
        least_square_polynomial = least_square_polynomial + a_coefficient_solution[i] * (x ** i) 
        Error = 0
    # total error
    for i in range(len(x_dataset)):
        P_order = 0 # 误差初始为0
        for j in range(order + 1):# '+1' correct the order
            P_order = P_order + a_coefficient_solution[j] * (x_dataset[i] ** j)
        Error = Error + (y_dataset[i] - P_order) ** 2
    print("Error",Error)
    return least_square_polynomial
# 三次自然样条
def fun_nature_cubic_spline(x_dataset:list, y_dataset:np.ndarray):
    listNum = len(x_dataset) - 1 # 下标最大值
    # 用于存放最终函数的列表
    natual_cubic_spline_polynomial = [0] * (listNum)
    # 定义系数列表
    a_coefficient = list(y_dataset)
    b_coefficient = [0] * (listNum+1)
    c_coefficient = [0] * (listNum+1)
    d_coefficient = [0] * (listNum+1)
    # 定义中间变量列表
    l = [0] * (listNum+1)
    u = [0] * (listNum+1)
    z = [0] * (listNum+1)
    alpha = [0] * (listNum+1)
    # 中间变量赋初值值
    l[0] = l[listNum] = 1 
    u[0] =z[listNum] =  z[0] = 0
    c_coefficient[listNum] = 0  
    # 循环得到系数矩阵及中间变量和系数的关系
    for i in range(listNum):
        hi = x_dataset[i+1] - x_dataset[i]
        if(i != 0):
            alpha[i] = 3 / hi * (a_coefficient[i+1] - a_coefficient[i])\
                - 3 / last_hi * (a_coefficient[i] - a_coefficient[i-1])
            l[i] = 2 * (x_dataset[i+1] - x_dataset[i-1]) - last_hi *u[i-1]
            u[i] = hi/l[i]
            z[i] = (alpha[i] - last_hi * z[i-1]) / l[i]
        last_hi = hi
    # 利用中间变量得到各个系数列表
    for j in range(listNum-1, -1, -1):
        hj = x_dataset[j+1] - x_dataset[j]
        c_coefficient[j] = z[j] - u[j] * c_coefficient[j+1]
        b_coefficient[j] = (a_coefficient[j+1] - a_coefficient[j]) / hj\
            -hj * (c_coefficient[j+1]+2 * c_coefficient[j]) / 3
        d_coefficient[j] = (c_coefficient[j+1] - c_coefficient[j]) / (3 * hj)
    # 将系数与对应x的次方相乘，得到最终表达式
    for k in range(listNum):
        natual_cubic_spline_polynomial[k] = a_coefficient[k] + \
                                            b_coefficient[k] * (x - x_dataset[k]) +\
                                            c_coefficient[k] * (x - x_dataset[k]) ** 2 +\
                                            d_coefficient[k] * (x - x_dataset[k]) ** 3
        natual_cubic_spline_polynomial[k] = expand(natual_cubic_spline_polynomial[k]) # 函数展开
    # 返回函数的列表
    return natual_cubic_spline_polynomial

def fun_clamped_cubic_spline(x_dataset:list, y_dataset:np.ndarray, diff_x0, diff_xn):
    
    FPO = diff_x0 # 左侧导数值
    FPN = diff_xn # 右侧导数值

    listNum = len(x_dataset) - 1 # 下标最大值
    # 构建函数列表
    clamped_cubic_spline_polynomial = [0] * (listNum)
    # 构建系数和中间变量表达式
    a_coefficient = list(y_dataset)
    b_coefficient = [0] * (listNum+1)
    c_coefficient = [0] * (listNum+1)
    d_coefficient = [0] * (listNum+1)
    l = [0] * (listNum+1)
    u = [0] * (listNum+1)
    z = [0] * (listNum+1)
    alpha = [0] * (listNum+1)
    # 中间变量赋初始值
    alpha[0] = 3 * (a_coefficient[1] - a_coefficient[0]) / (x_dataset[1] - x_dataset[0]) -3 * FPO 
    l[0] = 2 * (x_dataset[1] - x_dataset[0])
    u[0] = 0.5
    z[0] = alpha[0] / l[0]

    # 循环得到系数矩阵与中间变量的关系
    for i in range(listNum):
        hi = x_dataset[i+1] - x_dataset[i]
        if(i != 0):
            alpha[i] = 3 / hi * (a_coefficient[i+1] - a_coefficient[i])\
                - 3 / last_hi * (a_coefficient[i] - a_coefficient[i-1])
            l[i] = 2 * (x_dataset[i+1] - x_dataset[i-1]) - last_hi *u[i-1]
            u[i] = hi/l[i]
            z[i] = (alpha[i] - last_hi * z[i-1]) / l[i]
        last_hi = hi
        # 单独考虑循环到最后一次的规律
        if(i == listNum-1):
            alpha[listNum] =  3 * FPN - 3 * (a_coefficient[listNum] - a_coefficient[listNum-1]) /hi
            l[listNum] = hi * (2 - u[listNum-1])
            z[listNum] = (alpha[listNum] - hi * z[listNum-1])/l[listNum]
            c_coefficient[listNum] = z[listNum]
    # 根据系数关系得到系数列表
    for j in range(listNum-1, -1, -1):
        hj = x_dataset[j+1] - x_dataset[j]
        c_coefficient[j] = z[j] - u[j] * c_coefficient[j+1]
        b_coefficient[j] = (a_coefficient[j+1] - a_coefficient[j]) / hj-\
                            hj * (c_coefficient[j+1] + 2 * c_coefficient[j]) / 3
        d_coefficient[j] = (c_coefficient[j+1] - c_coefficient[j]) / (3 * hj)
    # 将系数与对应x的次方相乘，得到最终表达式
    for k in range(listNum):
        clamped_cubic_spline_polynomial[k] = a_coefficient[k] + \
                                            b_coefficient[k] * (x - x_dataset[k]) +\
                                            c_coefficient[k] * (x - x_dataset[k]) ** 2 +\
                                            d_coefficient[k] * (x - x_dataset[k]) ** 3
        clamped_cubic_spline_polynomial[k] = expand(clamped_cubic_spline_polynomial[k]) # 将函数展开
    # 返回函数列表    
    return clamped_cubic_spline_polynomial





# 读入文件
def readfile():
    global flag
    filename = filedialog.askopenfilename(title='打开excel文件', filetypes=[('XLSX', '*.xlsx'),('XLS','*xls')])
    if(filename != ''):
        flag = 0 # 改为从文件输入
    entry_filename.insert(0,filename) # 显示读入的文件名与地址
    workbook = openpyxl.load_workbook(filename)  # 返回一个workbook数据类型的值
    sheet = workbook.active  # 获取活动表
    # 获取第一和第二列
    x_cell = sheet['A']
    y_cell = sheet['B']
    # 将前两列的数据分别赋值给x_dataset和y_dataset
    for xi in x_cell:
        x_dataset.append(xi.value) 
    for yi in y_cell:
        y_dataset.append(yi.value)
    # print(x_dataset,y_dataset)    
    return filename
#清空x输入框
def ClearAllxData():
    entry_x_dataset.delete(0,END)
# 清空y输入框
def ClearAllyData():
    entry_y_dataset.delete(0,tk.END)
# 消息提醒弹窗,判断输入是否为空
def input_judge(): 
	tk.messagebox.showinfo(title='警告',
		message='输入不能为空！') 
def fun_button1():
    tk.messagebox.showinfo(title='帮助',message='1.手动输入请用,分隔(英文输入),文件输入请将第一列设置为横坐标，第二列设置为纵坐标；2.每次拟合完函数请重新启动软件；3.样条插值需要输入拟合的区间，如第一个点到第二点称为第0段') 
# def quit():
#     root.quit()  # 结束主循环
#     root.destroy()  # 销毁窗口

def submit():
    # global figure_window

    # figure_window = tkinter.Tk()  # 创建画图窗口
    # figure_window.title("figure")
    if(flag):# 手动输入
        # 为空会报错，需要判断是否为空    
        if(entry_x_dataset.get() == '' or entry_y_dataset.get() == ''):
            input_judge()
        global x_dataset,y_dataset
        # 读入输入框中的数据点
        x_dataset = list(map(float,entry_x_dataset.get().split(',')))# 对读入的字符串处理为浮点数类型,才能入列表
        y_dataset = list(map(float,entry_y_dataset.get().split(',')))
    # 拉格朗日
    if selectapprox.get() == 0:
        lagrange_interpolation_polynomial = fun_lagrange(x_dataset, y_dataset)
        print("lagrange_interpolation_polynomial### {}".format(lagrange_interpolation_polynomial))
        plot(x_dataset, y_dataset, lagrange_interpolation_polynomial, root)
        # x_point = input() # to caculate the value of the function at this x_point
        # lagrange_interpolation_polynomial_point = lagrange_interpolation_polynomial.evalf(subs ={'x':x_point})
    # nature cubic spline
    if selectapprox.get() == 1:
        if(entry_nature_piece.get() == ''): # 判断非空
            input_judge()
        global piece
        piece = int(entry_nature_piece.get())
        nature_cubic_spline_polynomial = fun_nature_cubic_spline(x_dataset, y_dataset)
        print("nature_cubic_spline_polynomial###",nature_cubic_spline_polynomial[piece])
        plot_cubic(x_dataset, y_dataset, nature_cubic_spline_polynomial[piece], root ,piece)
    # clamped cubic spline
    if selectapprox.get() == 2:
        if(entry_clamped_piece.get() == '' or entry_clamped_diffright.get() == '' or entry_clamped_diffleft.get() ==''):# 判断非空
            input_judge()
        piece = int(entry_clamped_piece.get())
        global diffleft,diffright
        diffleft = int(entry_clamped_diffleft.get()) # 读入左右导数 
        diffright = int(entry_clamped_diffright.get())
        clamped_cubic_spline_polynomial = fun_clamped_cubic_spline(x_dataset, y_dataset, diff_x0 = diffleft, diff_xn = diffright) #pass in five parameters
        print("clamped_cubic_spline_polynomia###",clamped_cubic_spline_polynomial[piece])
        plot_cubic(x_dataset, y_dataset, clamped_cubic_spline_polynomial[piece], root, piece)
    # 最小二乘法
    if selectapprox.get() == 3:
        order = int(entry_order.get())
        least_square_polynomial = fun_least_square(x_dataset, y_dataset, order = order)
        print("least_square_polynomial###", least_square_polynomial)
        plot(x_dataset, y_dataset, least_square_polynomial, root)
    # root.update()
    # figure_window.mainloop()

# 创建主窗口
root = Tk()
# main window setting
root.title("Curve Fitting Toolbox") # name
root.resizable() # Allows you to change the window size
width = 600
height = 450 # set window's size
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2) # make it keep in the center of the screen  
root.geometry(size_geo)
root.config(background ="#F5F5F5")
#内容设置
# 定义第一个容器，工具顶栏
frame_sidebar = tk.LabelFrame(root, labelanchor="n",bg='#F5F5F5')
# 使用 place 控制 LabelFrame 的位置
frame_sidebar.place(relx=0, rely=0, relwidth=1, relheight=0.08)
fontStyle = tkFont.Font(family = "TkDefaultFont",size=13)
button_1 = tk.Button(frame_sidebar, bg ='white' ,bd = 0.5, text="帮助(H)",font=fontStyle,relief ='raised', height = 1,command = fun_button1)
button_1.place(relx=0.02)

# 输入容器
frame_input = tk.LabelFrame(root, labelanchor="n",bg='#F5F5F5')
frame_input.place(relx=0, rely=0.07, relwidth=1, relheight=0.3)

label_markeswords = tk.Label(frame_input, bg ='#F5F5F5' ,bd = 0, text="请输入需要拟合的点：",font=fontStyle,relief ='raised', height = 1)
label_markeswords.place(relx=0,rely=0.01)

fontStyle = tkFont.Font(family = "TkDefaultFont",size=10)

label_x_dataset = tk.Label(frame_input, bg ='#F5F5F5' ,bd = 0, text="横坐标数据点:",font=fontStyle, relief ='raised', height = 1)
label_x_dataset.place(relx=0.001,rely=0.3)

entry_x_dataset = tk.Entry(frame_input,bg='white',xscrollcommand = 1)
entry_x_dataset.place(relx=0.15,rely=0.262,width=400, height=30)

button_x_dataset =tk.Button(frame_input,text='清空',command=ClearAllxData)
button_x_dataset.place(relx=0.85,rely=0.260)


label_y_dataset = tk.Label(frame_input, bg ='#F5F5F5' ,bd = 0, text="纵坐标数据点:",font=fontStyle, relief ='raised', height = 1)
label_y_dataset.place(relx=0.001,rely=0.7)

entry_y_dataset = tk.Entry(frame_input,bg='white',xscrollcommand = 1)
entry_y_dataset.place(relx=0.15,rely=0.642,width=400, height=30)

button_y_dataset =tk.Button(frame_input,text='清空',command=ClearAllyData)
button_y_dataset.place(relx=0.85,rely=0.640)

# 拟合方式选择窗口
frame_approx = tk.LabelFrame(root, labelanchor="n",bg='#F5F5F5')
frame_approx.place(relx=0, rely=0.35, relwidth=1, relheight=0.4)

fontStyle = tkFont.Font(family = "TkDefaultFont",size=13)#改变字体设置

label_markeswords = tk.Label(frame_approx, bg ='#F5F5F5' ,bd = 0, text="请选择拟合方式",font=fontStyle,relief ='raised', height = 1)
label_markeswords.place(relx=0)

fontStyle = tkFont.Font(family = "TkDefaultFont",size=11)

selectapprox = IntVar()
selectapprox.set(0)# 默认选择拉格朗日插值法
# 拉格朗日
rbutton_lagrange = tk.Radiobutton(frame_approx, text="拉格朗日插值法", font = fontStyle,value=0,variable=selectapprox)
rbutton_lagrange.place(relx=0.05,rely=0.1)
# 三次自然样条插值
rbutton_nature_cubic_spline = tk.Radiobutton(frame_approx, text="三次自然样条插值法", font = fontStyle,value=1,variable=selectapprox)
rbutton_nature_cubic_spline.place(relx=0.05,rely=0.3)
# 选择拟合区间
label_nature_piece = tk.Label(frame_approx, bg ='#F5F5F5' ,bd = 0, text="拟合区间(0,1,2...)",font=fontStyle, height = 1)
label_nature_piece.place(relx=0.35,rely=0.33)

entry_nature_piece = tk.Entry(frame_approx,bg='white')
entry_nature_piece.place(relx=0.56,rely=0.33,width=30, height=20)
# 三次紧压样条插值
rbutton_clamped_cubic_spline = tk.Radiobutton(frame_approx, text="三次紧压样条插值法", font = fontStyle,value=2,variable=selectapprox)
rbutton_clamped_cubic_spline.place(relx=0.05,rely=0.5)
# 选择拟合区间
label_clamped_piece = tk.Label(frame_approx, bg ='#F5F5F5' ,bd = 0, text="拟合区间(0,1,2...)",font=fontStyle, height = 1)
label_clamped_piece.place(relx=0.35,rely=0.52)

entry_clamped_piece = tk.Entry(frame_approx,bg='white')
entry_clamped_piece.place(relx=0.56,rely=0.52,width=30, height=20)
# 获取两侧导数初值
label_clamped_diffleft = tk.Label(frame_approx, bg ='#F5F5F5' ,bd = 0, text="两侧导数初值",font=fontStyle, height = 1)
label_clamped_diffleft.place(relx=0.63,rely=0.52)

entry_clamped_diffleft = tk.Entry(frame_approx,bg='white')
entry_clamped_diffleft.place(relx=0.8,rely=0.52,width=30, height=20)

entry_clamped_diffright = tk.Entry(frame_approx,bg='white')
entry_clamped_diffright.place(relx=0.87,rely=0.52,width=30, height=20)
# 多项式函数拟合
rbutton_least_square_approx = tk.Radiobutton(frame_approx, text="多项式函数拟合", font = fontStyle,value=3,variable=selectapprox)
rbutton_least_square_approx.place(relx=0.05,rely=0.7)
# 阶数输入
label_y_dataset = tk.Label(frame_approx, bg ='#F5F5F5' ,bd = 0, text="阶数",font=fontStyle, height = 1)
label_y_dataset.place(relx=0.32,rely=0.725)

entry_order = tk.Entry(frame_approx,bg='white')
entry_order.place(relx=0.4,rely=0.72,width=30, height=20)

#文件选择 上传窗口
frame_submit = tk.LabelFrame(root, labelanchor="s",bg='#F5F5F5')
frame_submit.place(relx=0, rely=0.72, relwidth=1, relheight=0.4)

button_upload =tk.Button(frame_submit,text='选择文件',command=readfile)
button_upload.place(relx=0.05,rely=0.2)

button_submit =tk.Button(frame_submit,text='开始拟合',command=submit)
button_submit.place(relx=0.8,rely=0.2)

entry_filename = tk.Entry(frame_submit, width=35, font=("宋体", 10, 'bold'))
entry_filename.place(relx=0.17,rely=0.21,height =30)

# 维持主窗口
root.mainloop()


# input("please input any key to exit!")