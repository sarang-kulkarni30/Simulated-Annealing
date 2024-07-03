import numpy
import cv2
import tkinter as tk
from tkinter import messagebox

# Constants for visualization
WIDTH = 640
HEIGHT = 480
FONT = cv2.FONT_HERSHEY_DUPLEX
SIZE = 0.7
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

# Functions for simulated annealing
def Generate(width, height, count):
    cities = []
    for i in range(count):
        position_x = numpy.random.randint(width)
        position_y = numpy.random.randint(height)
        cities.append((position_x, position_y))
    return cities

def Initialize(count):
    solution = numpy.arange(count)
    numpy.random.shuffle(solution)
    return solution

def Evaluate(cities, solution):
    distance = 0
    for i in range(len(cities)):
        index_a = solution[i]
        index_b = solution[i - 1]
        delta_x = cities[index_a][0] - cities[index_b][0]
        delta_y = cities[index_a][1] - cities[index_b][1]
        distance += (delta_x ** 2 + delta_y ** 2) ** 0.5
    return distance

def Modify(current):
    new = current.copy()
    index_a = numpy.random.randint(len(current))
    index_b = numpy.random.randint(len(current))
    while index_b == index_a:
        index_b = numpy.random.randint(len(current))
    new[index_a], new[index_b] = new[index_b], new[index_a]
    return new

def Draw(width, height, cities, solution, infos):
    frame = numpy.zeros((height, width, 3))
    for i in range(len(cities)):
        index_a = solution[i]
        index_b = solution[i - 1]
        point_a = (cities[index_a][0], cities[index_a][1])
        point_b = (cities[index_b][0], cities[index_b][1])
        cv2.line(frame, point_a, point_b, GREEN, 2)
    for city in cities:
        cv2.circle(frame, (city[0], city[1]), 5, RED, -1)
    cv2.putText(frame, f"Temperature", (25, 50), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Score", (25, 75), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Best Score", (25, 100), FONT, SIZE, WHITE)
    cv2.putText(frame, f"Worst Score", (25, 125), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[0]:.2f}", (175, 50), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[1]:.2f}", (175, 75), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[2]:.2f}", (175, 100), FONT, SIZE, WHITE)
    cv2.putText(frame, f": {infos[3]:.2f}", (175, 125), FONT, SIZE, WHITE)
    cv2.imshow("Simulated Annealing", frame)
    cv2.waitKey(5)

def start_simulated_annealing(width, height, city_count, initial_temp, stopping_temp, temp_decay):
    cities = Generate(width, height, city_count)
    current_solution = Initialize(city_count)
    current_score = Evaluate(cities, current_solution)
    best_score = worst_score = current_score
    temperature = initial_temp
    while (temperature > stopping_temp):
        new_solution = Modify(current_solution)
        new_score = Evaluate(cities, new_solution)
        best_score = min(best_score, new_score)
        worst_score = max(worst_score, new_score)
        if new_score < current_score:
            current_solution = new_solution
            current_score = new_score
        else:
            delta = new_score - current_score
            probability = numpy.exp(-delta / temperature)
            if probability > numpy.random.uniform():
                current_solution = new_solution
                current_score = new_score
        temperature *= temp_decay
        infos = (temperature, current_score, best_score, worst_score)
        Draw(width, height, cities, current_solution, infos)

def run_simulated_annealing():
    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        city_count = int(entry_city_count.get())
        initial_temp = float(entry_initial_temp.get())
        stopping_temp = float(entry_stopping_temp.get())
        temp_decay = float(entry_temp_decay.get())
        
        start_simulated_annealing(width, height, city_count, initial_temp, stopping_temp, temp_decay)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Create the Tkinter GUI
root = tk.Tk()
root.title("Simulated Annealing Parameters")

# Input fields
label_width = tk.Label(root, text="Enter the width of the area:")
label_width.pack()
entry_width = tk.Entry(root)
entry_width.pack()

label_height = tk.Label(root, text="Enter the height of the area:")
label_height.pack()
entry_height = tk.Entry(root)
entry_height.pack()

label_city_count = tk.Label(root, text="Enter the number of cities:")
label_city_count.pack()
entry_city_count = tk.Entry(root)
entry_city_count.pack()

label_initial_temp = tk.Label(root, text="Enter the initial temperature:")
label_initial_temp.pack()
entry_initial_temp = tk.Entry(root)
entry_initial_temp.pack()

label_stopping_temp = tk.Label(root, text="Enter the stopping temperature:")
label_stopping_temp.pack()
entry_stopping_temp = tk.Entry(root)
entry_stopping_temp.pack()

label_temp_decay = tk.Label(root, text="Enter the temperature decay rate:")
label_temp_decay.pack()
entry_temp_decay = tk.Entry(root)
entry_temp_decay.pack()

# Start button
button_start = tk.Button(root, text="Start Simulated Annealing", command=run_simulated_annealing)
button_start.pack()

root.mainloop()
