# Creates Environment
import os

f = open("availablebooks.txt","w")
f.write("Jungle\nJokes\nFiction\nSpace\nScience\nMaths\nCS\nComic")
f.close()

f = open("borrowedbooks.txt","w")
f.close()

f = open("keys.txt","w")
f.close()

f = open("users.txt","w")
f.close()

os.remove(f"{os.getcwd()}\\environment.py")