# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:52:26 2019
"""

""" Write a python program that takes integer n as user input and prints all the prime numbers till n (including n) """
     
n = input('Enter the number : ')

try:
    n = int(n)
except ValueError:
    print('Enter the value in numbers/integers')  
else : 
    # prime numbers are greater than 1
    for val in range(1, n + 1): 
      
       # If num is divisible by any number   
       # between 2 and val, it is not prime  
       if val > 1: 
           for n in range(2, val): 
               if (val % n) == 0: 
                   break
           else: 
               print(val) 
               
""" Write a python program that takes a string n as user input and prints whether the string is a palindrome or not """
 
s = input('Enter the value : ')
rev_s = s[::-1]

if s == rev_s:
    print("Its a palindrome")
else :
    print("Not a palindrome")
 
    
""" Write a python program that displays the following menu """

import sys
import pandas as pd
n = 4
""" Menu Display"""
def menu(book_data):
    print("************ BOOK MENU **************")
    choice = input("""a: Enter the Book Details \nb: View books \nc: Search book \nd: Remove book \ne: Exit \n**************************\nPlease enter a choice : """)
    
    if choice == "A" or choice =="a":
        book_data = addbook(book_data)
        print("Added")
        print(book_data)
        menu(book_data)
    elif choice == "B" or choice =="b":
        if len(book_data) == 0:
            print("\nNo Data!! Please Add\n")
            menu(book_data)
        else:
            book_data = viewbook(book_data)
            menu(book_data)
    elif choice == "C" or choice =="c":
        if len(book_data) == 0:
            print("\nNo Data!! Please Add\n")
            menu(book_data)
        else:
            book_data = searchbook(book_data)
            menu(book_data)
    elif choice=="D" or choice=="d":
        if len(book_data) == 0:
            print("\nNo Data!! Please Add\n")
            menu(book_data)
        else:
            book_data = removebook(book_data)
            menu(book_data)
    elif choice=="E" or choice=="e":
        sys.exit
    else:
        print("You must only select either A,B,C, or D.")
        print("Please try again")
#        sys.exit
        menu()

def addbook(book_data):
    bookid = input("Enter book id : ")
    booktitle = input("Enter book title : ")
    pages = input("Enter book pages : ")
    price = input("Enter book price : ")
    try:
        bookid = int(bookid)
    except ValueError:
        print('Enter the value in numbers/integers') 
    else:
        book_data =  book_data.append({'bookid': bookid , 'booktitle':booktitle ,'pages':pages , 'price':price }, ignore_index=True)
        return book_data

def viewbook(book_data):
    print(book_data)
    return book_data
    
def searchbook(book_data):
    bid = int(input("Enter book id : "))
    dfi = book_data[book_data['bookid']==bid].index.values.astype(int)
    print("\n#########################################################")
    search = book_data.iloc[dfi]
    print(search)
    print("#########################################################\n")
    return book_data

def removebook(book_data):
    bookid = int(input("Enter book id : "))
    dfi = book_data[book_data['bookid']==bookid].index.values.astype(int)[0]
#    print(dfi)
    book_data = book_data.drop(dfi)
    print("Book ID : "+bookid+" Deleted")
    print(book_data)
    return book_data
    
book_data = pd.DataFrame(columns = ['bookid', 'booktitle','pages','price'])   
menu(book_data)


""" Write a python program that takes in the number of lines n as user input and prints the following pattern """

def line_pattern(n): 
    lt = [] 
    m = 3
    for i in range(0,n): 
        if i == 0:
            lt.append(str(m))
        else :
            lt.append("_"*i+str(m))
        m = m+3
    print("\n".join(lt)) 


lines = int(input("Enter the number of lines : "))
line_pattern(lines)
    