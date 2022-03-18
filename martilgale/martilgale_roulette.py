import pyperclip as pyp
import pyautogui
import time

# this program automaticly uses martingale method in roulette which doubles
# the bet size if you lose and bring back to bet size to one unit if you win following a given sequence


# this function moves the mouse cursor to the coordinates and clicks num-clicks times
def click_coordinates(x, y, num_clicks=1, a=0):
    pyautogui.click(x, y, num_clicks, interval=a, button="left")

# this function gets the coordinates of: black and red betting buttons ,html position for winning number and rotate button


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

# this function extracts winning number from html that has no ">" before winng number


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

# this function extracts winning number from html that has no ">" before winng number


def get_number_from_clipboard2():
    pyautogui.hotkey("ctrl", "c")
    text = pyp.paste()
    print(text)
    text1 = text.replace(" ", "")
    number = 50
    number_place = text1.find(">")
    if(text1[number_place+3:number_place+5].isdigit()):
        number = int(text1[number_place+3:number_place+5])
    elif(text1[number_place+3].isdigit()):
        number = int(text1[number_place+3])
    return number


def roulette_with_button():

    # gets coordinates from the chosen roulette site
    x_black, y_black, x_red, y_red, x_html, y_html, x_button, y_button = get_postion()

    # bets on red to begin the sequenceand goes to html to get changing number
    click_coordinates(x_red, y_red, 1, 0.25)
    click_coordinates(x_button, y_button)
    click_coordinates(x_html, y_html)
    winning_number = []
    winning_number.append(get_number_from_clipboard2())
    f.write("1 red " + str(1) + "\n")

    martilgale = ["red", "red", "black", "red", "black",
                  "black"]  # martilgale sequence sequence
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16,
                   18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15,
                     17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    j = 1  # counter for betting times
    i = 0  # counter for matigale sequence
    bet = 1
    current_time = time.time()
    while(True):
        number = get_number_from_clipboard2()
        next_time = time .time()
        # if the result changes we bet
        if winning_number[-1] != number and number < 37 or (next_time-current_time > 10):
            winning_number.append(number)
            f.write(str(j+1)+" "+str(number))
            i = i % 6

            time.sleep(2.5)
            # check if number is red <or black or 0
            if (number in red_numbers):
                color = "red"
                f.write(" r ")

            elif(number in black_numbers):
                color = "black"
                f.write(" b ")

            else:
                color = 0

            # if color is the same color we betted on we only bet 1 unit on the next color in the sequence
            if color == martilgale[i % 6]:
                bet = 1
                if martilgale[(i+1) % 6] == "red":
                    click_coordinates(x_red, y_red, 1, 0.25)  # bet red
                    f.write((" red " + str(1) + "\n"))

                else:
                    click_coordinates(x_black, y_black, 1, 0.25)  # bet black
                    f.write((" black " + str(1) + "\n"))

                click_coordinates(x_button, y_button)  # click rotate
                # return to html and wait for number
                click_coordinates(x_html, y_html)

            # if color is not same color we betted w bet twice th amount we betted last on the next color in the sequence
            else:
                bet = bet*2
                if martilgale[(i+1) % 6] == "red":
                    click_coordinates(x_red, y_red, bet, 0.25)
                    f.write((" red " + str(bet) + "\n"))
                else:
                    click_coordinates(x_black, y_black, bet, 0.25)
                    f.write((" black " + str(bet) + "\n"))
                click_coordinates(x_button, y_button)
                click_coordinates(x_html, y_html)

            current_time = time.time()
            i = i+1
            j = j+1  # go to next color in sequence


f = open("result.txt", "w")
roulette_with_button()
