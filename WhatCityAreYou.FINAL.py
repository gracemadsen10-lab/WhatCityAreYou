# What City Are You?
# A lifestyle quiz with five possible city results.

# Path locates photos, and Tkinter provides the window and controls.
# (Python documentation: pathlib; Tkinter)
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Pillow opens and sizes photos for Tkinter. Missing Pillow allows placeholders.
# The exception handler allows the quiz to run without Pillow.
# (Python tutorial: Handling Exceptions; Pillow documentation: ImageTk)
try:
    from PIL import Image, ImageOps, ImageTk
except ImportError:
    Image = None

# These colours define the background, text and pink accent.
BG = '#F8F2EA'
INK = '#332C35'
ACCENT = '#934F67'
# This finds the folder containing this Python file.
# (Python documentation: pathlib)
BASE = Path(__file__).resolve().parent

# Each saved answer is a city name. Its position also tracks quiz progress.
# (Python tutorial: Data Structures)
answers = []

# Each city stores its result text, colour and photo filename.
# (Python tutorial: Data Structures — Dictionaries)
CITIES = {
    'Paris': {'colour': '#965971', 'tag': 'The romantic observer',
              'description': 'You enjoy thoughtful details, creative spaces and taking your time. Your ideal day mixes art, a good cafe and a beautiful walk.',
              'activities': 'Explore an art museum; browse a bookshop; picnic beside the Seine.', 'image': 'paris.jpg'},
    'Tokyo': {'colour': '#6C5A91', 'tag': 'The curious explorer',
              'description': 'You enjoy discovering something unexpected. Design, food and little hidden places make a city feel exciting to you.',
              'activities': 'Explore a new neighbourhood; visit a design shop; try a small ramen restaurant.', 'image': 'tokyo.jpg'},
    'Barcelona': {'colour': '#A75438', 'tag': 'The social sunseeker',
                  'description': 'You love colour, connection and a relaxed rhythm. You are happiest when a day outdoors turns into a lively evening with friends.',
                  'activities': 'Explore colourful architecture; wander a local market; share tapas with friends.', 'image': 'barcelona.jpg'},
    'New York': {'colour': '#45637D', 'tag': 'The energetic dreamer',
                 'description': 'You thrive on variety and possibility. Your ideal city gives you new ideas, lively streets and something different to do each day.',
                 'activities': 'See a live show; explore a gallery; walk through Central Park.', 'image': 'new_york.jpg'},
    'Sydney': {'colour': '#397B78', 'tag': 'The outdoors enthusiast',
               'description': 'You enjoy fresh air, open spaces and an easygoing pace. Your perfect city balances everyday comforts with time by the water.',
               'activities': 'Take a coastal walk; picnic by the harbour; spend a morning at the beach.', 'image': 'sydney.jpg'},
}

# The questions are stored in the order they appear in the quiz.
# Each question contains its wording and a list of five answer options.
# Each option pairs the button text with the city that receives one point.
# Every city appears once per question, giving each city equal scoring opportunities.
QUESTIONS = [
    ('Your perfect free morning starts with...', [
        ('A pastry, a book and a quiet cafe', 'Paris'),
        ('Exploring a neighbourhood I have never seen', 'Tokyo'),
        ('A slow breakfast with friends in the sunshine', 'Barcelona'),
        ('Coffee to go and a full day of plans', 'New York'),
        ('A swim or a walk by the water', 'Sydney')]),
    ('Choose a place to spend an afternoon.', [
        ('A little design store full of unusual things', 'Tokyo'),
        ('A colourful market with friends', 'Barcelona'),
        ('A busy street with galleries and shops', 'New York'),
        ('A sunny park near the coast', 'Sydney'),
        ('An art museum and a secondhand bookshop', 'Paris')]),
    ('Which holiday pace feels most like you?', [
        ('Relaxed days, lively evenings', 'Barcelona'),
        ('Lots to do from morning until late', 'New York'),
        ('Plenty of time outside and room to breathe', 'Sydney'),
        ('Slow wandering and noticing small details', 'Paris'),
        ('Following my curiosity into unexpected places', 'Tokyo')]),
    ('Pick an evening plan.', [
        ('A live show and late-night food', 'New York'),
        ('A sunset picnic by the water', 'Sydney'),
        ('A cosy dinner and a beautiful walk', 'Paris'),
        ('Trying a tiny restaurant down a side street', 'Tokyo'),
        ('Sharing food and chatting for hours', 'Barcelona')]),
    ('What fills your camera roll?', [
        ('Ocean views and outdoor adventures', 'Sydney'),
        ('Beautiful buildings and little cafe tables', 'Paris'),
        ('Street details, signs and unusual designs', 'Tokyo'),
        ('Colourful streets and pictures with friends', 'Barcelona'),
        ('Skyline views and big city moments', 'New York')]),
    ('Pick something to bring home.', [
        ('An art print or an old book', 'Paris'),
        ('Beautiful stationery or an unusual design object', 'Tokyo'),
        ('Colourful handmade ceramics', 'Barcelona'),
        ('A record or a souvenir from a live show', 'New York'),
        ('A beach tote for my next outdoor day', 'Sydney')]),
    ('What do you value most in a city?', [
        ('Discovery and interesting contrasts', 'Tokyo'),
        ('Community and a social atmosphere', 'Barcelona'),
        ('Energy and endless possibilities', 'New York'),
        ('Nature and a balanced lifestyle', 'Sydney'),
        ('Beauty and creative inspiration', 'Paris')]),
    ('Choose your ideal weekend activity.', [
        ('A long lunch and exploring with friends', 'Barcelona'),
        ('An exhibition followed by live music', 'New York'),
        ('A coastal hike with a picnic stop', 'Sydney'),
        ('A museum visit and a quiet cafe', 'Paris'),
        ('A food adventure in a new neighbourhood', 'Tokyo')]),
    ('Your travel style is closest to...', [
        ('Make a list: I want to experience everything', 'New York'),
        ('Follow the weather and find somewhere outdoors', 'Sydney'),
        ('Leave time to wander and soak up the atmosphere', 'Paris'),
        ('Seek out things I cannot find at home', 'Tokyo'),
        ('Go with friends and see where the day takes us', 'Barcelona')]),
    ('Which feeling would you like more of?', [
        ('Fresh air and freedom', 'Sydney'),
        ('Romance and creative inspiration', 'Paris'),
        ('Curiosity and surprise', 'Tokyo'),
        ('Warmth and connection', 'Barcelona'),
        ('Momentum and possibility', 'New York')]),
]


# Each city starts at zero before the saved answers are counted.
# (Python tutorial: Data Structures; More Control Flow Tools)
def calculate_scores():
    scores = {}
    for city in CITIES:
        scores[city] = 0
    for city in answers:
        scores[city] = scores[city] + 1
    return scores


# Screen changes remove old widgets without changing the saved answers.
def clear_screen():
    for widget in content.winfo_children():
        widget.destroy()
    canvas.yview_moveto(0)


# Labels share the same spacing, wrapping and font throughout the quiz.
# (Python documentation: Tkinter; TkDocs tutorial: Tk Concepts)
def add_label(text, size=14, colour=INK, bold=False):
    weight = 'normal'
    if bold:
        weight = 'bold'
    label = tk.Label(content, text=text, bg=BG, fg=colour,
                     font=('Helvetica', size, weight),
                     wraplength=530, justify='center')
    label.pack(fill='x', pady=9)


# Answer buttons fill the width; navigation uses a separate pink control.
def add_button(text, action, navigation=False):
    if navigation:
        # A coloured label provides consistent navigation colouring on macOS too.
        button = tk.Label(content, text=text, bg=ACCENT, fg='white',
                          font=('Helvetica', 12), padx=16, pady=10,
                          cursor='hand2', takefocus=True, highlightthickness=2,
                          highlightbackground=BG, highlightcolor=INK)
        button.pack(anchor='w', pady=(22, 5))
        # Click, Enter and Space all run the same navigation action.
        # (TkDocs tutorial: Tk Concepts; Python tutorial: Lambda Expressions)
        for event in ('<Button-1>', '<Return>', '<space>'):
            button.bind(event, lambda event: action())
    else:
        # The action runs on a click, rather than when this button is created.
        button = ttk.Button(content, text=text, command=action, padding=(12, 11))
        button.pack(fill='x', pady=5)


# The same photo file supplies a home thumbnail and a larger result image.
def show_photo(parent, city, size):
    path = BASE / 'images' / CITIES[city]['image']
    if Image is None or not path.exists():
        return False
    try:
        # Orientation is corrected before the photo is cropped to its display size.
        # (Pillow documentation: ImageOps)
        with Image.open(path) as photo:
            photo = ImageOps.exif_transpose(photo).convert('RGB')
            photo = ImageOps.fit(photo, size)
        # This converts the photo into an image that Tkinter can display.
        # (Pillow documentation: ImageTk)
        picture = ImageTk.PhotoImage(photo)
        label = tk.Label(parent, image=picture, bg=BG)
        # The reference keeps the picture available while its label is displayed.
        # (Python documentation: Tkinter — Images)
        label.image = picture
        label.pack(pady=10)
        return True
    except (OSError, ValueError):
        # An unreadable image produces a placeholder instead of stopping the quiz.
        # (Python tutorial: Handling Exceptions)
        return False


# The welcome screen introduces the quiz and previews the five destinations.
def show_home():
    clear_screen()
    add_label('A LITTLE ESCAPE', 12, ACCENT, True)
    add_label('What City Are You?', 34, bold=True)
    add_label('Find a destination that feels like you.', 18)
    add_label('10 questions. 5 cities. Your next daydream.', 14)
    add_label('Choose the answers that feel most like you.\nThere are no right or wrong answers.')

    # Each city has one small photo card in a single row.
    gallery = tk.Frame(content, bg=BG)
    gallery.pack(pady=5)
    for city in CITIES:
        card = tk.Frame(gallery, bg=BG)
        card.pack(side='left', padx=3)
        if not show_photo(card, city, (96, 80)):
            placeholder = tk.Canvas(card, width=96, height=80,
                                    bg=CITIES[city]['colour'], highlightthickness=0)
            placeholder.pack(pady=10)
        caption = tk.Label(card, text=city, bg=BG, fg=INK, font=('Helvetica', 11))
        caption.pack()

    add_button('Find my city', restart)
    add_label('A playful travel quiz, for inspiration only.', 11)


# A new game clears all choices, so the next score calculation starts fresh.
# (Python tutorial: Data Structures — List Methods)
def restart():
    answers.clear()
    show_question()


# Removing the last choice prevents its point from surviving an answer change.
# (Python tutorial: Data Structures — List Methods)
def go_back():
    if answers:
        answers.pop()
    show_question()


# An answer records its city, then advances the quiz or opens the results.
# (Python tutorial: Data Structures; More Control Flow Tools)
def choose_answer(city):
    answers.append(city)
    if len(answers) < len(QUESTIONS):
        show_question()
    else:
        finish_quiz()


# The number of saved answers determines the question currently displayed.
def show_question():
    clear_screen()
    index = len(answers)
    add_label('YOUR NEXT CHAPTER', 12, ACCENT, True)
    add_label(f'Question {index + 1} of {len(QUESTIONS)}', 13)
    progress = ttk.Progressbar(content, maximum=len(QUESTIONS), value=index)
    progress.pack(fill='x', pady=12)
    add_label(f'{index} of {len(QUESTIONS)} answered', 11)

    # Each question contains its wording and its list of answer-city pairs.
    question, options = QUESTIONS[index]
    add_label(question, 24, bold=True)
    for text, city in options:
        # city=city remembers this button's city until the player clicks it.
        # (Python tutorial: Lambda Expressions; Default Argument Values)
        add_button(text, lambda city=city: choose_answer(city))
    if index > 0:
        add_button('Back one question', go_back, navigation=True)


# All top-scoring cities are collected in their stored order to detect ties.
# (Python tutorial: More Control Flow Tools; Data Structures)
def finish_quiz():
    scores = calculate_scores()
    highest = max(scores.values())
    leaders = []
    for city in scores:
        if scores[city] == highest:
            leaders.append(city)

    # One winner opens a result; tied winners produce a final mood choice.
    if len(leaders) == 1:
        show_result(leaders[0])
    else:
        clear_screen()
        add_label('ONE LAST CHOICE', 12, ACCENT, True)
        progress = ttk.Progressbar(content, maximum=10, value=10)
        progress.pack(fill='x', pady=12)
        add_label('You have a mix of city energies.', 26, bold=True)
        add_label('Your top scores are tied. Which mood appeals most right now?')
        for city in leaders:
            # The tie choice selects a result without adding a scored answer.
            # (Python tutorial: Lambda Expressions; Default Argument Values)
            add_button(CITIES[city]['tag'], lambda city=city: show_result(city, tied=True))
        add_button('Change my last answer', go_back, navigation=True)


# The result uses the selected city's text, colour and a single larger photo.
def show_result(city, tied=False):
    clear_screen()
    details = CITIES[city]
    add_label('YOUR CITY MATCH', 12, details['colour'], True)
    add_label(city, 36, details['colour'], True)
    add_label(details['tag'], 19, bold=True)

    # A coloured banner appears when the result photo cannot be displayed.
    if not show_photo(content, city, (520, 210)):
        banner = tk.Canvas(content, height=150, bg=details['colour'], highlightthickness=0)
        banner.pack(fill='x', pady=10)
        banner.create_text(25, 60, text=city.upper(), anchor='w', fill='white',
                           font=('Helvetica', 28, 'bold'))
        banner.create_text(25, 105, text='YOUR NEXT DAYDREAM', anchor='w', fill='white',
                           font=('Helvetica', 12))
        add_label('Photo placeholder: add images/' + details['image'], 10)

    add_label(details['description'])
    add_label('Your ideal day', 17, details['colour'], True)
    add_label(details['activities'], 13)
    add_button('Take the quiz again', restart)
    add_button('Back to welcome', show_home)
    add_label('A creative personality match, not a scientific assessment.', 10)


# These two callbacks keep all content reachable when the window is resized.
# (TkDocs tutorial: Canvas; Tk Concepts)
def update_scroll_area(event):
    canvas.configure(scrollregion=canvas.bbox('all'))


def resize_content(event):
    canvas.itemconfigure(content_window, width=event.width)


# The window is created only when this program is run directly.
if __name__ == '__main__':
    root = tk.Tk()
    root.title('What City Are You?')
    root.geometry('800x760')
    root.minsize(620, 600)
    root.configure(bg=BG)

    # The canvas and scrollbar keep longer screens usable on smaller displays.
    # (TkDocs tutorial: Canvas)
    canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)
    content = tk.Frame(canvas, bg=BG, padx=32, pady=24)
    content_window = canvas.create_window((0, 0), window=content, anchor='nw')
    content.bind('<Configure>', update_scroll_area)
    canvas.bind('<Configure>', resize_content)

    # The welcome screen appears first, then the event loop responds to clicks.
    # (Python documentation: Tkinter; TkDocs tutorial: Tk Concepts)
    show_home()
    root.mainloop()
