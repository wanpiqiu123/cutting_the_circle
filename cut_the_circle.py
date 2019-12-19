'''
Originally written by Jiaming Luo 
For course "Mathematical Algorithm in Traditional Chinese Culture"
Finish date: December 13, 2019
Feel free to use or modify it
'''

from graphics import * #use "pip install graphics.py" if you don't have this library
import random
import time
from math import *
import numpy as np

class graph():
    def __init__(self):
        self.window = GraphWin("割圆术",900,700)
        self.window.setCoords(-300,-350,600,350)
        self.window.setBackground("gray")
        self.center = Point(0,0)
        self.radias = 250 #圆的半径
        self.out_radias = 0 #外切正多边形距离圆心的距离
        self.devide = 6 #正多边形的边数
        self.inner_angle = [] #内接正多边形顶点的角度
        self.outer_angle = [] #外切正多边形顶点的角度
        self.inner_dots = [] #内接正多边形顶点的坐标
        self.outer_dots = [] #外切正多边形顶点的坐标
        self.inner_polygon = 0 #内接正多边形
        self.outer_polygon = 0 #外切正多边形
        self.inner_perimeter = 0 #内接正多边形周长
        self.outer_perimeter = 0 #外切正多边形周长
        self.txt_inner_p = Text(Point(430,200),"内接正多边形周长：")
        self.txt_inner_p.setSize(15)
        self.txt_inner_p.setTextColor("gold")
        self.txt_inner_p.draw(self.window)
        self.txt_outer_p = Text(Point(430,180),"外接正多边形周长：")
        self.txt_outer_p.setSize(15)
        self.txt_outer_p.setTextColor("DeepSkyBlue")
        self.txt_outer_p.draw(self.window)
        self.txt_circle_p = Text(Point(430,160),"圆的周长："+str(round(2*pi,12)))
        self.txt_circle_p.setSize(15)
        self.txt_circle_p.setTextColor("crimson")
        self.txt_circle_p.draw(self.window)
        self.txt_pi_p = Text(Point(430,140),"PI的近似值：")
        self.txt_pi_p.setSize(15)
        self.txt_pi_p.setTextColor("PaleGreen")
        self.txt_pi_p.draw(self.window)
        self.explain = '''
        说明：使用阿基米德方法进行圆周率PI的计算\n
        首先输入正多边形的边数，点击“更新”按钮进行更新\n
        可使用“自动进行”按钮让边长持续扩大两倍直到超过10万\n
        自动进行可能有一些卡顿，等待结束后可重新操作\n
        在非计算状态下可点击“退出”离开程序界面
        '''
        self.txt_pi_ex = Text(Point(420,-180),self.explain)
        self.txt_pi_ex.setSize(12)
        self.txt_pi_ex.setTextColor("Orange")
        self.txt_pi_ex.draw(self.window)
        self.init_draw()
        self.run()

    def init_draw(self):
        self.circle = Circle(self.center,self.radias)
        self.circle.setOutline("crimson")
        self.circle.setWidth(2)
        self.circle.draw(self.window)

        self.devide_p = Point(450,60)
        self.input1 = Entry(self.devide_p,5)
        self.input1.setText(str(self.devide))
        self.input1.setTextColor("white")
        self.input1.draw(self.window)
        t0=Text(Point(410,60),"边数:")
        t0.setSize(12)
        t0.draw(self.window)

        self.btn_s = Rectangle(Point(390,-30),Point(430,10))
        self.btn_s.setFill("white")
        self.btn_s.setOutline("white")
        self.btn_s.draw(self.window)
        t1=Text(Point(410,-10),"更新").draw(self.window)
        t1.setTextColor("black")

        self.btn_e = Rectangle(Point(440,-30),Point(480,10))
        self.btn_e.setFill("white")
        self.btn_e.setOutline("white")
        self.btn_e.draw(self.window)
        t2=Text(Point(460,-10),"退出").draw(self.window)
        t2.setTextColor("black")

        self.btn_auto = Rectangle(Point(390,-80),Point(480,-40))
        self.btn_auto.setFill("white")
        self.btn_auto.setOutline("white")
        self.btn_auto.draw(self.window)
        t3=Text(Point(435,-60),"自动进行").draw(self.window)
        t3.setTextColor("black")
        
    def if_btn(self,point,btn): #判断鼠标点击是否在按钮内
        ll = btn.getP1()
        ur = btn.getP2()
        return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

    def draw_dot(self,dot,color = 'blue'): #画点
        small_circle = Circle(dot,1)
        small_circle.setOutline(color)
        small_circle.setFill(color)
        small_circle.draw(self.window)
        return small_circle

    def draw_polygon(self,point_list,color = 'green'): #画正多边形
        p = Polygon(point_list)
        p.setOutline(color)
        p.setWidth(2)
        p.draw(self.window)
        return p

    def dot_list_angle(self,devide): #获得n等分点的角度
        return np.linspace(0,2*pi,devide,False).tolist()

    def outer_radias(self,devide): #计算外切正多边形顶点与圆心的距离
        angle = pi/devide
        return self.radias/cos(angle)

    def outer_dot_list_angle(self,devide): #获得外切正多边形的顶点角度
        angle = pi/devide
        return np.linspace(angle,2*pi+angle,devide,False).tolist()

    def angle2point(self,radias,angle_list): #将角度转化成顶点坐标
        point_list = []
        for angle in angle_list:
            point_list.append(Point(cos(angle)*radias,sin(angle)*radias))
        return point_list

    def perimeter(self,radias,devide): #计算正多边形的周长
        angle = pi/devide
        return round(devide*2*sin(angle)*radias/self.radias,11)

    def draw_all(self): #更新所有显示内容
        tmp = eval(self.input1.getText())
        if tmp<=2 or type(tmp)!=int: #校验输入格式
            pass
        else:
            self.devide = eval(self.input1.getText())
        self.inner_angle = self.dot_list_angle(self.devide)
        self.out_radias = self.outer_radias(self.devide)
        self.outer_angle = self.outer_dot_list_angle(self.devide)
        self.inner_dots = self.angle2point(self.radias,self.inner_angle)
        self.outer_dots = self.angle2point(self.out_radias,self.outer_angle)
        if self.inner_polygon!=0:
            self.inner_polygon.undraw()
        self.inner_polygon=self.draw_polygon(self.inner_dots,"gold")
        if self.outer_polygon!=0:
            self.outer_polygon.undraw()
        self.outer_polygon=self.draw_polygon(self.outer_dots,"DeepSkyBlue")
        self.inner_perimeter = self.perimeter(self.radias,self.devide)
        self.outer_perimeter = self.perimeter(self.out_radias,self.devide)
        self.txt_inner_p.undraw()
        self.txt_inner_p = Text(Point(430,200),"内接正多边形周长："+str(self.inner_perimeter))
        self.txt_inner_p.setSize(15)
        self.txt_inner_p.setTextColor("gold")
        self.txt_inner_p.draw(self.window)
        self.txt_outer_p.undraw()
        self.txt_outer_p = Text(Point(430,180),"外接正多边形周长："+str(self.outer_perimeter))
        self.txt_outer_p.setSize(15)
        self.txt_outer_p.setTextColor("DeepSkyBlue")
        self.txt_outer_p.draw(self.window)
        self.txt_pi_p.undraw()
        self.txt_pi_p = Text(Point(430,140),"PI的近似值："+str(round(((self.inner_perimeter+self.outer_perimeter)/4),11)))
        self.txt_pi_p.setSize(15)
        self.txt_pi_p.setTextColor("PaleGreen")
        self.txt_pi_p.draw(self.window)

    def run(self):
        while True:
            self.draw_all()
            point = self.window.getMouse()
            if self.if_btn(point,self.btn_s): #更新
                self.draw_all()
            if self.if_btn(point,self.btn_e): #退出
                break
            if self.if_btn(point,self.btn_auto): #自动播放
                while self.devide <=100000: #一直加倍直到100,000（这个值可以修改）
                    self.input1.setText(str(self.devide*2))
                    time.sleep(.5)
                    self.draw_all()
        self.window.close()

if __name__ == "__main__":
    graph = graph()
    