##!/usr/bin/python
#-*- coding: UTF8 -*-
##Programa para calcular Un circuito oscilador RF conectado a una antena. 
##Copyright (c) 2010 Rafael Ortiz Johao Cuervo .
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:

##The above copyright notice and this permission notice shall be included in
##all copies or substantial portions of the Software.

##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
##THE SOFTWARE.

##Introduccion de parametros o variables

import sys, os 
import math 
import decimal #no se usa
import pygtk
import gtk



# This function will be called whenever you click on your button:
def click_handler(widget) :
    # quit the application:
    gtk.main_quit()

# Create the main window:
win = gtk.Window()

# Organize widgets in a vertical box:
vbox = gtk.VBox()
win.add(vbox)

# Create an area to draw in:
drawing_area = gtk.DrawingArea()
drawing_area.set_size_request(600, 400)
vbox.pack_start(drawing_area)
drawing_area.show()


# Make a pushbutton:
button = gtk.Button("Calcular")

# When it's clicked, call our handler:
button.connect("clicked", click_handler)

# Add it to the window:
vbox.pack_start(button)
button.show()

# Obey the window manager quit signal:
win.connect("destroy", gtk.main_quit)




vbox.show()
win.show()
gtk.main()


#inicia calculo 

print 'Introduzca los parametros de la antena'
vars1 = float(raw_input("Introduzca S11: "))
vars5 = float(raw_input("Introduzca Angulo  S11: "))
vars2 = float(raw_input("Introduzca  S12: "))
vars6 = float(raw_input("Introduzca Angulo  S12: "))
vars3 = float(raw_input("Introduca S21: "))
vars7 = float(raw_input("Introduca Angulo  S21: "))
vars4 = float(raw_input("Introduca S22: "))
vars8 = float(raw_input("Introduca Angulo  S22: "))

print "Usted escogio |S11| ", vars1
print "Usted escogio |S12| ", vars2
print "Usted escogio |S21| ", vars3
print "Usted escogio |S22| ", vars4
print "Usted escogio Angulo S11 ", vars5
print "Usted escogio Angulo S12 ", vars6
print "Usted escogio Angulo S21 ", vars7
print "Usted escogio Angulo S22 ", vars8

vars5rad = vars5*57.295779   #conversion a radianes. 
vars6rad = vars6*57.295779
vars7rad = vars7*57.295779  #conversion a radianes. 
vars8rad = vars8*57.295779 

##Calculo de estabilidad   
#DSc = S11*S22 − S12*S21 calculo DS complejo

DSCM1 = vars1*vars4 #calculo Magnitud DSC
DSCM2 = vars2*vars3   #calculo Magnitud DSC

DSCA1 = vars5rad + vars8rad #calculo Angulo 
DSCA2 = vars6rad + vars7rad #calculo Angulo

#Conversion a rectangular para resta. 
PR1= DSCM1*math.cos(DSCA1) #parte real1 raiZ!!!! x
PP1= DSCM1*math.sin(DSCA1) #parte polar1 y

PR2 = DSCM2*math.cos(DSCA2) #parte real2 x1
PP2 = DSCM2*math.sin(DSCA2) #parte polar2 y1

#calculo parametro DS complejo.

DSs1 = PR1 - PR2 #Resta Reales                                               
DSs2 = PP1 - PP2 #Resta angulos

#Calculo de polar a rectangular

R1 = math.sqrt((DSs1*DSs1) + (DSs2*DSs2)) #parte real de la resta que equivale a DS 

#k=    1 + (DS)2 − |S11 |2 − |S22 |2 / 2 * |S21 | * |S12 |  Ecuacion de K. 

K = ((1.0 + (R1*R1) - (vars1*vars1) - (vars4*vars4))/(2.0*vars3*vars2))                  

print 'Para estos valores la estabilidad K es igual a: %f'%K

#MAG= 10LOG|VARS|+10LOG
MAG  = (10*math.log10(vars3/vars5))+(10*math.log10(K-math.sqrt((K*K)-1)))

print  'Para estos valores la MAG es igual a: %f'%MAG

if K > 1: #evaluacion de estabilidad o inestabilidad. 
   
# print 'ciclo'                                                   
#       C2 = S22 − (DS * S11 )  Evaluacion de factor C2

   C2R = R1 

#       B2 = 1 + |S22 |2 − |S11 |2 − |DS |2 Evaluacion de factor B2

                  
   B2= (1.0 + (vars4*vars4) - (vars1*vars1) - (R1*R1))
                         
   print "El coeficiente B2 es: %f"%B2

#Magnitud coeficiente de reflexion hacia la carga           |TL| =  (B2 ± sqrt(B2 − 4|C2 |2))/(2*|C2|)                  

#   TL1 =  (B2 + math.sqrt((B2*B2) - 4*(R1*R1)))/(2*R1)
   TL1 =  (B2 + math.sqrt((B2*B2) - 4*(R1*R1)))/(2*R1)
                          
#TS =  

#Salida al Usuario 

  # print "Puede Utilizar alguno de estos dos valores para TL"
   print "El coeficiente de reflexion hacia la carga (1) es: %f"%TL1
  # print "El coeficiente de reflexion hacia la carga (2) es: %f"%TL2


#print "El coeficiente de reflexion hacia la fuente es: ", TS

#Input del arco

   vars9 = float(raw_input("Introduzca ARCO AB: "))
   vars10 = float(raw_input("Introduzca ARCO BC: ")) 
   frec = float(raw_input("Introduzca Frecuencia de trabajo en MHZ: "))

#salida

   C =   vars9 / (2*math.pi*frec*50000000)                              #C para ocilacion. 50 es el coef de normalizacion  
   L =   vars10*50 / (2*3.1415*frec*1000000)                             #L para la ocilacion

#Salida al usuario 

   print "La capacitancia para su circuito es: %f pf"%C
   print "La inductancia para su circuito es: %f nH"%L

else: print  "Su configuracion no es estable pruebe con otros valores."

 






