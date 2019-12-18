#! /usr/bin/env python
from constraint import *

problem = Problem()

#Variables
#Variables duplicadas para las dos horas semanales que pueden ser dadas, salvo educacion fisica que solo tiene 1 hora semanal asignada. Pueden tomar el
#valor de 0 a 11, que significa los dias de la semana y sus horas (0 es lunes a las 9, 1 es lunes a las 10, 2 es lunes a las 11, 3 es martes a las 9... asi sucesivamente
#hasta el jueves a las 10, que es la ultima hora disponible
#La restriccion 2 se cumple al definir las variables de esta forma porque nos aseguramos que hay 2 horas de cada asignatura
problem.addVariables(['CN1', 'CN2', 'CS1', 'CS2', 'LC1', 'LC2', 'I1', 'I2', 'EF', 'MT1', 'MT2'], range(11))

#Variables duplicadas para los profesores, puesto que cada profesor puede dar dos clases semanales.
#Pueden tomar los valores de las asignaturas. Al poder poner los nombres, en la ejecucion es mas facil identificar que asignatura da cada profesor
problem.addVariables(['A1', 'A2', 'J1', 'J2', 'L1', 'L2'], ['C.Naturales', 'C.Sociales', 'Lenguaje', 'Ingles', 'E.Fisica', 'Matematicas'])

#Restricciones

#Restriccion 1: La duracion de cada clase es de una hora y solo se puede impartir una materia
problem.addConstraint(AllDifferentConstraint(), ['CN1', 'CN2', 'CS1', 'CS2', 'LC1', 'LC2', 'I1', 'I2', 'EF', 'MT1', 'MT2'])

#Restriccion 3: C.Naturales debe impartirse de forma consecutiva el dia que se le asigne.

def cn_hours(a, b): #Funcion para comprobar que C.Naturales se asigna en dos horas consecutivas y que la primera de ellas no coincide en la ultima hora
	return a==b-1 and a!=2 and a!=5 and a!=8

problem.addConstraint(cn_hours, ('CN1', 'CN2'))

#Restriccion 4: Matematicas no puede impartirse el mismo dia que C.Naturales e Ingles

def dif_days(a, b, c, d, e): #Funcion para comprobar que cada dia no coincide matematicas con naturales e ingles
	if(a == 0 or a == 1 or a == 2):
		return b!=0 and b!=1 and b!=2 and c!=0 and c!=1 and c!=2 and d!=0 and d!=1 and d!=2 and e!=0 and e!=1 and e!=2
	elif(a == 3 or a == 4 or a == 5):
		return b!=3 and b!=4 and b!=5 and c!=3 and c!= 4 and c!=5 and d!=3 and d!=4 and d!=5 and e!=3 and e!=4 and e!=5
	elif(a == 6 or a == 7 or a == 8):
		return b!=6 and b!=7 and b!= 8 and c!=6 and c!=7 and c!=8 and d!=6 and d!=7 and d!=8 and e!=6 and e!=7 and e!= 8
	elif(a == 9 or a == 10):
		return b!=9 and b!=10 and c!=9 and c!=10 and e!=9 and e!=10

#Dos addConstraint para diferenciar una hora de matematicas con la otra
problem.addConstraint(dif_days, ('MT1', 'CN1', 'I1', 'CN2', 'I2'))
problem.addConstraint(dif_days, ('MT2', 'CN1', 'I1', 'CN2', 'I2'))

#Restriccion 5: Matematicas debe impartirse en las primeras horas y sociales en las ultimas.

#Las restricciones las anyadimos directamente con inSetConstraint para delimitar las horas a las que puede asignarse cada asignatura
problem.addConstraint(InSetConstraint([0, 3, 6, 9]), ['MT1'])
problem.addConstraint(InSetConstraint([0, 3, 6, 9]), ['MT2'])
problem.addConstraint(InSetConstraint([2, 5, 8, 10]), ['CS1']) #Poner un 10 para considerar el caso de jueves a ultima hora. Si no se pone salen 78336 soluciones.
problem.addConstraint(InSetConstraint([2, 5, 8, 10]), ['CS2'])

#Restriccion 6: Cada profesor debe impartir 2 asignaturas y deben ser distintas entre ellos

#Poniendo que todos los slots asignados a cada profesor (2) se cumple
problem.addConstraint(AllDifferentConstraint(), ['A1', 'A2', 'J1', 'J2', 'L1', 'L2'])

#Restriccion 7: Lucia se encargara de C.Sociales si Andrea se encarga de E.Fisica

#Si Lucia se encarga de Sociales, Andrea se dedicara a E. Fisica
def ef_cs_profesores (a, b, c, d):
	return c=='E.Fisica' or d=='E.Fisica' if(a=='C.Sociales') or (b=='C.Sociales') else None

problem.addConstraint(ef_cs_profesores, ('L1', 'L2', 'A1', 'A2'))

#Restriccion 8: Juan no se encargara de naturales o sociales si se dan a primera hora los lunes y los jueves

#Si alguna hora de sociales o naturales se dan a primera hora de lunes o jueves (0 y 9), no se le asignara a juan esas asignaturas
def cn_cs_profesores (a, b, c, d):
	return a!='C.Naturales' if(b == 0 or b == 9) else None
	return a!= 'C.Sociales' if (c == 0 or c == 9 or d == 0 or d == 9) else None

problem.addConstraint(cn_cs_profesores, ('J1', 'CN1', 'CS1', 'CS2'))
problem.addConstraint(cn_cs_profesores, ('J2', 'CN1', 'CS1', 'CS2'))

print(len(problem.getSolutions()))
print(problem.getSolution())
#print(problem.getSolutions()[12000])
#print(problem.getSolutions()[60000])
#print(problem.getSolutions())
