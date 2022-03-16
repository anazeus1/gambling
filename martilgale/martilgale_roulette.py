import pyperclip as pyp
import pyautogui
import time


def bet_black():
    # pyautogui.moveTo(640,820)  location of black in speed auto roulette
    pyautogui.moveTo(870,870)
    pyautogui.leftClick()

def bet_red():
    #pyautogui.moveTo(560,820) location of red in speed auto roulette
    pyautogui.moveTo(800,870)
    pyautogui.leftClick()

def click_rotate():
    pyautogui.moveTo(1000,1020)
    pyautogui.click()

def return_to_html():
    #pyautogui.moveTo(1800,820) location of html in speed auto roulette
    pyautogui.moveTo(1800,800)
    pyautogui.leftClick()

def get_number_from_clipboard():
    
    pyautogui.hotkey('ctrl','c')
    
    text=pyp.paste()
    number=50
    if(text[55:57].isdigit()):
        
        number=int(text[55:57])
    elif(text[55:56].isdigit()):
        number = int(text[55:56])
    return number

def main():
    i =0
    
    bet=1

    while(True):
        number = get_number_from_clipboard()
        if winning_number[-1]!=number and number<37:
            i=i%6
        
            winning_number.append(number)
            if (number in red_numbers):
                color ="red"
            elif(number in black_numbers):
                color ="black"
            else:
                color=0
            time.sleep(4)
            if color==martilgale[i%6]:
                bet=1
                if martilgale[(i+1)%6]=="red":
                    print(bet,"red")
                    bet_red()
                else:
                    print(bet,"black")
                    bet_black()
                click_rotate
                return_to_html()
            else:
                bet = bet*2
                if martilgale[(i+1)%6]=="red":
                    print(bet,"red")
                    for loop in range(bet):
                        bet_red()
                else:
                    print(bet,"black")
                    for loop in range(bet):
                        bet_black()
                click_rotate()
                return_to_html()
            i=i+1
            print(winning_number)

time.sleep(3)

bet_red()
click_rotate()
return_to_html()
winning_number=[]
winning_number.append(get_number_from_clipboard())

martilgale=["red","red","black","red","black","black"]
red_numbers=[1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
black_numbers=[2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]      
main()