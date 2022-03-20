from operator import index
from turtle import bgcolor
from black import format_cell
import pyperclip as pyp
import pyautogui
import time
import xlsxwriter
import random
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
    # text1 = text.replace(" ", "")
    number = 50
    # number_place = text1.find(">")
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


def roulette_with_button(worksheet, money):

    # gets coordinates from the chosen roulette site
    x_black, y_black, x_red, y_red, x_html, y_html, x_button, y_button = get_postion()

    # bets on red to begin the sequenceand goes to html to get changing number
    click_coordinates(x_red, y_red, 1, 0.25)
    click_coordinates(x_button, y_button)

    click_coordinates(x_html, y_html)
    row_index = 2  # counter for betting times

    winning_number = []
    winning_number.append(get_number_from_clipboard2())
    worksheet.write("A"+str(row_index), str(row_index-1))
    worksheet.write("B"+str(row_index), str(winning_number[0]))
    worksheet.write("C"+str(row_index), str(1))
    worksheet.write("D"+str(row_index), str(1*bet_unit))
    worksheet.write("E"+str(row_index), "red")
    money = money-bet_unit
    worksheet.write("F"+str(row_index), str(money))

    row_index += 1  # counter for betting times

    martilgale = ["red", "red", "black", "red", "black",
                  "black"]  # martilgale sequence sequence
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16,
                   18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15,
                     17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    i = 0  # counter for matigale sequence
    bet = 1
    current_time = time.time()
    while(i < 6):
        number = get_number_from_clipboard2()
        next_time = time .time()
        # if the result changes we bet
        if winning_number[-1] != number and number < 37 or (next_time-current_time > 10):
            winning_number.append(number)
            worksheet.write("A"+str(row_index), str(row_index-1))
            worksheet.write("B"+str(row_index), str(number))

            i = i % 6

            time.sleep(2.5)
            # check if number is red <or black or 0
            if (number in red_numbers):
                color = "red"

            elif(number in black_numbers):
                color = "black"

            else:
                color = 0

            # if color is the same color we betted on we only bet 1 unit on the next color in the sequence
            if color == martilgale[i % 6]:
                money = money+(2*bet*bet_unit)

                bet = 1
                if martilgale[(i+1) % 6] == "red":
                    click_coordinates(x_red, y_red, 1, 0.25)  # bet red
                    worksheet.write("C"+str(row_index), str(bet))
                    worksheet.write("D"+str(row_index), str(bet*bet_unit))
                    worksheet.write("E"+str(row_index), "red")

                else:
                    click_coordinates(x_black, y_black, 1, 0.25)  # bet black
                    worksheet.write("C"+str(row_index), str(bet))
                    worksheet.write("D"+str(row_index), str(bet*bet_unit))
                    worksheet.write("E"+str(row_index), "black")

                click_coordinates(x_button, y_button)  # click rotate
                money = money-bet_unit
                worksheet.write("F"+str(row_index), str(money))

                # return to html and wait for number
                click_coordinates(x_html, y_html)

            # if color is not same color we betted w bet twice th amount we betted last on the next color in the sequence
            else:
                bet = bet*2
                if martilgale[(i+1) % 6] == "red":
                    click_coordinates(x_red, y_red, bet, 0.25)
                    worksheet.write("C"+str(row_index), str(bet))
                    worksheet.write("D"+str(row_index), str(bet*bet_unit))
                    worksheet.write("E"+str(row_index), "red")
                else:
                    click_coordinates(x_black, y_black, bet, 0.25)
                    worksheet.write("C"+str(row_index), str(bet))
                    worksheet.write("D"+str(row_index), str(bet*bet_unit))
                    worksheet.write("E"+str(row_index), "black")
                click_coordinates(x_button, y_button)
                money = money-(bet*bet_unit)
                worksheet.write("F"+str(row_index), str(money))

                click_coordinates(x_html, y_html)

            current_time = time.time()
            i = i+1   # go to next color in sequence
            row_index += 1


def test_roulette(worksheet, money):

    row_index = 2  # counter for betting times

    winning_number = []
    money_won = []
    money_won.append(money)
    winning_number.append(random.randint(0, 36))
    worksheet.write("A"+str(row_index), row_index-1)
    worksheet.write("B"+str(row_index), winning_number[0])
    worksheet.write("C"+str(row_index), 1)
    worksheet.write("D"+str(row_index), 1*bet_unit)
    worksheet.write("E"+str(row_index), "red")
    money = money-bet_unit
    money_won.append(money)

    worksheet.write("F"+str(row_index), money)

    row_index += 1  # counter for betting times

    martilgale = ["red", "red", "black", "red", "black",
                  "black"]  # martilgale sequence sequence
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16,
                   18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15,
                     17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    i = 0  # counter for matigale sequence
    bet = 1
    while(row_index < 10) and money > 0:
        number = random.randint(0, 36)

        winning_number.append(number)
        worksheet.write("A"+str(row_index), row_index-1)

        i = i % 6

        if (number in red_numbers):
            color = "red"
            worksheet.write("B"+str(row_index), number, format_red)

        elif(number in black_numbers):
            color = "black"
            worksheet.write("B"+str(row_index), number, format_black)

        else:
            color = 0
            worksheet.write("B"+str(row_index), number, format_green)

        # if color is the same color we betted on we only bet 1 unit on the next color in the sequence
        if color == martilgale[i % 6]:
            money = money+(2*bet*bet_unit)

            bet = 1
            if martilgale[(i+1) % 6] == "red":
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet_unit)
                worksheet.write("E"+str(row_index), "red")

            else:
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet_unit)
                worksheet.write("E"+str(row_index), "black")

            money = money-bet_unit
            worksheet.write("F"+str(row_index), money)

            # return to html and wait for number

        # if color is not same color we betted w bet twice th amount we betted last on the next color in the sequence
        else:
            if money > 2*bet*bet_unit:
                bet = bet*2
            else:
                bet = money/bet_unit
            if martilgale[(i+1) % 6] == "red":
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "red")
            else:
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "black")
            money = money-(bet*bet_unit)
            worksheet.write("F"+str(row_index), money)
        money_won.append(money)
        i = i+1   # go to next color in sequence
        row_index += 1
    Max = max(money_won)
    return Max, money_won.index(Max), row_index, money


def massinielo_roulette(worksheet, bet_unit, money):
    excel_sheet = [[99, 101, 102, 103, 104, 104, 103, 102, 101, 101, 100], [1, 99, 101, 103, 104, 104, 104, 103, 102, 101, 100],
                   [2, 1, 99, 102, 103, 104, 105, 104, 103, 102, 100], [
                       3, 3, 2, 99, 102, 104, 105, 106, 105, 103, 101],
                   [4, 4, 3, 2, 99, 102, 105, 107, 107, 105, 102], [4, 4, 4, 4, 2, 99,
                                                                    103, 107, 109, 108, 104], [3, 4, 5, 5, 5, 3, 99, 105, 109, 111, 108],
                   [2, 3, 4, 6, 7, 7, 5, 99, 108, 115, 115], [1, 2, 3, 5, 7, 9, 9, 8, 99, 115, 130], [1, 1, 2, 3, 5, 8, 11, 15, 15, 99, 161], [0, 0, 0, 1, 2, 4, 8, 15, 30, 61, 99]]

    print(excel_sheet)
    row_index = 2  # counter for betting times

    winning_number = []
    money_won = []
    money_won.append(money)
    winning_number.append(random.randint(0, 36))
    worksheet.write("A"+str(row_index), row_index-1)
    worksheet.write("B"+str(row_index), winning_number[0])

    worksheet.write("F"+str(row_index), money)

    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16,
                   18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15,
                     17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    i = 0  # counter for matigale sequence
    bet = 1
    j = 0
    last_color = 0

    while(i < 11) and (j < 11) and money > 0:
        number = random.randint(0, 36)

        winning_number.append(number)
        worksheet.write("A"+str(row_index), row_index-1)

        if (number in red_numbers):
            if last_color == "red":
                money += 2*bet*bet_unit
            worksheet.write("B"+str(row_index), number, format_red)
            i = i+1
            if i == 11:
                worksheet.write("F"+str(row_index), money)

                break
            if excel_sheet[i][j] > 100:
                bet = excel_sheet[i][j] % 100
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "black")
                last_color = "black"
            elif excel_sheet[i][j] != 99:
                bet = excel_sheet[i][j]
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "red")
                last_color = "red"
            else:
                bet = 0
                last_color = 0

        elif(number in black_numbers):
            if last_color == "black":
                money += 2*bet*bet_unit

            j = j+1
            if j == 11:
                worksheet.write("F"+str(row_index), money)

                break
            worksheet.write("B"+str(row_index), number, format_black)
            if excel_sheet[i][j] > 100:
                bet = excel_sheet[i][j] % 100
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "black")
                last_color = "black"
            elif excel_sheet[i][j] != 99:
                bet = excel_sheet[i][j]
                worksheet.write("C"+str(row_index), bet)
                worksheet.write("D"+str(row_index), bet*bet_unit)
                worksheet.write("E"+str(row_index), "red")
                last_color = "red"
            else:
                bet = 0
                last_color = 0

        else:
            worksheet.write("B"+str(row_index), number, format_green)

            if last_color == "red":
                j = j+1
                if j == 11:
                    worksheet.write("F"+str(row_index), money)

                    break

                if excel_sheet[i][j] > 100:
                    bet = excel_sheet[i][j] % 100
                    worksheet.write("C"+str(row_index), bet)
                    worksheet.write("D"+str(row_index), bet*bet_unit)
                    worksheet.write("E"+str(row_index), "black")
                    last_color = "black"
                elif excel_sheet[i][j] != 99:
                    bet = excel_sheet[i][j]
                    worksheet.write("C"+str(row_index), bet)
                    worksheet.write("D"+str(row_index), bet*bet_unit)
                    worksheet.write("E"+str(row_index), "red")
                    last_color = "red"
                else:
                    bet = 0
                    last_color = 0
            elif last_color == "black":
                i = i+1
                if i == 11:
                    worksheet.write("F"+str(row_index), money)
                    break

                if excel_sheet[i][j] > 100:
                    bet = excel_sheet[i][j] % 100
                    worksheet.write("C"+str(row_index), bet)
                    worksheet.write("D"+str(row_index), bet*bet_unit)
                    worksheet.write("E"+str(row_index), "black")
                    last_color = "black"
                elif excel_sheet[i][j] != 99:
                    bet = excel_sheet[i][j]
                    worksheet.write("C"+str(row_index), bet)
                    worksheet.write("D"+str(row_index), bet*bet_unit)
                    worksheet.write("E"+str(row_index), "red")
                    last_color = "red"
                else:
                    bet = 0
                    last_color = 0
        money = money-bet*bet_unit

        worksheet.write("F"+str(row_index), money)

        # return to html and wait for number

        # if color is not same color we betted w bet twice th amount we betted last on the next color in the sequence

        money_won.append(money)
        row_index += 1
    Max = max(money_won)
    return Max, money_won.index(Max), row_index, money


workbook = xlsxwriter.Workbook("massinielo.xlsx")

format_red = workbook.add_format({"bg_color": "#ff0000"})
format_black = workbook.add_format(
    {"bg_color": "#000000", "font_color": "#ffffff"})
format_green = workbook.add_format(
    {"bg_color": "#00ff00"})


worksheet = workbook.add_worksheet(name="result")

worksheet.write("A1", "Number ID")
worksheet.write("B1", "Number")
worksheet.write("C1", "Bet by unit")
worksheet.write("D1", "bet by real money")
worksheet.write("E1", "Betting color")
worksheet.write("F1", "Money now")
bet_unit = 0.2
money = 10
i, j, l, z = massinielo_roulette(worksheet, bet_unit, money)

# roulette_with_button()
workbook.close()
