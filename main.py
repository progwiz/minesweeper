import UI
import sys

if __name__ == "__main__":
    print("Minefield dimensions: ", sys.argv[1]," X ", sys.argv[2])
    #try:
    UI.GUI(int(sys.argv[1]),int(sys.argv[2]))
    #except: 
    #    print("GUI FAILED TO START!")
