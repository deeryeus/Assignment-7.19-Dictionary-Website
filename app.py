from flask import Flask, render_template

app = Flask(__name__)


file = open('words.txt')
word_list = file.read().splitlines()

# must always be UPPER CASE to compare to the word list
# values are passed on to this global variable from function: word_dictionary()
current_prefix = ''
# words that can use the current prefix are stored in this list
prefix_list = []

# lists the first 26 letters of the alphabet
def get_first_prefixes():
    prefix = ""
    global prefix_list
    prefix_list.clear()

    for word in word_list:
        prefix = word[0]
        prefix_list.append(prefix)

    unique_prefixes = set(prefix_list)
    sorted_prefixes = sorted(unique_prefixes)

    return(sorted_prefixes)

def get_words_with_current_prefix():

    words_with_current_prefix = []

    for word in word_list: # for each word in our list ...

        has_prefix = bool(word.startswith(current_prefix)) # set this bool to true if it contains the prefix...

        if has_prefix: # if it has the selected prefix...
            words_with_current_prefix.append(word) # add it to the list.
    
    return words_with_current_prefix

# returns the next character of prefixes for words that exist 
def get_next_prefix():

    next_prefix = ""

    global prefix_list
    prefix_list.clear()

    words_with_current_prefix = get_words_with_current_prefix()

    character_counter = len(current_prefix)

    # generate a new list of characters with their next prefix
    for word in words_with_current_prefix:
        next_prefix = word[0:character_counter + 1]
        prefix_list.append(next_prefix)

    # remove duplicates
    unique_words_with_next_prefix = set(prefix_list)

    # remove the current prefix from the updated list, if it's in there
    if current_prefix in unique_words_with_next_prefix:
        unique_words_with_next_prefix.remove(current_prefix) 

    # sort alphabetically
    sorted_prefixes = sorted(unique_words_with_next_prefix)

    return sorted_prefixes

def is_valid():
    if current_prefix in word_list:
        return True
    else:
        return False

def get_word_count():
    if is_valid():
        return len(prefix_list)-1 #if current prefix is a valid word, stop it from counting itself
    else:
        return len(prefix_list)

@app.route('/')
def home():

    title = "Word Dictionary"

    prefix_list = get_first_prefixes()

    text = f"There are {get_word_count()} words in the word list with the prefixes below."

    return render_template('home.html', title=title, text=text, prefix_list=prefix_list)

@app.route('/word_dictionary/<string:prefix>')
def word_dictionary(prefix):

    title = "Word Dictionary"

    global current_prefix
    current_prefix = prefix

    prefix_list = get_next_prefix()

    text = ""

    if is_valid():
        text += f"{current_prefix} is a valid word in the list. "
    else:
        text += f"{current_prefix} is not a valid word in the list. "

    if prefix_list:
        text += f"There are {get_word_count()} words that use {prefix} as a prefix:"
    else:
        text += f"There are no more words that use {prefix} as a prefix."

    return render_template('word_dictionary.html', title=title, text=text, prefix_list=prefix_list)

