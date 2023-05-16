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
is_user_turn = False
current_colors = []  # Variable to store the sequence of colors selected by the game
user_colors = []  # Variable to store the sequence of colors clicked by the user

# Create a function to start the game
def start():
    global score, is_game_running, is_user_turn
    # Check if the user has input his/her name
    if chatbox.get() == '':
        # update the label
        label1.config(text='Please enter your name')
    elif not is_game_running:
        is_game_running = True
        button.config(state=tk.DISABLED)
        score = 0
        update_score()
        is_user_turn = False  # Reset user turn
        change_colors()

# Create a function to get the original color of a rectangle
def get_original_color(rect):
    if rect == 'rect1':
        return 'red'
    elif rect == 'rect2':
        return 'green'
    elif rect == 'rect3':
        return 'yellow'
    elif rect == 'rect4':
        return 'blue'
    
# Create function to choose a random rectangle and change its color for 1 second and then change back to its original color
def change_colors():
    global current_colors, is_user_turn
    is_user_turn = False  # Disable user input during the color sequence
    # Choose a random rectangle
    rect = random.choice(['rect1', 'rect2', 'rect3', 'rect4'])
    # Add the chosen color to the sequence
    current_colors.append(rect)
    # Change the color of the rectangles in the sequence
    for color in current_colors:
        rect_id = canvas.find_withtag(color)[0]  # Get the ID of the rectangle
        canvas.itemconfig(rect_id, fill='white')
        window.update()
        time.sleep(1)
        canvas.itemconfig(rect_id, fill=get_original_color(color))
        window.update()
        time.sleep(0.5)

    # Enable user input
    is_user_turn = True
    user_colors.clear()  # Clear user's sequence

# Create a function to check if the user has clicked on the correct sequence of colors
def check(event):
    global score, is_game_running, user_colors, is_user_turn
    if is_user_turn:
        # Get the tags of the item that the user has clicked on
        tags = canvas.gettags(tk.CURRENT)
        # Change the color of the rectangle temporarily
        rect_id = canvas.find_withtag(tags[0])[0]  # Get the ID of the rectangle
        canvas.itemconfig(rect_id, fill='white')
        window.update()
        time.sleep(0.2)
        canvas.itemconfig(tags[0], fill=get_original_color(tags[0]))
        # Add the clicked color to the user's sequence
        user_colors.append(tags[0])
        # Check if the user's sequence matches the current sequence
        if user_colors == current_colors:
            score += 1
            update_score()
            user_colors = []  # Reset the user's sequence
            window.after(1000, change_colors)
        elif len(user_colors) == len(current_colors):
            end_game()  # If the user's sequence length is equal to the current sequence length but not matching, end the game

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
        scores.sort(reverse=True)  # Sort scores in descending order
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

# Bind the rectangles to the check function
canvas.tag_bind('rect1', '<Button-1>', check)
canvas.tag_bind('rect2', '<Button-1>', check)
canvas.tag_bind('rect3', '<Button-1>', check)
canvas.tag_bind('rect4', '<Button-1>', check)

# When the program is running, the window will not be closed
window.mainloop()