import cv2
import mediapipe as mp
import numpy as np
import json



# Define some colors
BLACK = ( 0, 0, 0)

BG = (30,30,30)

WHITE = ( 255, 255, 255)

WHITE2 = (150,150,150)

GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
LINE_COLOR = (255,255,255)

# Open a new window

ANCHO = 1500
ALTO = 600

ANCHOA = 480
ALTOA = 640

GLINEAS = 5
TIPOLINEA = cv2.LINE_8

RCIRCULO = 10


DIBUJARCIRCULOS = True
DIBUJARLINEAS = True
DIBUJARDEDOSJUNTOS = True

# unir dos imagenes hstak
class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontColor = (255, 255, 255)
        self.fontScale = 0.5
    
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def positionFinder(self,image, handNo=0, draw=True, positions = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            #print(self.results.multi_hand_landmarks)
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                
                #cx,cy = int(lm.x), int(lm.y)
                lmlist.append([id,cx,cy])
                #print(f'{id} , {lm}')
                if draw:
                    cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)
                    
                if positions:
                    cv2.putText(image, f"{id+1} \n x: {cx} \n y: {cy}", (cx,cy), self.font, self.fontScale, self.fontColor)

                
        list_positions = {}
        try:
            list_positions['0'] = [lmlist[0]]
            list_positions['1'] = lmlist[1:5]
            list_positions['2'] = lmlist[6:9]
            list_positions['3'] = lmlist[10:13]
            list_positions['4'] = lmlist[14:17]
            list_positions['5'] = lmlist[18:21]
        except IndexError:
            pass
                 
        return list_positions


def main():
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("rtsp://192.168.1.16:8080/h264.sdp")
    
    
    tracker = handTracker()
    
    


    # Establecer el ancho y alto de la ventana
    #ancho = 800
    #alto = 600
    #cv2.resizeWindow('MiVentana', ancho, alto)
    
    while True:
        success, image = cap.read()
        try:
            image = cv2.flip(image, 1)
            image = tracker.handsFinder(image)
            h, w, c = image.shape
            t = image.shape
            lmList = tracker.positionFinder(image)
        except:
            pass
        dibujo = np.zeros(t)
        
        try:
            mu = lmList["0"][0]
            
            f1 = lmList["1"][0]
            f2 = lmList["2"][0]
            f3 = lmList["3"][0]
            f4 = lmList["4"][0]
            f5 = lmList["5"][0]
            
        except:
            pass
        
        elementListPoints = list(lmList)
        for element in range(len(elementListPoints)-1):
            for pos in lmList[elementListPoints[element+1]]:
                
                #print(pos)
                x = pos[-2]
                y = pos[-1]
                radio = 1
                #pygame.draw.ellipse(screen, WHITE2, [x,y,x,y], 1)
                if DIBUJARCIRCULOS:
                    cv2.circle(dibujo, (x, y), RCIRCULO, WHITE2, GLINEAS, TIPOLINEA)
        
        
        pad = 80
        def circulo(mu, f, c):
            
            pasos = 5
            pasosy = 5
            
            lx = f[1]
            ly = f[2]
            
            #print(f)
            for a in range(4,0,-1):
                
                disCir = ((mu[2] - f[2]) / pasosy)
                yy = abs(mu[2] - (a * disCir)) 
                
                disx = ((mu[1] - f[1]) / pasos)
                xx = abs(mu[1] - (a * disx))   # Definir el rango máximo usando el valor 'pad'
                
                
                
                
                #print(xx,yy,a+1,f, max_range)
                if DIBUJARCIRCULOS:
                    cv2.circle(dibujo, (xx, yy), RCIRCULO, c, GLINEAS, TIPOLINEA)
                if DIBUJARLINEAS:
                    #pygame.draw.line(screen, c, [lx,ly], [xx, yy], GLINEAS)
                    cv2.line(dibujo, [lx,ly], [xx, yy] , c, GLINEAS )
                
                    
                lx = xx
                ly = yy
            print(lx,ly)
            
            return [lx, ly]

        try:
            muny = []
                
            muny.append(circulo(mu, f2, (150,150,255)))
            muny.append(circulo(mu, f3, (150,255,150)))
            muny.append(circulo(mu, f4, (255,150,150)))
            muny.append(circulo(mu, f5, (250,250,250)))
            
            if DIBUJARDEDOSJUNTOS and DIBUJARLINEAS:
                for element in range(len(muny)-1):
                    #pygame.draw.line(screen, WHITE2, [muny[element][0],muny[element][1]],[muny[element+1][0],muny[element+1][1]], GLINEAS)
                    cv2.line(dibujo, [muny[element][0],muny[element][1]], [muny[element+1][0],muny[element+1][1]] , WHITE2, GLINEAS )
        except:
            pass         

        
        for element in range(len(list(lmList))):
            elementLists = list(lmList)[element]
            #print(elementLists)
            lenElement = len(lmList[elementLists])-1
            #print(lenElement)
            for pos in range(lenElement):
                #print(positions[elementLists])
                elemento = lmList[elementLists]
                x1 = elemento[pos][1]
                y1 = elemento[pos][2]
                
                x2 = elemento[pos+1][1]
                y2 = elemento[pos+1][2]
                
                if DIBUJARLINEAS:
                    if elementLists == "2":
                        #pygame.draw.line(screen, (150,150,255), [x1,y1], [x2, y2], GLINEAS)
                        cv2.line(dibujo, [x1,y1], [x2, y2] , (150,150,255), GLINEAS )
                
                    if elementLists == "3":
                        #pygame.draw.line(screen, (150,255,150), [x1,y1], [x2, y2], GLINEAS)
                        cv2.line(dibujo, [x1,y1], [x2, y2] , (150,255,150), GLINEAS )
                    if elementLists == "4":
                        #pygame.draw.line(screen, (255,150,150), [x1,y1], [x2, y2], GLINEAS)
                        cv2.line(dibujo, [x1,y1], [x2, y2] , (255,150,150), GLINEAS )
                    if elementLists == "5":
                        #pygame.draw.line(screen, (250,250,250), [x1,y1], [x2, y2], GLINEAS)
                        cv2.line(dibujo, [x1,y1], [x2, y2] , (250,250,250), GLINEAS )
                    if elementLists == "1":
                        #pygame.draw.line(screen, WHITE2, [x1,y1], [x2, y2], GLINEAS)
                        cv2.line(dibujo, [x1,y1], [x2, y2] , WHITE2, GLINEAS )
     
        
        
            #cv2.putText(image, f"signo: {obtenerSigno(lmList,'a')}", (10, h-20), tracker.font, 2, tracker.fontColor)
        #dibujo_resultado = np.hstack([image,dibujo])
        #cv2.imshow("imagen", image)
        cv2.imshow("dibujo", dibujo)
        #cv2.imshow("resultado", dibujo_resultado)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
