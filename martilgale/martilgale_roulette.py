import pyperclip as pyp
import pyautogui
import time

# this program automaticly uses martingale method in roulette which doubles
# the bet size size if you lose and bring back to bet size to one unit if you lose


# this method moves the mouse cursor to the coordinates and clicks num-clicks times
def click_coordinates(x, y, num_clicks=1):
    pyautogui.click(x, y, num_clicks, interval=0, button="left")


def get_postion():
    pyautogui.alert(
        "lease put the mouse cursor on black betting button ,you have 2 seconds.")
    time.sleep(2)
    x_black, y_black = pyautogui.position()

    pyautogui.alert(
        "lease put the mouse cursor on red betting button ,you have 2 seconds.")
    time.sleep(2)
    x_red, y_red = pyautogui.position()

    pyautogui.alert(
        "lease put the mouse cursor on html of the result ,you have 2 seconds.")
    time.sleep(2)
    x_html, y_html = pyautogui.position()

    pyautogui.alert(
        "lease put the mouse cursor on the rotate button ,you have 2 seconds.")
    time.sleep(2)
    x_button, y_button = pyautogui.position()

    return x_black, y_black, x_red, y_red, x_html, y_html, x_button, y_button


def get_number_from_clipboard():
    pyautogui.hotkey("ctrl", "c")
    text1 = pyp.paste()
    #text1 = text.replace(" ", "")
    number = 50
    #number_place = text1.find(">")
    if(text1[55:57].isdigit()):
        number = int(text1[55:57])
    elif(text1[55].isdigit()):
        number = int(text1[55])
    return number


f = open("C:\\Users\\main laptop\\programation\\algorthims coursera\\gambling\\martilgale\\result.txt", "w")


# gets coordinates from the chosen roulette site
x_black, y_black, x_red, y_red, x_html, y_html, x_button, y_button = get_postion()

# bets on red to begin the sequenceand goes to html to get changing number
click_coordinates(x_red, y_red)
#click_coordinates(x_button, y_button)
click_coordinates(x_html, y_html)
winning_number = []
winning_number.append(get_number_from_clipboard())
f.write((str(winning_number) + " red " + str(1) + "\n"))

martilgale = ["red", "red", "black", "red", "black",
              "black"]  # martilgale sequence sequence
red_numbers = [1, 3, 5, 7, 9, 12, 14, 16,
               18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_numbers = [2, 4, 6, 8, 10, 11, 13, 15,
                 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

i = 0  # counter for matigale sequence
bet = 1
while(True):
    number = get_number_from_clipboard()
    if winning_number[-1] != number and number < 37:  # if the result changes we bet
        i = i % 6
        winning_number.append(number)
        f.write(str(number)+" \n")

        # check if number is red <or black or 0
        if (number in red_numbers):
            color = "red"

        elif(number in black_numbers):
            color = "black"

        else:
            color = 0

        time.sleep(2.5)
        # if color is the same color we betted on we only bet 1 unit on the next color in the sequence
        if color == martilgale[i % 6]:
            bet = 1
            if martilgale[(i+1) % 6] == "red":
                click_coordinates(x_red, y_red)  # bet red
                f.write((" red " + str(1) + "\n"))

            else:
                click_coordinates(x_black, y_black)  # bet black
                f.write((" black " + str(1) + "\n"))

            # click_coordinates(x_button, y_button)  # click rotate
            # return to html and wait for number
            click_coordinates(x_html, y_html)

        # if color is not same color we betted w bet twice th amount we betted last on the next color in the sequence
        else:
            bet = bet*2
            if martilgale[(i+1) % 6] == "red":
                click_coordinates(x_red, y_red, bet)
                f.write(("red " + str(bet) + "\n"))
            else:
                click_coordinates(x_black, y_black, bet)
                f.write((" black " + str(1) + "\n"))
            #click_coordinates(x_button, y_button)
            click_coordinates(x_html, y_html)

        i = i+1  # go to next color in sequence
