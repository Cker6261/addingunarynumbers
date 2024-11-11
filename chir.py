import tkinter as tk
from tkinter import messagebox

class TuringMachine:
    def __init__(self, tape, blank_symbol='_'):
        self.tape = list(tape) + [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head = 0
        self.current_state = 'q0'
        self.transition_table = {
            ('q0', '1'): ('q0', '1', 'R'),
            ('q0', '_'): ('q1', '_', 'R'),
            ('q1', '1'): ('q2', '_', 'L'),
            ('q1', '_'): ('q_accept', '_', 'N'),
            ('q2', '1'): ('q2', '1', 'L'),
            ('q2', '_'): ('q0', '1', 'R'),
        }
        self.transitions_log = []

    def step(self):
        char_under_head = self.tape[self.head]
        action = self.transition_table.get((self.current_state, char_under_head))
        if action:
            new_state, new_char, direction = action
            self.tape[self.head] = new_char
            self.current_state = new_state
            self.transitions_log.append(
                f"{self.head}: ({self.current_state}, {char_under_head}) -> ({new_state}, {new_char}, {direction})"
            )
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head -= 1
            return True
        else:
            return False

    def run(self):
        while self.current_state != 'q_accept':
            if not self.step():
                break
        return ''.join(self.tape).strip(self.blank_symbol)

    def print_transition_table(self):
        print("Transition Table:")
        print("Current State | Symbol | New State | Write Symbol | Move")
        for key, value in self.transition_table.items():
            state, symbol = key
            new_state, write_symbol, move = value
            print(f"{state:^13} | {symbol:^6} | {new_state:^10} | {write_symbol:^12} | {move:^4}")

    def print_tape(self):
        print("Tape after execution:", ''.join(self.tape).strip(self.blank_symbol))

    def print_transitions_log(self):
        print("\nTransitions Log:")
        for log in self.transitions_log:
            print(log)

def process_input():
    unary_input = input_entry.get().strip()
    if not all(c in '1_' for c in unary_input):
        messagebox.showerror("Invalid Input", "Please enter a unary addition problem (e.g., '111_1111').")
    else:
        tm = TuringMachine(unary_input)
        result = tm.run()
        tm.print_transition_table()
        tm.print_tape()
        tm.print_transitions_log()
        output_label.config(text=f"Tape After Execution: {''.join(tm.tape).strip(tm.blank_symbol)}")

# GUI setup
root = tk.Tk()
root.title("Turing Machine Simulator - Unary Addition")
root.geometry("500x300")
root.resizable(False, False)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

input_label = tk.Label(input_frame, text="Enter Unary Addition Problem:")
input_label.pack(side=tk.LEFT, padx=5)

input_entry = tk.Entry(input_frame, width=30)
input_entry.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack(pady=10)

# Output Frame
output_frame = tk.Frame(root)
output_frame.pack(pady=20)

output_label = tk.Label(output_frame, text="", font=("Arial", 12), wraplength=400)
output_label.pack()

root.mainloop()
