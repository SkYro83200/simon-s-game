import tkinter as tk
import os
import time
import random

scores_file = os.path.join(os.path.dirname(__file__), 'scores.txt')

# Define the original and darker colors
original_colors = {
    'rect1': 'red',
    'rect2': 'green',
    'rect3': 'yellow',
    'rect4': 'blue'
}
darker_colors = {
    'rect1': '#800000',  # Dark red
    'rect2': '#004d00',  # Dark green
    'rect3': '#808000',  # Dark yellow
    'rect4': '#000080'   # Dark blue
}

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

# Draw 4 rectangles with different colors on the canvas, taking all the space of the canvas and assigning an ID to each rectangle
rect1 = canvas.create_rectangle(0, 0, 150, 100, fill=original_colors['rect1'], tags='rect1')
rect2 = canvas.create_rectangle(150, 0, 300, 100, fill=original_colors['rect2'], tags='rect2')
rect3 = canvas.create_rectangle(0, 100, 150, 200, fill=original_colors['rect3'], tags='rect3')
rect4 = canvas.create_rectangle(150, 100, 300, 200, fill=original_colors['rect4'], tags='rect4')

# Create chatbox for the user to input his/her name
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
    username = chatbox.get().strip()  # Get the user's input and remove leading/trailing whitespace

    # Check if the user has input a valid name
    if len(username) < 3:
        # Update the label
        label1.config(text='Name should have at least 3 characters')
    elif len(username) > 7:
        # Update the label
        label1.config(text='Name should have at most 7 characters')
    elif any(symbol in username for symbol in "!@#$%^&*()_+={}[]|\:;'<>?,./\""):
        label1.config(text='Name should not contain symbols')
    elif any(word in username.lower() for word in ["violent_word1", "violent_word2", "violent_word3"]):
        # Update the label
        label1.config(text='Name should not contain violent words')
    elif not is_game_running:
        is_game_running = True
        button.config(state=tk.DISABLED)
        score = 0
        update_score()
        is_user_turn = False  # Reset user turn
        animate_colors()  # Call the animation function

# Function to animate the colors at the beginning of the game
def animate_colors():
    global is_user_turn
    is_user_turn = False  # Disable user input during the color sequence

    # Animate the colors
    for rect_color in darker_colors:
        rect_id = canvas.find_withtag(rect_color)[0]  # Get the ID of the rectangle
        canvas.itemconfig(rect_id, fill=darker_colors[rect_color])
        window.update()
        time.sleep(0.5)
        canvas.itemconfig(rect_id, fill=original_colors[rect_color])
        window.update()
        time.sleep(0.2)

    is_user_turn = True  # Enable user input after the animation
    user_colors.clear()  # Clear user's sequence
    change_colors()  # Start the game after the animation

    # Enable user input
    is_user_turn = True
    user_colors.clear()  # Clear user's sequence

def get_original_color(rect):
    return original_colors.get(rect, 'white')

# Create a function to choose a random rectangle and change its color for 1 second and then change back to its original color
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
        canvas.itemconfig(rect_id, fill=darker_colors[color])
        window.update()
        time.sleep(1)
        canvas.itemconfig(rect_id, fill=original_colors[color])
        window.update()
        time.sleep(0.5)

    # Enable user input
    is_user_turn = True
    user_colors.clear()  # Clear user's sequence

def check(event):
    global score, is_game_running, user_colors, is_user_turn
    if is_user_turn:
        # Get the tags of the item that the user has clicked on
        tags = canvas.gettags(tk.CURRENT)
        # Change the color of the rectangle temporarily
        rect_id = canvas.find_withtag(tags[0])[0]  # Get the ID of the rectangle
        canvas.itemconfig(rect_id, fill=darker_colors[tags[0]])
        window.update()
        time.sleep(0.2)
        canvas.itemconfig(tags[0], fill=get_original_color(tags[0]))
        # Add the clicked color to the user's sequence
        user_colors.append(tags[0])
        # Check if it's the first attempt and the user failed
        if len(user_colors) == 1 and user_colors[0] != current_colors[0]:
            end_game()  # End the game if the user failed on the first attempt
        elif user_colors == current_colors:
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