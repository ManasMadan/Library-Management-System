import pyautogui as pag
from tkinter import *
import tkinter.font as font
import random as rd
window = Tk()
myFont = font.Font(family='Helvetica', size=14, weight='bold')


# I/O Functions
def addBooks(book):
    f = open('availablebooks.txt','a')
    f.write(f"\n{book}")
    f.close()
def getUsers():
    users = {}
    f = open('users.txt','r')
    content = f.read()
    user = content.split("\n")
    for i in user:
        try:
            a = i.split('-')
            users.update({a[0]:a[1]})
        except:
            None
    f.close()
    return users
def addUsers(Name,passw):
    f = open('users.txt','a')
    f.write(f"\n{Name}-{passw}")
    f.close()
def getborrowedBooks():
    books = {}
    f = open('borrowedbooks.txt','r')
    content = f.read()
    book = content.split("\n")
    for i in book:
        try:
            a = i.split('-')
            books.update({a[0]:a[1]})
        except:
            None
    f.close()
    return books
def addborrowedBooks(user,book):
    c = getborrowedBooks()
    c.update({user:book})
    f = open('borrowedbooks.txt','a')
    f.write(f"\n{book}-{user}")
    f.close()
def removeborrowedBooks(book):
    b = getborrowedBooks()
    b.pop(book)

    f = open('borrowedbooks.txt','w')
    f.write("")
    f.close()

    f = open('borrowedbooks.txt','a')
    for k in b:
        f.write(f"{k}-{b.get(k)}\n")
    f.close()
def addKey(k):
    g = getKeys()
    g.append(k)
    f = open('keys.txt','w')
    for i in g:
        f.write(f"\n{i}")
    f.close()
def getKeys():
    f = open('keys.txt','r')
    content = f.read()
    content = content.split("\n")
    f.close()
    return content
def removeKey(k):
    f = open('keys.txt','r')
    content = f.read()
    content = content.split("\n")
    f.close()
    content.remove(k)
    f = open('keys.txt','w')
    f.write("")
    f.close()
    f = open('keys.txt','a')
    for i in content:
        f.write(f"{i}\n")
    f.close()
def getBooks(file):
    list = []
    myFile = open(file, "r")
    content = myFile.read()
    content_list = content.split("\n")
    myFile.close()
    return content_list

# Returns Key From Value Of A Dictionary else returns -1
def get_key(val,book): 
    for key, value in book.items(): 
        if val == value:
            return key
    return -1
# Generates A Random Key b/w 1000 and 10000
def randomKey():
    num = rd.randint(1000,10000)
    while(num in getKeys()):
        num = randomKey()
    else:
        addKey(num)
        return num


# Button Functions
#Display Books
def display(): 
    Books = getBooks('availablebooks.txt')
    books = ""
    j = 0
    for i in Books:
        books = books + i + "\t"
        j+=1
        if(j % 9 == 0):
            books = books + 2 * "\n"
        
    
    newWindow = Toplevel(window) 
    newWindow.title("Available Books") 
    
    text = Label(newWindow,text = books,bg = "blanched almond")
    text['font'] = myFont
    text.pack()

    back = Button(newWindow, text="Back", bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120',command = newWindow.destroy)
    back.place(width = 100,height = 40,relx=0.05, rely=0.05, anchor=CENTER)
    back['font'] = myFont



    newWindow.configure(bg='blanched almond')
    newWindow.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
    Label(newWindow).pack()
#login/Sign Up
def login():
    global username
    global loggedIn
    global login_text
    if(loggedIn == True):
        ch = pag.confirm(f"You Are Logged In As {username}",buttons=['Log Out','Cancel'])
        if(ch == 'Log Out'):
            loggedIn = False
            username = ""
            login_text.set("Login/SignUp")
        return
    opt = pag.confirm('Login/SignUp', buttons=['Login', 'SignUp'])
    'B'
    if(opt == 'Login'):
        username = pag.prompt('Enter Username')
        password = pag.password('Enter Password')
        if(username in getUsers().keys()):
            if(password == getUsers().get(username)):
                loggedIn = True
                login_text.set("Logged In")
            else:
                pag.alert("Invalid Credentials!")
                login()
        else:
            pag.alert("Invalid Credentials!")
            login()
    else:
        username = pag.prompt('Enter Username')
        if(username in getUsers().keys()):
            pag.alert("Sorry This Username Is Already Taken")
            login()
        else:
            password = pag.password('Enter Password')
            key = pag.password("Enter The Payment Key")
            if key in getKeys():
                addUsers(username,password)
                pag.alert(f"Sign Up Succesful!, You Have Been Logged In, Your Username Is {username} and Password is {password}")
                login_text.set("Logged In")
                loggedIn = True
                removeKey(key)
            else:
                pag.alert("Invalid Key, Purchase A Key From The Counter")
#LendBooks
def lendBooks():
    global loggedIn
    if(not loggedIn):
        ch = pag.confirm("Login To Continue",buttons=['Login','Cancel'])
        if(ch == 'Login'):
            login()
            return
        else:
            return
    # After Logged In
    if(username in getborrowedBooks().values()):
        pag.alert(f"Sorry The Book {get_key(username,getborrowedBooks())} Has Already Been Lended to You Return It To Get A New One")
        return
    book = pag.prompt('Enter Book Name')
    if book not in getBooks('availablebooks.txt'):
        pag.alert(f"Sorry Currently Our Library Do Not Own The Book {book}")
    elif book in getborrowedBooks().keys():
        pag.alert(f"Sorry {book} is currently lended to user {getborrowedBooks().get(book)}")
    else:
        ch = pag.confirm(f"Do You Want To Continue\nBookname : {book}")
        if(ch == 'OK'):
            pag.alert(f"{book} has been lended to you, get it from the table")
            addborrowedBooks(username,book)
def addBook():
    book = pag.prompt("Enter Book Name")
    if book == "" or book == None:
        return
    ch = pag.confirm("Do You Wish To Continue!")
    if(ch == 'OK'):
        pag.alert(f"Thank You! You Have Been Gifted With A Membership, Use {randomKey()} as a payment key and get a free membership worth rupees 100")
        addBooks(book)
    else:
        return
def returnBook():
    global loggedIn
    if(not loggedIn):
        ch = pag.confirm("Login To Continue",buttons=['Login','Cancel'])
        if(ch == 'Login'):
            login()
            return
        else:
            return
    # After Logging In!
    if(username not in getborrowedBooks().values()):
        pag.alert("You Have Not Been Lended With A book, try adding it to get a free membership")
    else:
        book = pag.prompt("Enter Book You Want To Return!")
        if (book == "" or book == None):
            return
        ch = pag.confirm("Do You Wish To Continue")
        if ch != 'OK':
            return
        removeborrowedBooks(book)
        pag.alert("Book Has Been Returned Keep It On Table No. 10 Thank You!")



# Basic Variables (Global Variables)
library_name = "Manas Library"
loggedIn = False
username = "" # username : password
login_text = StringVar()
login_text.set("Login/SignUp")



if __name__ == "__main__":
    login_btn = Button(window, textvariable=login_text, bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120' , command = login)
    login_btn.place(width = 200,height = 80,relx=0.1, rely=0.07, anchor=CENTER)
    login_btn['font'] = myFont
    
    displayBooks_btn = Button(window, text="Display Books", bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120', command = display)
    displayBooks_btn.place(width = 500,height = 80,relx=0.5, rely=0.18, anchor=CENTER)
    displayBooks_btn['font'] = myFont

    lendBooks_btn = Button(window, text="Lend Books", bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120', command = lendBooks)
    lendBooks_btn.place(width = 500,height = 80,relx=0.5, rely=0.32, anchor=CENTER)
    lendBooks_btn['font'] = myFont

    addBooks_btn = Button(window, text="Add Books", bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120', command = addBook)
    addBooks_btn.place(width = 500,height = 80,relx=0.5, rely=0.46, anchor=CENTER)
    addBooks_btn['font'] = myFont

    returnBooks_btn = Button(window, text="Return Books", bd = '5' , fg='white', bg = 'black' , height = '4' , width = '120', command = returnBook)
    returnBooks_btn.place(width = 500,height = 80,relx=0.5, rely=0.6, anchor=CENTER)
    returnBooks_btn['font'] = myFont

    window.configure(bg='blanched almond')
    lbl = Label(window)
    window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
    window.title(library_name)
    window.mainloop()