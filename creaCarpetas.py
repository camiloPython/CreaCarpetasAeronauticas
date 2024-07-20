# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 10:06:27 2017

@author: rvindas
"""

import sys
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
import testPDF2 as tp
import modulo_crea_carpetas2 as mcc
#from datetime.datetime import date
import datetime
import os

ventanaPrincipal = uic.loadUiType("interfazMROC3.ui")[0]
#class ventana(QtWidgets.QMainWindow, ventanaPrincipal):

class ventana(QtWidgets.QMainWindow, ventanaPrincipal):
    
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("IMN-DMSA, Crea Carpetas 2.5")
        self.alto.toggled.connect(self.checkVueloA)
        self.bajo.toggled.connect(self.checkVueloB)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor("#cce6ff"))
        self.setPalette(palette)
        
        #self.actual_18.toggled.connect(self.checkTiempoA)
        #self.actual_12.toggled.connect(self.checkTiempoA)
        #self.actual_6.toggled.connect(self.checkTiempoA)
        #self.actual.toggled.connect(self.checkTiempoB)
        #self.z6.toggled.connect(self.checkZetaA)
        #self.z12.toggled.connect(self.checkZetaB)
        #self.z18.toggled.connect(self.checkZetaC)
        #self.z24.toggled.connect(self.checkZetaD)
        self.crea.clicked.connect(self.creaCarpetas)
        self.descargar.clicked.connect(self.descargaMapas)
        self.spin50.setMinimum(1)
        self.spin100.setMinimum(1)
        self.spin180.setMinimum(1)
        self.spin240.setMinimum(1)
        #self.zygrid.setEnabled(False)
        
        #dia = datetime.date.today()
        dia = datetime.datetime.utcnow()
        hoy = dia.day
        mes = dia.month
        anno = dia.year
       
        #Crear las carpetas necesarias!
        #mcc.creaCarpetas(hoy,mes,anno)
        ruta_directorio = mcc.construyeRutas(hoy,mes,anno,0)
        mcc.creaDirectorios(ruta_directorio)
        ruta_directorio =  ruta_directorio = mcc.construyeRutas(hoy,mes,anno,1)
        mcc.creaDirectorios(ruta_directorio)
        ruta_directorio =  ruta_directorio = mcc.construyeRutas(hoy,mes,anno,2)
        mcc.creaDirectorios(ruta_directorio)
        
        #----Inicio Codigo para colocar valores en el pop up----
        ptr = open("archivos\\vuelos.txt","r")
        lineas = ptr.readlines()
        flies = []
        for linea in lineas:
            lista = linea.split(",")
            flies.append(lista[0])
            flies.sort()
            
        combo = self.vuelos
        model = combo.model()
        for row in flies:
            item = QtGui.QStandardItem(row)
            item.setForeground(QtGui.QColor('black'))
            font = item.font()
            font.setPointSize(10)
            item.setFont(font)
            model.appendRow(item)
            
            
        ptr = open("archivos\\presion-QNH.txt","r")
        lineas = ptr.readlines()
        flies = []
        for linea in lineas[1:]:
            lista = linea.split("\t")
            flies.append(lista[0])
            flies.sort()
            
        combo = self.comboQNH
        model = combo.model()
        for row in flies:
            item = QtGui.QStandardItem(row)
            item.setForeground(QtGui.QColor('black'))
            font = item.font()
            font.setPointSize(10)
            item.setFont(font)
            model.appendRow(item)
            
        combo = self.aeropuerto
        model = combo.model()
        for row in ["Alajuela","Liberia","Pavas","Limón"]:
            item = QtGui.QStandardItem(row)
            item.setForeground(QtGui.QColor('black'))
            font = item.font()
            font.setPointSize(10)
            item.setFont(font)
            model.appendRow(item)    
        #----Fin Codigo para colocar valores en el pop up----
           
           
           
        #---Inicio codigo valores default de checkBoxes----   
        vueloAlto = self.alto
        prev = self.actual_6
        zeta = self.z12
        
        vueloAlto.setChecked(True)
        prev.setChecked(True)
        zeta.setChecked(True)
        #--Fin del codigo para valores default de checkboxes-----        
    

    def descargaMapas(self):
        
        """
        Funcion para el boton de descargar imagenes
        """
        try:
            mcc.descargaTodosLosMapas()
            self.messMapasDescargados()
        
        except IOError:
            self.messErrorInesperado()

        

    
    #-----codigo para desmarcar las casillas al marcar otra-------
    def checkVueloA(self):
        self.bajo.setChecked(False)
        self.zygrid.setChecked(False)
        self.zygrid.setEnabled(False)
        self.spin50.setEnabled(False)
        self.spin100.setEnabled(False)
        self.spin180.setEnabled(False)
        self.spin240.setEnabled(False)
        
        
    def checkVueloB(self):
        self.alto.setChecked(False)
        self.zygrid.setEnabled(True)
        self.zygrid.setChecked(True)
        self.spin50.setEnabled(True)
        self.spin100.setEnabled(True)
        self.spin180.setEnabled(True)
        self.spin240.setEnabled(True)
    

    #def checkTiempoA(self):
    #    self.actual.setChecked(False)
        
    #def checkTiempoB(self):
    #    self.previo.setChecked(False)     
    
                      
    #def checkZetaA(self):
    #    self.z24.setChecked(False)
    #    self.z12.setChecked(False)
    #    self.z18.setChecked(False)
        
    #def checkZetaB(self):
    #    self.z6.setChecked(False)
    #    self.z24.setChecked(False)
    #    self.z18.setChecked(False)
    
    #def checkZetaC(self):
    #    self.z6.setChecked(False)
    #    self.z24.setChecked(False)
    #    self.z12.setChecked(False)
        
    #def checkZetaD(self):
    #    self.z6.setChecked(False)
    #    self.z12.setChecked(False)
    #    self.z18.setChecked(False)    
    #-----Fin del codigo para desmarcar las casillas al marcar otra-------    



    #---Serie de gets para obtener los valores de la ventana----
    """    
    def getValores(self):
        
       
        
        valores = {}
    
        fly = self.vuelos.currentText()
        valores.setdefault("vuelo", str(fly))        
        
        prono = self.pronosticador.text()
        valores.setdefault("pronosticador",str(prono))
        
        number = self.numero.text()
        valores.setdefault("noDocu", str(number))
        
        emi = self.emision.text()
        valores.setdefault("emision", str(emi))
        
        despe = self.despegue.text()
        valores.setdefault("horaDespegue", str(despe))
        
        qnh = self.comboQNH.currentText()
        valores.setdefault("QNH", str(qnh))
        
        dire = self.velocidad.text()
        valores.setdefault("direccion", str(dire))
        
        temp = self.temperatura.text()
        valores.setdefault("temperatura",str(temp))
        
        return valores
        
    """    
    def getValores(self):
        
        valores = []
    
        fly = self.vuelos.currentText()
        valores.append(str(fly))        
        
        prono = self.pronosticador.text()
        valores.append(str(prono))
        
        number = self.numero.text()
        valores.append(str(number))
        
        emi = self.emision.text()
        valores.append(str(emi))
        
        despe = self.despegue.text()
        valores.append(str(despe))
        
        qnh = self.comboQNH.currentText()
        valores.append(str(qnh))
        
        dire = self.velocidad.text()
        valores.append(str(dire))
        
        temp = self.temperatura.text()
        valores.append(str(temp))
        
        comentario = self.sigmet.text()
        valores.append(str(comentario))
        
        return valores



        
    def getEstadoTipoVuelo(self):
        
        vueloBajo = self.bajo.isChecked()
        vueloAlto = self.alto.isChecked()
        #if vueloBajo:
        #    self.zygrid.setEnabled(True)
        estados = [vueloBajo, vueloAlto]
        return estados


    def getEstadoTipoMapaSig(self):
        
        act_18 = self.actual_18.isChecked()
        act_12 = self.actual_12.isChecked()
        act_6 = self.actual_6.isChecked()
        act = self.actual.isChecked()
        estados = [act, act_6, act_12, act_18]
        return estados


    def getEstadoMapaVT(self):
         
        """
        Funcion para obtener las casillas marcadas
        en la interfaz respecto a los mapas de V y T
        """
        
        act_24 = self.z24.isChecked()
        act_18 = self.z18.isChecked()
        act_12 = self.z12.isChecked()
        act_6 = self.z6.isChecked()
        estados = [act_6, act_12, act_18, act_24]
        
        return estados
        
        
    def getEstadoValidez(self):
        
        zeta6 = self.z6.isChecked()
        zeta12 = self.z12.isChecked()
        zeta18 = self.z18.isChecked()
        zeta24 = self.z24.isChecked()
        estados = [zeta6, zeta12, zeta18, zeta24]
        
        return estados                        
    #---Fin de los gets para obtener los valores---        
        

    def presion(self):
                        
        QNH_hPa, QFE_inHg, QFE_hPa = "","",""
        valorExiste = False
        pres = self.comboQNH.currentText()
        pres = str(pres)
        ptr = open("archivos\\presion-QNH.txt","r")
        lineas = ptr.readlines()
        for linea in lineas:
            datos = linea.strip().split("\t")
            if pres in datos:
                valorExiste = True
                QNH_hPa, QFE_inHg, QFE_hPa = datos[1],datos[2],datos[3]
                
        if not valorExiste:
            QNH_hPa, QFE_inHg, QFE_hPa = "NA","NA","NA"
            
        return [pres,QNH_hPa,QFE_inHg,QFE_hPa]    


    def determinaRuta(self):
        
        ruta = ""
        fly = str(self.vuelos.currentText())
        ptr = open("archivos\\vuelos.txt","r")
       
        
        lineas = ptr.readlines()
        for linea in lineas:
            valor = linea.strip().split(",")
            if fly in valor:
                ruta = valor[1] + "-" + valor[2]
            
        return ruta



    def escribeTaf(self):
        fly = str(self.vuelos.currentText())
        mcc.escribeTaf(fly)
        
    
    def rutasZygrid(self):

        rutas = []        
        #mapa50 = "C:\\Users\\rvindas\\Desktop\\codigoMROC\\mapas\\50.jpg"
        mapa50 = "mapas\\50.jpg"
        rutas.append(mapa50)
        
        #mapa100 = "C:\\Users\\rvindas\\Desktop\\codigoMROC\\mapas\\100.jpg"
        mapa100 = "mapas\\100.jpg"
        rutas.append(mapa100)
        
        #mapa180 = "C:\\Users\\rvindas\\Desktop\\codigoMROC\\mapas\\180.jpg"
        mapa180 = "mapas\\180.jpg"
        rutas.append(mapa180)
        
        #mapa240 = "C:\\Users\\rvindas\\Desktop\\codigoMROC\\mapas\\240.jpg"
        mapa240 = "mapas\\240.jpg"
        rutas.append(mapa240)
        
        return rutas
        
    
                
    def mapas(self):
        
        """
        Esta funcion extrae la informacion respecto a los mapas que desea el usuario
        y prepara las rutas para agregar los mismos a la carpeta de vuelo
        [act, act_6, act_12, act_18]        
        """        
        actual_18 = self.getEstadoTipoMapaSig()[3]        
        actual_12 = self.getEstadoTipoMapaSig()[2]
        actual_6 = self.getEstadoTipoMapaSig()[1]
        actual = self.getEstadoTipoMapaSig()[0]
        zeta6 = self.getEstadoMapaVT()[0]
        zeta12 = self.getEstadoMapaVT()[1]
        zeta18 = self.getEstadoMapaVT()[2]
        zeta24 = self.getEstadoMapaVT()[3]
        
        horario = []
        #linkSig = ""
        """
        if actual:
            linkSig = "a"
        
        if actual_6:
            linkSig = "a6"
        
        if actual_12:
            linkSig = "a12"
            
        if actual_18:
            linkSig = "a18"
        """        
            
        if zeta6:
            horario.append("6z")    
            
        if zeta12:
            horario.append("12z")
            
        if zeta18:
            horario.append("18z")    
            
        if zeta24:
            horario.append("24z")
            
        #listaRutaMapas = mcc.descargaMapasATexto(horario, linkSig)
        listaRutaMapas = mcc.rutasDeMapas(horario, actual, actual_6, actual_12, actual_18)    
        return listaRutaMapas
        
           
    def creaCarpetas(self):
        
        try:        
            self.escribeTaf()
            aeropuerto = str(self.aeropuerto.currentText())
            maps = self.mapas()
            fly = str(self.vuelos.currentText())
            ruta = str(self.determinaRuta())
            prono = str(self.pronosticador.text())
            number = str(self.numero.text())
            emi = str(self.emision.text())
            despe = str(self.despegue.text())
            vel = str(self.velocidad.text())
            dire = str(self.direccion.text())
            temp = str(self.temperatura.text())
            pres = str(self.presion()[0])
            QNH_hPa = str(self.presion()[1])
            QFE_inHg = str(self.presion()[2])
            QFE_hPa = str(self.presion()[3])
            
            #print ("-----Rutas mapas de Zygrid---------")
            #print (self.rutasZygrid()[0], self.spin50.value())
            #print (self.rutasZygrid()[1], self.spin100.value())
            #print (self.rutasZygrid()[2], self.spin180.value())
            #print (self.rutasZygrid()[3], self.spin240.value())
            #print ("-----------------------------------")
            
            if self.zygrid.isChecked() == True:
                mapa100 = mcc.convierteGris(self.rutasZygrid()[0], self.spin50.value())
                mapa300 = mcc.convierteGris(self.rutasZygrid()[1], self.spin100.value())
                mapa340 = mcc.convierteGris(self.rutasZygrid()[2], self.spin180.value())
                mapa390 = mcc.convierteGris(self.rutasZygrid()[3], self.spin240.value())
               
                maps.setdefault("z100", mapa100)
                maps.setdefault("z300", mapa300) 
                maps.setdefault("z340", mapa340) 
                maps.setdefault("z390", mapa390) 
            
            
            #else:    
            #    mapa100 = self.mapas()[1]
            #    mapa300 = self.mapas()[2]
            #    mapa340 = self.mapas()[3]
            #    mapa390 = self.mapas()[4]
        
            #mapaSignificante = self.mapas()[0]
            #dia = datetime.date.today()
            maps.setdefault("mapaPavas","mapas\\mapaPavas.jpg")
            dia = datetime.datetime.utcnow()
            hoy = dia.day
            mes = dia.month
            anno = dia.year

            #print "-------------llaves ----------------------"            
            #print maps.keys()
            #print "------------------------------------------"
            
            meses = {1:"Ene.",2:"Feb.",3:"Mar.",4:"Abr.",5:"May.",6:"Jun.",7:"Jul.",
                 8:"Ago.",9:"Sep.",10:"Oct.",11:"Nov.",12:"Dic."}
                 
            fecha = "%d %s %d"%(hoy, meses[mes],anno)    
        
            #directorioDia = "C:\\Users\\rvindas\\Desktop\\camilo\\proyectosIMN\\interfazIntento2\\vuelos_%d_%d_%d\\"%(hoy,mes,anno)
            directorioDia = mcc.construyeRutas(hoy,mes,anno,2) + "\\"
            if self.alto.isChecked() == True:
                tp.creaCarpeta(fly,ruta,emi,prono,fecha,number,despe,dire,QFE_hPa,QNH_hPa,temp,vel,QFE_inHg,pres,maps,directorioDia,aeropuerto)
                self.messCarpetaCreada()
            else:
                #tp.creaCarpeta(fly,ruta,emi,prono,fecha,number,despe,dire,QFE_hPa,QNH_hPa,temp,vel,QFE_inHg,pres,mapa100,mapa300,mapa340,mapa390,directorioDia,vueloAlto = False)
                tp.creaCarpeta(fly,ruta,emi,prono,fecha,number,despe,dire,QFE_hPa,QNH_hPa,temp,vel,QFE_inHg,pres,maps,directorioDia,aeropuerto, vueloAlto = False)                
                self.messCarpetaCreada()

        except IOError as err:

            if err.errno == 13:
                self.messErrorPDF()


            elif err.errno == 2:
                #e_type, e_object, e_traceback = sys.exc_info()
                #e_line_number = e_traceback.tb_lineno
                #e_filename = os.path.split(
                #    e_traceback.tb_frame.f_code.co_filename
                #    )[1]

                e_message = str(err)

                #e_line_number = e_traceback.tb_lineno

                #a = f'exception type: {e_type}'

                #b = f'exception filename: {e_filename}'

                #c = f'exception line number: {e_line_number}'

                d = f'exception message: {e_message}'               
                self.messErrorArchivos(d)
                
            else:
                #print type(err.errno)
                #print err.errno
                #print err
                self.messErrorInesperado()
                
        except IndexError as err:
            self.messErrorCasillas()
            
            
                
    def messErrorPDF(self):
        msgBox = QtWidgets.QMessageBox() 
        msgBox.setWindowTitle("Error!")
        msgBox.setText("A ocurrido un error durante la ejecucion del programa")
        msgBox.setDetailedText("Tiene la carpeta de vuelo abierta, cierre el documento para poder sobreescribirlo")
        msgBox.exec_()        
                                            

    def messErrorArchivos(self,d):
        msgBox = QtWidgets.QMessageBox()
        #msgBox.setWindowFlags(Qt::CustomizeWindowHint | Qt::WindowTitleHint)
        msgBox.setWindowTitle("Error!")
        msgBox.setText("A ocurrido un error durante la ejecucion del programa")
        #msgBox.setDetailedText("Es posible que el mapa de pavas, los mapas de Zygrid y/o el archivo vuelos no se encuentra en la ruta especificada. Si los archivo estan en las carpetas correctas entonces el error puede ser por problemas de conexion a internet")
        msgBox.setDetailedText(d)
        
        msgBox.exec_()                  
                
                       
    def messErrorInesperado(self):
        msgBox = QtWidgets.QMessageBox() 
        msgBox.setWindowTitle("Error!")
        msgBox.setText("A ocurrido un error durante la ejecucion del programa")
        msgBox.setDetailedText("A ocurrido un error de origen desconocido, comuniquese son el desarrollador rvindas@imn.ac.cr")
        msgBox.exec_()


    def messCarpetaCreada(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Proceso exitoso!")
        msgBox.setText("La carpeta se ha creado correctamente!")
        #msgBox.setDetailedText("A ocurrido un error de origen desconocido, comuniquese son el desarrollador rvindas@imn.ac.cr")
        msgBox.exec_()


    def messErrorCasillas(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Error!")
        msgBox.setText("Asegurese que todas las casillas necesarias esten marcadas")
        #msgBox.setDetailedText("A ocurrido un error de origen desconocido, comuniquese son el desarrollador rvindas@imn.ac.cr")
        msgBox.exec_()


    def messMapasDescargados(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Proceso exitoso!")
        msgBox.setText("Los mapas se han descargado correctamente!")
        #msgBox.setDetailedText("A ocurrido un error de origen desconocido, comuniquese son el desarrollador rvindas@imn.ac.cr")
        msgBox.exec_()                  
                          
        
        
        
app = QtWidgets.QApplication(sys.argv)
miVentana = ventana(None)
miVentana.show()
app.exec_()

#print"................Variables de la Carpeta de Vuelo.................."
#print miVentana.getValores(), miVentana.getEstadoTipoVuelo(), miVentana.presion() 
#print ".-................................................................"
                        