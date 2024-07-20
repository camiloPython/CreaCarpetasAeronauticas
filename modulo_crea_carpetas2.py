# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 09:28:41 2016

@author: rvindas


Modulo para distintas funciones relacionadas con la interfaz grafica de crea carpetas.
"""


#import datetime 
import os



import urllib.request as urllib
#import html2text
from PIL import Image
from PIL import ImageEnhance

import ssl

"""
dia = datetime.date.today()
hoy = dia.day
mes = dia.month
anno = dia.year

meses = {1:"Ene.",2:"Feb.",3:"Mar.",4:"Abr.",5:"May.",6:"Jun.",7:"Jul.",
                 8:"Ago.",9:"Sep.",10:"Oct.",11:"Nov.",12:"Dic."}
                 
fecha = "%d %s %d"%(hoy, meses[mes],anno)
"""
"""
@retry(IOError, tries=4, delay=3, backoff=2)
def descargaMapas(link, mapa):
    urllib.urlretrieve(link, mapa)
"""    
    

def creaDirectorios(ruta_directorio):
    
    """ Funcion que crea directorios cada dia -si no existen- para guardar las carpetas 
    de los vuelos """ 
    
    if not (os.path.exists(ruta_directorio)):
        #print ("-----Directorios no exiten previamente..... Creando directorios...")
        os.mkdir(ruta_directorio)
        return (ruta_directorio)
        
    else:    
        return (ruta_directorio)                     



def construyeRutas(dia,mes,anno,numeroRuta):
    
    meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
             9:"Setiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
             
    mes_str = meses[mes]
    
    ruta_directorio = ""
    
    if numeroRuta == 0:
        ruta_directorio = "carpetasDeVuelos\\carpetas_%d\\"%(anno)
           
    if numeroRuta == 1:
        ruta_directorio = "carpetasDeVuelos\\carpetas_%d\\%s\\"%(anno,mes_str)
        
    if numeroRuta == 2:
         #uta_directorio = "carpetasDeVuelos\\carpetas_%d\\%s\\vuelos_%d_%d_%d"%(anno,mes_str,hoy,mes,anno)
         ruta_directorio = "carpetasDeVuelos\\carpetas_%d\\%s\\vuelos_%d_%d_%d"%(anno,mes_str,dia,mes,anno)
         
    return ruta_directorio    


    


def convierteGris(imagen, factor):
    
    """Esta funcion recibe la direccion de una imagen 
    y la convierte en una con solo tonos de blancos y negros.
    Esta pensada para convertir los mapas de colores de viento y
    temperatura para las carpetas de vuelos bajos.
    El parametro factor indica el grado de contraste en la imagen, el default 1
    es para mapas claros como el amarillo de 50.
    Para los mapas mas oscuros como el azul de 240 se necesita un factor de 60"""    
    
   
    nombre = imagen.replace(".jpg", "GRIS.jpg")
    img = Image.open(imagen)
    img = img.convert("L")
    contraste = ImageEnhance.Contrast(img)
    img = contraste.enhance(factor)
    img.save(nombre)
    img.close()
    
    return nombre

      
def escribeTaf(vuelo):
    
    """Funcion que recibe un codigo que indica el vuelo, busca ese vuelo 
    en el archivo vuelos.txt y si lo encuentra genera el url del taf para dicho
    vuelo para escribirlo en un archivo de texto.
    La funcion regresa una lista con la primera entrada un boleano ->True si encuentra el codigo del vuelo en la lista, caso contrario
    regresa False. La 2da entrada el codigo de vuelo, la tercera la salida (MROC) y la cuarta entrada el destino."""

    ruta = "archivos\\vuelos.txt"
    vuelos = open(ruta,"r")
    lista_vuelos = vuelos.readlines()#lista que contiene los datos de los vuelos
    vuelos.close()
    SIestaNOesta = False
    salida = ""
    destino = ""
    valores = []
    valores.append(SIestaNOesta)
    valores.append(vuelo)
    valores.append(salida)
    valores.append(destino)
    #mensaje = "Buscando el vuelo %s en la lista y descargando los datos de www.aviationweather.gov..."%(vuelo)
    
    for linea in lista_vuelos:
        codigo_vuelo = linea.split(",")[0]
        
        
        if vuelo.lower() == codigo_vuelo.lower():
            valores = []
            salida = linea.split(",")[1]
            destino = linea.split(",")[2]
            aeropuertos = linea.strip().split(",")[1:]
            separador = aeropuertos[0] + "%2C"
            SIestaNOesta= True
            valores.append(SIestaNOesta)
            valores.append(codigo_vuelo)
            valores.append(salida)
            valores.append(destino)
            
            #print ("*****************************************************")
            #print (aeropuertos)
            #print (aeropuertos[1:-1])
            #print ("*****************************************************")
           
            #for aeropuerto in aeropuertos[1:-1]:
            for aeropuerto in aeropuertos[1:-1]:    
                #aero = aeropuerto + "%20"
                aero = aeropuerto + "%2C"
                separador += aero
                print (separador)
                 
            separador += aeropuertos[-1]
            
            #linkParte1 = "https://www.aviationweather.gov/taf/data?ids=" 
            #linkParte3 = "&format=raw&hours=0&taf=off&layout=off&date=0" 
            
            #cambios en la página de ADDS
            #https://aviationweather.gov/cgi-bin/data/taf.php?ids=MROC%2CMRPV%2CMRLM&sep=true
            #https://aviationweather.gov/cgi-bin/data/taf.php?ids=MROC%2CMRPV%2CMRLB&sep=true
            #https://aviationweather.gov/data/metar/?id=MROC,MRLB,MRPV&hours=6&include_taf=yes
            #https://aviationweather.gov/cgi-bin/data/metar.php?ids=MROC%2CMRLB%2CMRPV&hours=6&order=id%2C-obs&sep=true&taf=true
            linkParte1 = "https://aviationweather.gov/cgi-bin/data/taf.php?ids=" 
            linkParte3 = "&sep=true" 
            link = linkParte1 + separador + linkParte3
            print (link)
            
            #print "link del taf:"
            #print link
            #print "----------------------------"
            
            # AGREGADO
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE            
            
            urllib.urlretrieve(link,"archivos\\taf.txt")
            #html = open("archivos\\taf.txt").read()
            #texto = html2text.html2text(html)
            tafAlternos = "tafAeropuertosAlternos\\tafAlternos_%s.txt"%(vuelo)
            tafVuelos = open(tafAlternos,"w")
            #modificacion debido a cambios en pagina de ADDS 17/10/2023
            taf = open("archivos\\taf.txt", "r")
            texto = taf.read()
            taf.close()
            tafVuelos.write(texto)
            tafVuelos.close()
                
       
    return valores    


"""   
def descargaMapasATexto(horario, linkSig):

    

    mapas = []
    if linkSig == "a":    
        linkMapaPrincipal = "http://www.aviationweather.gov/data/iffdp/2129.gif"
    else:
        linkMapaPrincipal = "http://www.aviationweather.gov/data/iffdp/3129.gif"
        
    
    
    mapa1 = "mapas\\tiempoSIg.gif"
    urllib.urlretrieve(linkMapaPrincipal,mapa1)
    mapas.append(mapa1)
    
    
    if horario == "6z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2300.gif"
        mapa2 = "mapas\\FL390-6z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2301.gif"
        mapa3 = "mapas\\FL340-6z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2302.gif"
        mapa4 = "mapas\\FL300-6z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2305.gif"
        mapa5 = "mapas\\FL100-6z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
        
    if horario == "12z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2310.gif"
        mapa2 = "mapas\\FL390-12z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2311.gif"
        mapa3 = "mapas\\FL340-12z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2312.gif"
        mapa4 = "mapas\\FL300-12z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2315.gif"
        mapa5 = "mapas\\FL100-12z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
                


    if horario == "18z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2320.gif"
        mapa2 = "mapas\\FL390-18z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2321.gif"
        mapa3 = "mapas\\FL340-18z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2322.gif"
        mapa4 = "mapas\\FL300-18z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2325.gif"
        mapa5 = "mapas\\FL100-18z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)

                
    if horario == "24z":
           
        FL390 = "http://www.aviationweather.gov/data/iffdp/2330.gif"
        mapa2 = "mapas\\FL390-24z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2331.gif"
        mapa3 = "mapas\\FL340-24z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2332.gif"
        mapa4 = "mapas\\FL300-24z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
                
        FL100 = "http://www.aviationweather.gov/data/iffdp/2335.gif"
        mapa5 = "mapas\\FL100-24z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
                                     
    return mapas            

"""           
def descargaMapasATexto(horario, linkSig):

    # AGREGADO
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE    
    
    mapas = []
    if linkSig == "a":    
        linkMapaPrincipal = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_0000.png"
    else:
        linkMapaPrincipal = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_0600.png"
        
    #AGREGADO
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE    
    
    mapa1 = "mapas\\tiempoSIg.gif"
    urllib.urlretrieve(linkMapaPrincipal,mapa1)
    mapas.append(mapa1)
    
    
    if horario == "6z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2300.gif"
        mapa2 = "mapas\\FL390-6z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2301.gif"
        mapa3 = "mapas\\FL340-6z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2302.gif"
        mapa4 = "mapas\\FL300-6z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2305.gif"
        mapa5 = "mapas\\FL100-6z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
        
    if horario == "12z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2310.gif"
        mapa2 = "mapas\\FL390-12z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2311.gif"
        mapa3 = "mapas\\FL340-12z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2312.gif"
        mapa4 = "mapas\\FL300-12z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2315.gif"
        mapa5 = "mapas\\FL100-12z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
                


    if horario == "18z":
        FL390 = "http://www.aviationweather.gov/data/iffdp/2320.gif"
        mapa2 = "mapas\\FL390-18z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2321.gif"
        mapa3 = "mapas\\FL340-18z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2322.gif"
        mapa4 = "mapas\\FL300-18z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
        
        FL100 = "http://www.aviationweather.gov/data/iffdp/2325.gif"
        mapa5 = "mapas\\FL100-18z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)

                
    if horario == "24z":
           
        FL390 = "http://www.aviationweather.gov/data/iffdp/2330.gif"
        mapa2 = "mapas\\FL390-24z.gif"
        urllib.urlretrieve(FL390,mapa2)
        mapas.append(mapa2)
                
        FL340 = "http://www.aviationweather.gov/data/iffdp/2331.gif"
        mapa3 = "mapas\\FL340-24z.gif"
        urllib.urlretrieve(FL340,mapa3)
        mapas.append(mapa3)
                
        FL300 = "http://www.aviationweather.gov/data/iffdp/2332.gif"
        mapa4 = "mapas\\FL300-24z.gif"
        urllib.urlretrieve(FL300,mapa4)
        mapas.append(mapa4)
                
        FL100 = "http://www.aviationweather.gov/data/iffdp/2335.gif"
        mapa5 = "mapas\\FL100-24z.gif"
        urllib.urlretrieve(FL100,mapa5)
        mapas.append(mapa5)
                                     
    return mapas            




def descargaTodosLosMapas():
    
    """
    Esta funcion descarga todos los mapas relacionados con las carpetas
    """

    # AGREGADO
    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #ctx.verify_mode = ssl.CERT_NONE    
    
    #mapas = []
    #if linkSig == "a":    
    #linkMapaPrincipal1 = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_0000.png"
    linkMapaPrincipal1 = "https://aviationweather.gov/data/products/swh/00_sigwx_hi_a.gif"
    #else:
    #linkMapaPrincipal2 = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_0600.png"
    #linkMapaPrincipal3 = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_1200.png"
    #linkMapaPrincipal4 = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=0&syol=PGEE07_1800.png"
    
    linkMapaPrincipal2 = "https://aviationweather.gov/data/products/swh/06_sigwx_hi_a.gif"
    linkMapaPrincipal3 = "https://aviationweather.gov/data/products/swh/12_sigwx_hi_a.gif"
    linkMapaPrincipal4 = "https://aviationweather.gov/data/products/swh/18_sigwx_hi_a.gif"
        
        
    #AGREGADO
    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #ctx.verify_mode = ssl.CERT_NONE    
    
    mapa1 = "mapas\\tiempoSigActual.gif"
    urllib.urlretrieve(linkMapaPrincipal1,mapa1)
    
    mapa1 = "mapas\\tiempoSigPrevio.gif"
    urllib.urlretrieve(linkMapaPrincipal2,mapa1)
    
    mapa1 = "mapas\\tiempoSigPrePrevio.gif"
    urllib.urlretrieve(linkMapaPrincipal3,mapa1)
    
    mapa1 = "mapas\\tiempoSigPrePrePrevio.gif"
    urllib.urlretrieve(linkMapaPrincipal4,mapa1)
    #mapas.append(mapa1)
    
    
    #if horario == "6z":
    FL390 = "https://aviationweather.gov/data/products/fax/F06_wind_390_a.gif"
    mapa2 = "mapas\\FL390-6z.gif"
    urllib.urlretrieve(FL390,mapa2)
    #mapas.append(mapa2)
                
    FL340 = "https://aviationweather.gov/data/products/fax/F06_wind_340_a.gif"
    mapa3 = "mapas\\FL340-6z.gif"
    urllib.urlretrieve(FL340,mapa3)
    #mapas.append(mapa3)
                
    FL300 = "https://aviationweather.gov/data/products/fax/F06_wind_300_a.gif"
    mapa4 = "mapas\\FL300-6z.gif"
    urllib.urlretrieve(FL300,mapa4)
    #mapas.append(mapa4)
        
    FL100 = "https://aviationweather.gov/data/products/fax/F06_wind_100_a.gif"
    mapa5 = "mapas\\FL100-6z.gif"
    urllib.urlretrieve(FL100,mapa5)
    #mapas.append(mapa5)
        
    #if horario == "12z":
    FL390 = "https://aviationweather.gov/data/products/fax/F12_wind_390_a.gif"
    mapa2 = "mapas\\FL390-12z.gif"
    urllib.urlretrieve(FL390,mapa2)
    #mapas.append(mapa2)
                
    FL340 = "https://aviationweather.gov/data/products/fax/F12_wind_340_a.gif"
    mapa3 = "mapas\\FL340-12z.gif"
    urllib.urlretrieve(FL340,mapa3)
    #mapas.append(mapa3)
                
    FL300 = "https://aviationweather.gov/data/products/fax/F12_wind_300_a.gif"
    mapa4 = "mapas\\FL300-12z.gif"
    urllib.urlretrieve(FL300,mapa4)
    #mapas.append(mapa4)
        
    FL100 = "https://aviationweather.gov/data/products/fax/F12_wind_100_a.gif"
    mapa5 = "mapas\\FL100-12z.gif"
    urllib.urlretrieve(FL100,mapa5)
    #mapas.append(mapa5)
                
    #if horario == "18z":
    FL390 = "https://aviationweather.gov/data/products/fax/F18_wind_390_a.gif"
    mapa2 = "mapas\\FL390-18z.gif"
    urllib.urlretrieve(FL390,mapa2)
    #mapas.append(mapa2)
                
    FL340 = "https://aviationweather.gov/data/products/fax/F18_wind_340_a.gif"
    mapa3 = "mapas\\FL340-18z.gif"
    urllib.urlretrieve(FL340,mapa3)
    #mapas.append(mapa3)
                
    FL300 = "https://aviationweather.gov/data/products/fax/F18_wind_300_a.gif"
    mapa4 = "mapas\\FL300-18z.gif"
    urllib.urlretrieve(FL300,mapa4)
    #mapas.append(mapa4)
        
    FL100 = "https://aviationweather.gov/data/products/fax/F18_wind_100_a.gif"
    mapa5 = "mapas\\FL100-18z.gif"
    urllib.urlretrieve(FL100,mapa5)
    #mapas.append(mapa5)

                
    #if horario == "24z":
           
    FL390 = "https://aviationweather.gov/data/products/fax/F24_wind_390_a.gif"
    mapa2 = "mapas\\FL390-24z.gif"
    urllib.urlretrieve(FL390,mapa2)
    #mapas.append(mapa2)
                
    FL340 = "https://aviationweather.gov/data/products/fax/F24_wind_340_a.gif"
    mapa3 = "mapas\\FL340-24z.gif"
    urllib.urlretrieve(FL340,mapa3)
    #mapas.append(mapa3)
                
    FL300 = "https://aviationweather.gov/data/products/fax/F24_wind_300_a.gif"
    mapa4 = "mapas\\FL300-24z.gif"
    urllib.urlretrieve(FL300,mapa4)
    #mapas.append(mapa4)
                
    FL100 = "https://aviationweather.gov/data/products/fax/F24_wind_100_a.gif"
    mapa5 = "mapas\\FL100-24z.gif"
    urllib.urlretrieve(FL100,mapa5)
    
    linkIRCA = "https://www.imn.ac.cr/imagenes-sat/IRCA.png"
    imagenIRCA = "mapas\\IRCA.png"
    urllib.urlretrieve(linkIRCA,imagenIRCA)
    #mapas.append(mapa5)
    
    #print "Mapas descargados!!"                                 
    #return mapas            



def rutasDeMapas(horario, actual, actual_6, actual_12, actual_18):
    
    """ 
    Esta funcion regresa los nombres de las rutas de los mapas segun sea la eleccion del usuario    
    """
    
    
    mapas = {}
    
    if actual:
        mapas.setdefault("actual","mapas\\tiempoSigActual.gif")
    if actual_6:
        mapas.setdefault("actual_6","mapas\\tiempoSigPrevio.gif")
    if actual_12:
        mapas.setdefault("actual_12","mapas\\tiempoSigPrePrevio.gif")
    if actual_18:
        mapas.setdefault("actual_18","mapas\\tiempoSigPrePrePrevio.gif")    
    #print horario
    if len(horario) != 0:
        for hora in horario:
            mapas.setdefault("390_%s"%(hora),"mapas\\FL390-%s.gif"%(hora))
            mapas.setdefault("340_%s"%(hora),"mapas\\FL340-%s.gif"%(hora))
            mapas.setdefault("300_%s"%(hora),"mapas\\FL300-%s.gif"%(hora))
            mapas.setdefault("100_%s"%(hora),"mapas\\FL100-%s.gif"%(hora))
    
    #print mapas.keys()
    return mapas



#Funcion en desuso debido a problemas para imorimir poor ambas caras  
def imprimeTaf():
    
    """Esta funcion imprime el archivo con los tafs"""
    os.startfile("./tafAlternos.txt","print")
    

"""
FL390 = "http://www.aviationweather.gov/data/iffdp/2310.gif"
mapa2 = "mapas\\FL390-12z.gif"
urllib.urlretrieve(FL390,mapa2)
#print mapa2
#mapas.append(mapa2)
                
FL340 = "http://www.aviationweather.gov/data/iffdp/2311.gif"
mapa3 = "mapas\\FL340-12z.gif"
urllib.urlretrieve(FL340,mapa3)
#print mapa3
#mapas.append(mapa3)
                
FL300 = "http://www.aviationweather.gov/data/iffdp/2312.gif"
mapa4 = "mapas\\FL300-12z.gif"
urllib.urlretrieve(FL300,mapa4)
#print mapa4
#mapas.append(mapa4)
        
FL100 = "http://www.aviationweather.gov/data/iffdp/2315.gif"
mapa5 = "mapas\\FL100-12z.gif"
urllib.urlretrieve(FL100,mapa5)
#print mapa5
#mapas.append(mapa5)


taf = "https://www.aviationweather.gov/taf/data?ids=MROC%20KMIA%20KFLL%20KPBI%20KRSW%20KMCO%20KTPA%20KPBI%20MMMD&format=raw&hours=0&taf=off&layout=off&date=0"
        
"""    


            
            