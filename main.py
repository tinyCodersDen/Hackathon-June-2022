# Write a program that asks the user to enter an integer from 1 to 99. The program should print the integer in words. For example, if the user enters 78, the program should print "Seventy Eight".
# Tip: Integers from 10 to 19 will need special consideration.

import math
num = int(input("Enter a number from 1 to 99: "))
def num_to_word(n):
    if n == 0:
        return ""
    elif n == 1:
        return "One"
    elif n == 2:
        return "Two"
    elif n == 3:
        return "Three"
    elif n == 4:
        return "Four"
    elif n == 5:
        return "Five"
    elif n == 6:
        return "Six"
    elif n == 7:
        return "Seven"
    elif n == 8:
        return "Eight"
    elif n == 9:
        return "Nine"
    elif n == 10:
        return "Ten"
    elif n == 20:
        return "Twenty"
    elif n == 30:
        return "Thirty"
    elif n == 40:
        return "Fourty"
    elif n == 50:
        return "Fifty"
    elif n == 60:
        return "Sixty"
    elif n == 70:
        return "Seventy"
    elif n == 80:
        return "Eighty"
    elif n == 90:
        return "Ninety"

if num < 11:
    print(num_to_word(num))
elif 10 < num < 20:
    if num == 11:
        print("Eleven")
    elif num == 12:
        print("Twelve")
    elif num == 13:
        print("Thirteen")
    elif num == 14:
        print("Fourteen")
    elif num == 15:
        print("Fifteen")
    elif num == 16:
        print("Sixteen")
    elif num == 17:
        print("Seventeen")
    elif num == 18:
        print("Eighteen")
    elif num == 19:
        print("Nineteen")
else:
    tens_place_num = math.floor(num / 10) * 10
    ones_place_num = num - tens_place_num
    print(f"{num_to_word(tens_place_num)} {num_to_word(ones_place_num)}")
