import tkinter as ui
import os
import random
import array

# vars #

# Set child dir to our game folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Folder Name to store users always add a / to the end of the name
userFolderName = 'users/'

# UI vars
frameBgColor = "lightgray"
errorTextColor = "red"

# Screen set up
screen = ui.Tk()
canvas = ui.Canvas(screen, height=600, width=600)    
frame = ui.Frame(screen, bg=frameBgColor)

# Login / Register Lables 
loginHeaderLabel = ui.Label(frame, text="Login or Register", bg=frameBgColor)
loginUserLable = ui.Label(frame, text="Username", bg=frameBgColor)
loginPassLable = ui.Label(frame, text="Password", bg=frameBgColor)
loginErrorText = ui.StringVar()
loginErrorLable = ui.Label(frame, textvariable=loginErrorText, bg=frameBgColor, fg=errorTextColor)

# Textarea / Button
userTextArea = ui.Entry(frame)
passTextArea = ui.Entry(frame)

# Array of Login / Registar elements
uiElementsArray = []

# Player Count
userCount = 0

# End vars #

# Functions #
def StartLoop():
    FileSetup()
    UISetUp()

def FileSetup():
    currentDir = os.getcwd()
    newUserDir = os.path.join(currentDir, userFolderName[0:len(userFolderName) - 1])
    if not os.path.exists(newUserDir):
        os.mkdir(userFolderName[0:len(userFolderName) - 1])

def UISetUp():
    # use globle to edit vars outside of the function
    global userTextArea
    global passTextArea

    # use global to edit buttons from ui set up
    global loginButton
    global registerbutton

    # Set Window Name  
    screen.title("Login - Register")

    #main set up full screen
    canvas.pack()

    #set up fames or "Sections of the window" 
    frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Login / Registar UI set up
    loginHeaderLabel.place(relx=0.1, rely=0.02, relwidth=0.8)
    uiElementsArray.append(loginHeaderLabel)
    loginUserLable.place(relx=0.1, rely=0.1, relwidth=0.8)
    uiElementsArray.append(loginUserLable)
    userTextArea.place(relx=0.35, rely=0.18, relwidth=0.3)
    uiElementsArray.append(userTextArea)
    loginPassLable.place(relx=0.1, rely=0.26, relwidth=0.8)
    uiElementsArray.append(loginPassLable)
    passTextArea.place(relx=0.35, rely=0.34, relwidth=0.3)
    uiElementsArray.append(passTextArea)
    loginErrorLable.place(relx=0.1, rely=0.45, relwidth=0.8)
    uiElementsArray.append(loginErrorLable)

    # Login / Register Buttons
    loginButton = ui.Button(frame, text="Login", command=Login)
    loginButton.place(anchor='w', relx=0.30, rely=0.42, relwidth=0.18)
    uiElementsArray.append(loginButton)
    registerbutton = ui.Button(frame, text="Register", command=Register)
    registerbutton.place(anchor='e', relx=0.70, rely=0.42, relwidth=0.18 )
    uiElementsArray.append(registerbutton)

# Register the user into a text file
def Register():
    # Get the string from the Entry field
    currentUsername = userTextArea.get()
    currentPassword = passTextArea.get()

    # Check to see if the User exists. If not a new user is made 
    if len(userTextArea.get() or passTextArea.get()) == 0:
        UpdateLabelText(loginErrorLable, loginErrorText, 'No user data', 'red')
    else:
        if currentUsername.isspace() or len(userTextArea.get()) == 0:
            UpdateLabelText(loginErrorLable, loginErrorText, 'Please type a username', 'red')
        elif currentPassword.isspace() or len(passTextArea.get()) == 0:
            UpdateLabelText(loginErrorLable, loginErrorText, 'Please type a password', 'red')
        else:
            if os.path.exists(userFolderName + currentUsername):
                UpdateLabelText(loginErrorLable, loginErrorText, currentUsername + ' already exists', 'red')
            else:
                userFile = open(userFolderName + currentUsername, "w")
                userFile.write(currentUsername+"\n")
                userFile.write(currentPassword)
                userFile.close()
                UpdateLabelText(loginErrorLable, loginErrorText, currentUsername + ' registered', 'green')

    # Clear entry fields when the button is clicked
    ClearLoginText()

def Login():
    # Get the string from the Entry field
    currentUsername = userTextArea.get()
    currentPassword = passTextArea.get()

    #Count for user logins
    global userCount

    #list of files in the user folder
    users = os.listdir(userFolderName[0:len(userFolderName) - 1])

    if currentUsername in users:
        userFile = open(userFolderName + currentUsername, 'r')
        fileInfo = userFile.readlines()
        if currentPassword == fileInfo[1]:
            ClearLoginText()
            UpdateLabelText(loginErrorLable, loginErrorText, 'Login success', 'green')
            userCount += 1
            if userCount == 2:
                print('Start Game')
                ClearUi(uiElementsArray)
        else:
            ClearLoginText()
            UpdateLabelText(loginErrorLable, loginErrorText, 'incorrect password', 'red')
    else:
        ClearLoginText()
        UpdateLabelText(loginErrorLable, loginErrorText, 'user ' + currentUsername + ' not found', 'red')

# Clears text from the Entry Fields
def ClearLoginText():
    userTextArea.delete(0, ui.END)
    passTextArea.delete(0, ui.END)

def UpdateLabelText(labelObj, textVar, errorText, errorColor):
    textVar.set(errorText)
    labelObj.config(fg=errorColor)

#clears elements in the array provided uiElements = array of tkinter wigets
def ClearUi(uiElements):
    for i in uiElements:
        i.destroy()

# End functions #

StartLoop()
screen.mainloop()