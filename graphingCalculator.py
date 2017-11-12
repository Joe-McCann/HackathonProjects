import turtle
import math
from colorsys import hls_to_rgb
from random import random

'''
Calculator class by Joe McCann

'''

class calculator:

    def __init__(self, x_bounds = [-10, 10], y_bounds = [-10, 10], xaxis = 0, screen_limx = [-775, 775], screen_limy = [-775, 775], background_color="white", pen_color="black"):
        self.plane = turtle.Screen()
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.bg_color = background_color
        self.p_color = pen_color
        self.axis_color = pen_color
        self.x_lim = x_bounds
        mag = (abs(y_bounds[0]) + abs(y_bounds[1]))*.9/2
        self.y_lim =  [y_bounds[0]-mag, y_bounds[1]+mag]
        self.screen_x = screen_limx
        self.screen_y = screen_limy

        self.t.color(self.p_color)
        self.plane.bgcolor(self.bg_color)
        self.drawAxis()

    #Draw correct relative axis
    def drawAxis(self):
        self.t.color(self.axis_color)
        self.safeGoto(self.screen_x[0], self.CoC(0, self.y_lim, self.screen_y))
        self.t.goto(self.screen_x[1], self.CoC(0, self.y_lim, self.screen_y))
        self.safeGoto(self.CoC(0, self.x_lim, self.screen_x), self.screen_y[0])
        self.t.goto(self.CoC(0, self.x_lim, self.screen_x), self.screen_y[1])

    def changeAxis(self, x_bounds, y_bounds):
        self.x_lim = x_bounds
        mag = (abs(y_bounds[0]) + abs(y_bounds[1]))*.9/2
        self.y_lim =  [y_bounds[0]-mag, y_bounds[1]+mag]
        self.screenReset()

    #Goto without drawing
    def safeGoto(self, x, y):
        self.t.up()
        self.t.goto(x, y)
        self.t.down()

    #Change of coordinates
    def CoC(self, point, u, v):
        a = (point-u[0])
        b = (u[1]-u[0])
        c = (v[1]-v[0])
        return a/b*c+v[0]

    def toGraphable(self, x, y):
        return self.CoC(x, self.x_lim, self.screen_x), self.CoC(y, self.y_lim, self.screen_y)
    
    #Graph a function given a function of y. Give another function of x to plot a parametric equation
    def graph(self, f, fx=lambda x:x, step_size=.1, col=False, t_int = False):
        if col:
            self.t.color(col)
        else:
            self.t.color(hls_to_rgb(random(), .5, 1))
        rnge = self.x_lim
        if t_int:
            rnge = t_int
        xpoints = [rnge[0]+i*step_size for i in range(0, math.ceil((rnge[1]-rnge[0])/step_size))]
        count = 0
        while True:
            try:
                self.safeGoto(*self.toGraphable(fx(xpoints[count]), f(xpoints[count])))
                break
            except:
                count+=1
                if count > len(xpoints):
                    return
                continue
        for point in xpoints[count:]:
            try:
                self.t.goto(*self.toGraphable(fx(point), f(point)))
                self.t.down()
            except:
                self.t.up()
        self.t.color(self.p_color)

    def graphPolar(self, f, step_size=.1, col=False, theta_int=[0,2*math.pi]):
        if col:
            self.t.color(col)
        else:
            self.t.color(hls_to_rgb(random(), .5, 1))
        count = 0
        thetas = [theta_int[0]+step_size*i for i in range(0, math.ceil((theta_int[1]-theta_int[0])/step_size))]
        
        while True:
            try:
                coords = [f(thetas[count])*math.cos(thetas[count]), f(thetas[count])*math.sin(thetas[count])]
                self.safeGoto(*self.toGraphable(*coords))
                break
            except:
                count+=1
                if count > len(thetas):
                    return
                continue
        for theta in thetas[count:]:
            try:
                coords = [f(theta)*math.cos(theta), f(theta)*math.sin(theta)]
                self.t.goto(*self.toGraphable(*coords))
                self.t.down()
            except:
                self.t.up()
                continue
        self.t.color(self.p_color)

    def graphSequence(self, f, initial, col=False, N=False):
        if col:
            self.t.color(col)
        else:
            self.t.color(hls_to_rgb(random(), .5, 1))
        if not N:
            N = self.x_lim[1]+1
        n = [i for i in range(1, N)]
        self.safeGoto(*self.toGraphable(0, initial))
        while True:
            try:
                xn = f(initial)
                break
            except:
                return
        for i in n:
            try:
                self.t.goto(*self.toGraphable(i, xn))
                xn = f(xn)
                self.t.down()
            except:
                return
        self.t.color(self.p_color)

    def graphVectorField(self, fx, fy, step_size=1, x_bounds=False, y_bounds=False):
        if not x_bounds:
            x_bounds=self.x_lim
        if not y_bounds:
            y_bounds=self.y_lim
        xpos = x_bounds[0]
        while xpos <= x_bounds[1]:
            ypos = y_bounds[0]
            while ypos <= y_bounds[1]:
                try:
                    self.safeGoto(*self.toGraphable(xpos, ypos))
                    self.t.circle(1)
                    dx = fx(xpos, ypos)
                    dy = fy(xpos, ypos)
                    mag = math.sqrt(dx**2+dy**2)
                    self.t.color(hls_to_rgb(min(.9, mag/340), .5, 1))
                    self.t.goto(*self.toGraphable(xpos+dx/mag*step_size, ypos+dy/mag*step_size))
                    ypos += step_size
                except:
                    ypos += step_size
                    continue
            xpos+= step_size

    def trapezoid(self, f, b, a, partitions):
        tot = 0
        stepSize = (b-a)/partitions
        for i in range(0, partitions-1):
            tot += (stepSize*(f(a)+f(a+stepSize))/2)
            a += stepSize
        return tot
        
           
    def graphNonLinearTransformation(self, f, g, origin=0, step_size=.1, int_step=.5, der_step=.01):
        xpoints = [self.x_lim[0]+i*step_size for i in range(0, math.ceil((self.x_lim[1]-self.x_lim[0])/step_size))]
        derivative = lambda func, x: (func(x+der_step)-func(x-der_step))/(2*der_step)
        ds = lambda x: math.sqrt(1+derivative(g, x)**2)
        self.graph(g)
        self.t.up()
        for point in xpoints:
            try:
                integ = f(self.trapezoid(ds, point, origin, 1000))
                x = point - integ*derivative(g, point)/math.sqrt(1+derivative(g, point)**2)
                y = g(point) + integ*1/math.sqrt(1+derivative(g, point)**2)
                self.t.goto(*self.toGraphable(x, y))
                self.t.down()
            except:
                self.t.up()
                continue

    def graphScatter(self, y, x=False, col=False):
        if not x:
            x = [i for i in range(0, len(y))]
        
        for i in range(0, len(y)):
            self.safeGoto(*self.toGraphable(x[i], y[i]))
            self.t.circle(1)

    def screenReset(self):
        self.t.clear()
        self.drawAxis()
        
    
if __name__ == "__main__":
    calc = calculator(x_bounds=[-20, 20], y_bounds=[-20, 20], background_color="black", pen_color="white")
    calc.graph(lambda t: 8*math.cos(t), fx = lambda t: 6*math.sin(8*t), step_size = .01, col="red", t_int=[0,2*math.pi])
    input("Hit enter to continue: ")
    calc.screenReset()
    
    calc.graphPolar(lambda t: 10*math.cos(t)+10, step_size=.01)
    input("Hit enter to continue: ")
    
    calc.changeAxis([-1, 200], [-.1, 1])
    calc.graphSequence(lambda x: 4*x*(1-x), .8)
    input("Hit enter to continue: ")
    
    calc.changeAxis([-20, 20], [-20, 20])
    calc.graphVectorField(lambda x, y: -y, lambda x, y: x, step_size=1, x_bounds=[-10, 10], y_bounds=[-10,10])

    input("Hit enter to continue: ")
    calc.screenReset()
    calc.graphNonLinearTransformation(lambda x: 3*math.sin(x/5), lambda x: 3*math.sin(x/5), origin = 0)

    input("Hit enter to continue: ")
    calc.screenReset()
    calc.graphScatter([i for i in range(0, 15)])
        
        
        
        
        
