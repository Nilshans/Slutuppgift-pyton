#--------------------------- CLASSES ------------------------->
class boardgame():

    def __init__(self, title, players, time, age_restriction, user=None):
        self.title = title
        self.players = players
        self.time = time
        self.age_restriction = age_restriction
        self.user = user
        self.default = ""
        if user is None:
            user = self.default

    def print_properties(self):
        if self.user != None:
            print (self.user)
        print ("Title: "+str(self.title)+" Players: "+str(self.players)+" Time: "+str(self.time)+" Age: "+str(self.age_restriction))
    def add_to_file(self):
        f = open('workfile.txt', 'a')
        user = self.user
        if user == None:
            user = ""
        f.write(user+str(self.title)+", "+str(self.players)+", "+str(self.time)+", "+str(self.age_restriction)+"\n")
        f.close()
    def add_to_file_user(self):
        f = open('workfile.txt', 'a')
        f.write(self.user+"\n")
        f.close()

class userFrame():

    def __init__(self, username, items, index):
        self.username = username
        self.items = items
        self.index = index
    def print_properties(self):
        print(self.username, self.items, self.index)

#--------------------------- List functions ------------------------->

raw_d = []
pure_d = []
user_d = []
board_d = []
users = []

def fill_raw_d():       #Reads from file into list line by line
    raw_d.clear
    f = open('workfile.txt', 'r')
    for line in f:
        raw_d.append(line)
    f.close()
def fill_pure_d():      #Formats data into lines of lists
    pure_d.clear()
    for i, j in enumerate(raw_d):
        raw_d[i] = raw_d[i].rstrip('\n')
        raw_d[i] = raw_d[i].replace(",","")
        newLine = (raw_d[i].split())
        pure_d.append(newLine)
def fill_users():       #Selects lists with one element to distinguish users from boardgames. Enters 3 values: username, index and items
    users.clear()       #Function reads indexvalues where length of list is 1. Then match these values to get distance to next user index to get number of items
    x = 0
    userBoards = []
    for i, j in enumerate(pure_d):
        if len(pure_d[i]) == 1:
            userBoards.append(i)
            i += 1
        x = i + 1
    userBoards.append(x)
    userBoards.remove(0)
    for i, j in enumerate(pure_d):
        if len(userBoards) != 0 and len(j) == 1:
            b = userBoards.pop(0)
        if len(j) == 1:
            b = b - i
            users.append([j, b, i]) #User + gameboards + start index
        i += 1

def add_content_to_file(save):      #Function calls a class function that writes to file if true
    board_d.clear()                 #If False, then it populates a list of object that can be used later 
    if save == True:
        clean_file()
    for i, j in enumerate(pure_d): # i = list 2 index | j = list2 value ex newGame(0,1,2,3)
        if len(j) == 1:
            for z, y in enumerate(j): #z = tuple index newGame(0,1,2,3) | y = tuple value
                if z == 0:
                    newUser = boardgame("", "", "", "", y)
                    if save == True:
                        newUser.add_to_file_user()
                    else:
                        board_d.append(newUser)
            i += 1
        else:
            for z, y in enumerate(j): #z = tuple index newGame(0,1,2,3) | y = tuple value
                if z == 0:
                    title = y
                if z == 1:
                    players = y
                if z == 2:
                    time = y
                if z == 3:
                    age_restriction = y
            newBoardgame = boardgame(title, players, time, age_restriction)
            if save == True:
                newBoardgame.add_to_file()
            else:
                board_d.append(newBoardgame)

def set_user_list(user):    #Function returns a list of boardgames based on a users indexvalues
    userBoard = board_d.copy()
    for x in user_d:
        if x.username == user:
            del userBoard[x.index+x.items:]
            del userBoard[0:x.index+1]
            return userBoard

def clean_file():           #When its time to write(append) data to file I make sure to clean the file first so no data duplicates
    f = open('workfile.txt', 'w')
    f.write("")
    f.close()
def user_boards():          #Saves data to a list of object values
    user_d.clear()
    for i, j in enumerate(users):
        for x, y in enumerate(j):
            if x == 0:
                username = str(y[0])
            if x == 1:
                items = y
            if x == 2:
                index = y
        userData = userFrame(username, items, index)
        user_d.append(userData)
def update_lists():         #A small function with purpose to update a collection of list functions
    fill_users()
    user_boards()
    add_content_to_file(False)
def set_index_values(user): #Returns a list of saved index/item values based on current user
    index = 0
    items = 0
    for z in user_d:
        if z.username == user:
            index = z.index
            items = z.items
    return [index, items]

#--------------------------- Menu functions ------------------------->
def add_item(user):
    index = 0
    items = 0
    while True:
        try: 
            title = str(input("Enter a title: "))
            if set_user_list(user) != None:
                for x in set_user_list(user):
                    while x.title == str(title):
                        raise NameError(title)
            break
        except NameError:
            print("Game already exists, enter another one!")
        except ValueError:
            print ("ValueError, please use characters")
    while True:
        try:
            players = int(input("Enter number of players: "))
            break
        except ValueError:
            print ("ValueError, please use numbers")
    while True:
        try:
            time = int(input("Enter time / session: "))
            break
        except ValueError:
            print ("ValueError, please use numbers")
    while True:
        try:
            age_restriction = int(input("Enter age restriction: "))
            break
        except ValueError:
            print ("ValueError, please use numbers")
    
    boardEntry = (title, players, time, age_restriction)
    for y in user_d:
        if y.username == user:
            index = y.index
            items = y.items
    pure_d.insert(index+items, boardEntry)
    update_lists()
    main_options(user)

def add_filter(user):
    set_index_values(user)
    boards = []
    filterBoards = []
    answerPlayers = input("Set a filter on MAX players: ")
    answerTime = input("Set a filter on MAX time: ")
    answerAge = input("Set a filter on MIN age: ")
    for x, y in enumerate(set_user_list(user)):
        if (y.players <= answerPlayers and y.time <= answerTime) and (y.age_restriction >= answerAge):
            filterBoards = boardgame(y.title, y.players, y.time, y.age_restriction)
            boards.append(filterBoards)

    for i in boards:
        i.print_properties()

def select_user():
    print("Here are all saved users: ")
    if len(user_d) == 0:
        add_user()
    for x in user_d:
        print(x.username)
    while True:
        try:
            user = str(input("Select a user or type another username: "))
            for x in user_d:
                if user == x.username:
                    current_user = user
                    print(str("You selected: "+current_user))
                    return user
            print("Sorry, no such user exist")
            select_user()
            break
        except ValueError:
            print ("ValueError, please use characters")

def add_user():
    user = input("Enter a username: ")
    pure_d.append([user])
    update_lists()
    main_options(user)

def delete_user(user):
    indexValues = set_index_values(user)
    for x in user_d:
        if x.username == user:
            print(str(user)+" at row: "+str(indexValues[0])+" with "+str(indexValues[1])+" items was deleted")
            del pure_d[indexValues[0]:indexValues[0]+indexValues[1]]
            update_lists()
            main_options(None)

def remove_item(user):
    index = 0
    items = 0
    titleNotFound = True
    for j in set_user_list(user):
        print(j.title)
    title = input("Type the title you wish to remove: ")
    for z in user_d:
        if z.username == user:
            index = z.index
            items = z.items
    for x, y in enumerate(set_user_list(user)):
        if y.title == title:
            print("Found "+str(title)+" at row: "+str(index+x))
            del pure_d[index+x+1:index+x+2]
            titleNotFound = False
    update_lists()
    for i in set_user_list(user):
        print(i.title)
    if titleNotFound == True:     
        print("Sorry, no such title could be found")
    main_options(user)
    
def save_and_exit():
    print("Saved changes successfully")
    add_content_to_file(True)
def show_all_programs(show):
    for x in board_d:
        if show == True:
            x.print_properties()

#--------------------------- Main function ------------------------->

def main_options(current_user):
    if current_user == None:
        current_user = select_user()
    while True:
        try:
            answer = int(input("Make a choise: 1.add boardgame, 2.add_filter, 3.remove_boardgame 4.change user, 5.add user, 6..delete user(and all its boardgames) 7.save and exit: "))
            while answer < 1 or answer > 7:
                raise NameError(answer)
            if int(answer) == 1:
                add_item(current_user)
            if int(answer) == 2:
                add_filter(current_user)
            if int(answer) == 3:
                remove_item(current_user)
            if int(answer) == 4:
                select_user()
            if int(answer) == 5:
                add_user()
            if int(answer) == 6:
                delete_user(current_user)
            if int(answer) == 7:
                save_and_exit()
            break
        except NameError:
                print ("No such option!")
        except ValueError:
            print ("ValueError, please use numbers")

#--------------------------- Initialize data ------------------------->

fill_raw_d()
fill_pure_d()
update_lists()
main_options(None)
