import tkinter as tk
from tkinter import messagebox
import random 

BOARDS = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],

    [
        [0, 4, 0, 2, 0, 1, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 5, 0, 0, 0, 3, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 7, 0, 8, 0, 1, 0, 4],
        [0, 1, 0, 0, 0, 0, 0, 9, 0],
        [0, 0, 1, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 7, 0, 5, 0, 0, 0],
        [6, 0, 8, 9, 0, 4, 5, 0, 3]
    ],

    [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0],
        [5, 0, 0, 7, 0, 3, 0, 0, 8],
        [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 7],
        [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]
]

class SudokuCSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver (CSP)")
        self.cells = {}
        self.create_grid()
        self.create_buttons()
        self.load_random_board() 
    def create_grid(self):
        """Creates the 9x9 GUI grid with thicker borders for 3x3 subgrids."""
        frame = tk.Frame(self.root, bg='black')
        frame.pack(padx=10, pady=10)

        for row in range(9):
            for col in range(9):
                pady = (1, 3) if row % 3 == 2 and row != 8 else 1
                padx = (1, 3) if col % 3 == 2 and col != 8 else 1

                cell = tk.Entry(frame, width=2, font=('Arial', 24, 'bold'), justify='center')
                cell.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")
                self.cells[(row, col)] = cell

    def create_buttons(self):
        """Creates the interactive control buttons."""
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        check_btn = tk.Button(btn_frame, text="Check Solution", command=self.check_solution, font=('Arial', 12))
        check_btn.grid(row=0, column=0, padx=5)

        solve_btn = tk.Button(btn_frame, text="Solve using CSP", command=self.solve_csp, font=('Arial', 12))
        solve_btn.grid(row=0, column=1, padx=5)

        # Updated to trigger the random board function
        reset_btn = tk.Button(btn_frame, text="New Random Board", command=self.load_random_board, font=('Arial', 12))
        reset_btn.grid(row=0, column=2, padx=5)

    def load_random_board(self):
        """Selects a random board from the BOARDS list and loads it."""
        board = random.choice(BOARDS)
        self.load_board(board)

    def load_board(self, board):
        """Loads a board state into the GUI, marking pre-filled numbers as read-only."""
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].config(state='normal')
                self.cells[(row, col)].delete(0, tk.END)
                val = board[row][col]
                if val != 0:
                    self.cells[(row, col)].insert(0, str(val))
                    self.cells[(row, col)].config(state='readonly', disabledforeground='blue', fg='blue') 
                else:
                    self.cells[(row, col)].config(fg='black')

    def get_current_board(self):
        """Reads the current user input from the GUI and returns a 2D array."""
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.cells[(row, col)].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    current_row.append(int(val))
                else:
                    current_row.append(0)
            board.append(current_row)
        return board

    def update_gui_from_board(self, board):
        """Updates empty GUI cells with the solved CSP numbers."""
        for row in range(9):
            for col in range(9):
                if self.cells[(row, col)].get() == "":
                     self.cells[(row, col)].insert(0, str(board[row][col]))
                     self.cells[(row, col)].config(fg='green') 

    def is_valid_constraint(self, board, row, col, num):
        """Checks if placing 'num' at (row, col) violates any CSP constraints."""
        if num in board[row]:
            return False

        for r in range(9):
            if board[r][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def solve_csp_backtracking(self, board):
        """Standard backtracking algorithm to solve the CSP."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_constraint(board, row, col, num):
                            board[row][col] = num 
                            if self.solve_csp_backtracking(board):
                                return True
                            board[row][col] = 0
                    return False 
        return True 

    def check_solution(self):
        """Evaluates the user's manual inputs."""
        board = self.get_current_board()
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    messagebox.showwarning("Incomplete", "Please fill all cells before checking.")
                    return

        valid = True
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                board[row][col] = 0 
                if not self.is_valid_constraint(board, row, col, num):
                    valid = False
                    break
                board[row][col] = num
            if not valid:
                break

        if valid:
            messagebox.showinfo("Result", "You won!")
        else:
            messagebox.showerror("Result", "Try again.")

    def solve_csp(self):
        """Handler for the 'Solve using CSP' button."""
        board = self.get_current_board()
        if self.solve_csp_backtracking(board):
            self.update_gui_from_board(board)
            messagebox.showinfo("Solved", "The Sudoku was successfully solved using the CSP approach.")
        else:
            messagebox.showerror("Error", "No valid solution exists for the current configuration.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuCSPApp(root)
    root.mainloop()
