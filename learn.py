# Import tkinter, os, time, random
import tkinter as tk
import os
import time
import random

scores_file = os.path.join(os.path.dirname(__file__), 'scores.txt')


# Create a window
window = tk.Tk()
window.title('Simon Says')
window.geometry('500x500')

# Create a label
label = tk.Label(window, text='Simon Says', font=('Arial', 12), width=30, height=2)
label.pack()

# Create a frame
frame = tk.Frame(window)
frame.pack()

# Create a canvas
canvas = tk.Canvas(frame, bg='white', width=300, height=200)
canvas.pack(side='left')

# Create a button
button = tk.Button(frame, text='Start', font=('Arial', 12), width=10, height=2)
button.pack(side='right')

# draw 4 rectangles with different colors on the canvas, takes all the space of the canvas and attribute id to each rectangle
rect1 = canvas.create_rectangle(0, 0, 150, 100, fill='red', tags='rect1')
rect2 = canvas.create_rectangle(150, 0, 300, 100, fill='green', tags='rect2')
rect3 = canvas.create_rectangle(0, 100, 150, 200, fill='yellow', tags='rect3')
rect4 = canvas.create_rectangle(150, 100, 300, 200, fill='blue', tags='rect4')

# Create chatbox for user to input his/her name
chatbox = tk.Entry(window, show=None, font=('Arial', 14), width=20)
chatbox.pack()

# Create a label
label1 = tk.Label(window, text='Enter your name', font=('Arial', 12), width=30, height=2)
label1.pack()

# Create a label for the score
label_score = tk.Label(window, text='Score: ', font=('Arial', 12), width=30, height=2)
label_score.pack()

score = 0
is_game_running = False
current_color = ''  # Variable to store the color of the rectangle selected by the game

# Create a function to start the game
def start():
    global score, is_game_running
    # Check if the user has input his/her name
    if chatbox.get() == '':
        # update the label
        label1.config(text='Please enter your name')
    elif not is_game_running:
        is_game_running = True
        button.config(state=tk.DISABLED)
        score = 0
        update_score()
        change_color()

# Create function to choose a random rectangle and change its color for 1 second and then change back to its original color
def change_color():
    global current_color
    # Choose a random rectangle
    rect = random.choice(['rect1', 'rect2', 'rect3', 'rect4'])
    # Change the color of the rectangle
    canvas.itemconfig(rect, fill='white')
    # Update the current color
    current_color = rect
    # Wait for 1 second
    window.after(1000, lambda: restore_color(rect))
    # Create a function to restore the color of a rectangle
def restore_color(rect):
    # Change the color of the rectangle back to its original color (red, green, yellow, or blue)
    if rect == 'rect1':
        canvas.itemconfig(rect1, fill='red')
    elif rect == 'rect2':
        canvas.itemconfig(rect2, fill='green')
    elif rect == 'rect3':
        canvas.itemconfig(rect3, fill='yellow')
    elif rect == 'rect4':
        canvas.itemconfig(rect4, fill='blue')
    # Enable user input
    canvas.bind('<Button-1>', check)

# Create a function to check if the user has clicked on the correct rectangle
def check(event):
    global score, is_game_running
    # Disable user input
    canvas.unbind('<Button-1>')
    # Get the tags of the item that the user has clicked on
    tags = canvas.gettags(tk.CURRENT)
    # Check if the user has clicked on the correct rectangle
    if tags[0] == current_color:
        score += 1
        update_score()
        # Change the color of the rectangle back to its original color after a short delay
        window.after(500, change_color)
    else:
        end_game()

# Update the score label
def update_score():
    label_score.config(text='Score: ' + str(score))

# End the game
def end_game():
    global is_game_running
    label_score.config(text='Game Over')
    is_game_running = False
    button.config(state=tk.NORMAL)
    # Disable user input
    canvas.unbind('<Button-1>')
    # Save the score to the scores file
    save_score(score, chatbox.get())

def save_score(score, name):
    # Load existing scores from the file
    existing_scores = load_scores()
    # Add the new score
    existing_scores.append((score, name))
    # Sort the scores by descending order
    existing_scores.sort(reverse=True)
    # Keep only the top 10 scores
    existing_scores = existing_scores[:10]
    # Save the updated scores to the file
    with open(scores_file, 'w') as file:
        for score, name in existing_scores:
            file.write(f'{score},{name}\n')
def load_scores():
    scores = []
    if os.path.isfile(scores_file):
        with open(scores_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    score, name = line.split(',')
                    scores.append((int(score), name))
        scores.sort(reverse=True)  # Tri des scores par ordre décroissant
    return scores

def show_scores():
    scores = load_scores()
    scores_window = tk.Toplevel(window)
    scores_window.title('Top 10 Scores')
    scores_window.geometry('300x200')
    # Create a label for each score
    for i, (score, name) in enumerate(scores):
        label = tk.Label(scores_window, text=f'{i+1}. {name}: {score}', font=('Arial', 12))
        label.pack()

scores_button = tk.Button(window, text='Scores', font=('Arial', 12), width=10, height=2, command=show_scores)
scores_button.pack()

# Bind the chatbox to the function
chatbox.bind('<Return>', lambda event: start())

# Bind the button to the function
button.config(command=start)



# When the program is running, the window will not be closed
window.mainloop()
