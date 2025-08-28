from sympy import *
import random
from sympy.abc import x,y,u
init_printing(use_latex="mathjax")

#datos de entrada
#formula de la funcion
limite_inferior=0
limite_superior=2
x_recibido=4
y_recibido=5
iteraciones=10000

#calcular la funcion de densidad conjunta
f = Rational(1,28)*(2*x + 3*y + 2)

#marginal de x
f1 = integrate(f, (x, limite_inferior, limite_superior))
print("f_1(x) : ",f1)          

#marginal de y
f2 = integrate(f, (y, limite_inferior, limite_superior))
print("f_2(y) : ",f2)          

fx_y=simplify(f/f1)
fy_x=simplify(f/f2)

#generamos funciones de densidad condicional
print("\nf(x|y) \n",f/f1," \n = ", fx_y)
print("\nf(y|x) \n",f/f2,"\n = ",fy_x)

#generamos funciones de densidad acumulada
Fx_y=integrate(fx_y,(x,limite_inferior,x))
Fy_x=integrate(fy_x,(y,limite_inferior,y))  
print("\nF(x|y) \n",Fx_y)
print("\nF(y|x) \n",Fy_x)

#igual respecto a u las funciones 
ecuacion_u=Eq(u,Fx_y)
ecuacion_v=Eq(u,Fy_x)

#despejar f(x|y_0) y f(y|x_0)
f_x_i=solve(ecuacion_u,x)[1] #[0] es para tomar el valor positivo
f_y_i=solve(ecuacion_v,y)[1] #[0] es para tomar el valor positivo
print("\n x","1 :",f_x_i)
print("y","1 :",f_y_i)

puntos_x=[x_recibido]
puntos_y=[y_recibido]
for cont in range(iteraciones):
    #print("\nResultados de la iteracion ",cont+1)
    r1=random.uniform(0, 1)
    r2=random.uniform(0, 1)
    #print("Valor de rand : ",r)
    #print("Valores actuales : x :",x_recibido," y :",y_recibido)
    x_i=f_x_i.subs({y: y_recibido, u: r1})
    y_i=f_y_i.subs({x: x_recibido, u: r2})

    #print("x",cont+1," :", x_i)
    #print("y",cont+1," :", y_i)
    
    x_recibido=x_i
    y_recibido=y_i
    puntos_x.append(x_recibido)
    puntos_y.append(y_recibido)

#print("\nPuntos x : ",puntos_x)
#print("Puntos y : ",puntos_y)

