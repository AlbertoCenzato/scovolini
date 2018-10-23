#!/usr/bin/python

import sys
import os
import argparse
import time
import json
import signal
import traceback

import threading

from stepper import Stepper
import ui

# ----- global variables ------
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

CONFIG_FILE = "config.json"
DEFAULT_SPEED = 70

save_configuration = False
steps_per_cycle = 0
speed = 0
debug_mode = False


# ---------- functions -------------
def parse_input():
   parser = argparse.ArgumentParser()
   parser.add_argument('cicli', type=int, help="Numero di cicli da effettuare")
   parser.add_argument('--vel', type=int, default=0, help="Velocita' dello scovolino (opzionale)")
   parser.add_argument('--taratura', action='store_true', help="Avvia la procedura per impostare di quanto avanza lo scovolino ad ogni ciclo (opzionale)")
   parser.add_argument('--debug', action='store_true', help="Lancia il programma in modalita' debug")
   return parser.parse_args()


def taratura():
   os.system("clear")
   print("-------------------------------")
   print("| Avvio procedura di taratura |")
   print("-------------------------------\n\n")
  
   raw_input("Portare lo scovolino in posizione di massima estensione e premere [INVIO].\n")
   
   print("Ora lo scovolino tornera' indietro, premere [INVIO] quando si e' soddisfatti della posizione raggiunta.\n")
   raw_input("Premere [INVIO] per iniziare.")
   print("Inizio taratura...")
   time.sleep(2)

   d = {'key_pressed': False}

   def wait_enter():
      raw_input()
      d['key_pressed'] = True

   steps_per_cycle = 0
   with Stepper() as stepper:
      threading.Thread(target=wait_enter).start()
      while not d['key_pressed']:
         stepper.stepBackwards()
         steps_per_cycle += 1
         time.sleep(0.1)
      stepper.stepForward(steps_per_cycle) # go back to initial position
  
   print("Taratura completata!\n")
   time.sleep(2)
   os.system("clear")
   return steps_per_cycle


def load_params(args):
   vel = args.vel
   steps = 0
   if not args.taratura:
      try:
         with open(CONFIG_FILE) as config_file:
            config = json.load(config_file)
            steps = config['steps_per_cycle']
            if vel == 0:
               vel = config['speed']
      except IOError:
         if debug_mode:
            traceback.print_exc("")
         print("Attenzione! File di configurazione non trovato!")
         print("Ripetere la taratura.")
         exit()
   else:
      steps = taratura()
      if vel == 0:
         print("Velocita' di default: " + str(DEFAULT_SPEED))
         vel = DEFAULT_SPEED
   return vel, steps


def exit_program():
   os.system("clear")
   if save_configuration:
      try:
         if os.path.isfile(CONFIG_FILE):
            os.remove(CONFIG_FILE)
         with open(CONFIG_FILE, 'w') as config_file:
            json.dump({'speed': speed, 'steps_per_cycle': steps_per_cycle}, config_file)
      except IOError:
         if debug_mode:
            traceback.print_exc()
            raw_input("")
         print("Impossibile salvare la configurazione corrente!")
         time.sleep(3)
   os.system("clear")
   print("FINE!")
   time.sleep(3)
   os.system("clear")
   sys.exit(0)


# ------------------ PROGRAM --------------------------------------
def main():
   signal.signal(signal.SIGINT, exit_program)
   
   try:
      args = parse_input()
      debug_mode = args.debug
      
      ui.splash_screen()
      
      speed, steps_per_cycle = load_params(args)
   
      save_configuration = True
      
      with Stepper() as stepper:
         stepper.setSpeed(speed)
         for i in range(args.cicli):
            os.system("clear")
            print("Velocita': " + str(speed))
            print("Cicli: " + str(i+1) + "/" + str(args.cicli))
            print("\nPremere CTRL+C per bloccare")
            stepper.stepBackwards(steps_per_cycle)
            stepper.stepForward(steps_per_cycle)
      
   except Exception:
      if debug_mode:
         traceback.print_exc()
         raw_input("")
      os.system("clear")
      print("Si e' verificato un errore imprevisto!")
   
   time.sleep(3)
   exit_program()



if __name__ == "__main__":
   main()