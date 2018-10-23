import os
import time
from colorama import Fore, Back, Style

TOOTH_IMG = """             `----------.        .------------ 
             `::``````````.---:::--.```````````.:- 
            `/`` ```````````````.----.`````````.-:-
            /.`  ``````````````````````````````.--/
            /``  `````````````````````````````.---/
            /``  ````````````````````````````.---:.
            --`   ``````````````````````````.---:: 
             /.```````````````````````````..----/  
             `/``  ``````````````````````.-----/`  
              .:````````````````````````.-----/.   
               ./```````````````````````.-----:    
                +-``````````````````````.----./                        TESTER SCOVOLINI
                /..`````````````````````.-----/    
                /````````````...-.``````.-----/    
                :``````````.--:-`-:.`````.----+    
                -.````````.--:-   `:-`````.---+    
                `/```````.---:      :-````.---+    
                 --`````.---/        /`````---/    
                  /.````.---:        .:````---:    
                   /.```.--/`         /```.--/`    
                    :-```.-/.         /```.-:-     
                     -:``.---         /``..:-      
                      `:.`../        `:`.-:.       
                        .:-./        `/.::`        
                          ``          `-`  """         



def splash_screen():
    os.system("clear")
    for _ in range(10):
        print("")
    print(TOOTH_IMG)
    time.sleep(3)
    os.system("clear")

#
#key = None
#
#def callback(event):
#    global key = event.name
#    
#
#def choose_one(options_list):
#    selection = 0
#    keyboard.hook(callback)
#    while key != 'enter':
#        os.system("clear")
#        if key == 'up':
#            selection = (selection - 1) % len(options_list)
#        elif key == 'down':
#            selection = (selection + 1) % len(options_list)
#        for i in range(len(options_list)):
#            option = str(i) + ". " + options_list[i]
#            if selection == i:
#                print(Fore.BLACK + Back.WHITE + option + Style.RESET_ALL)
#                print(Style.RESET_ALL)
#            else:
#                print(option)
#        key = keyboard.read_key()
#    return selection
#    