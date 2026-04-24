# 🧩 Sudoku Solver using CSP Algorithm

A professional Python desktop application built with **Tkinter** that solves Sudoku puzzles using the powerful **Constraint Satisfaction Problem (CSP)** approach with **Backtracking Algorithm**.

This project allows users to play Sudoku, check their answers, generate random boards, and automatically solve puzzles intelligently.

---

## 📌 Project Overview

Sudoku is a logic-based number puzzle where digits **1 to 9** must be placed correctly in a **9×9 grid**.

This project uses **Artificial Intelligence techniques** through:

- 🧠 Constraint Satisfaction Problem (CSP)
- 🔁 Backtracking Search
- ✅ Rule Validation

It provides an interactive graphical interface for solving Sudoku.

---

## ✨ Features

✅ User-friendly GUI using Tkinter  
✅ Random Sudoku board generator  
✅ Manual puzzle solving mode  
✅ Check user solution instantly  
✅ Solve puzzle automatically using CSP  
✅ Highlights solved values in green  
✅ Pre-filled numbers locked in blue  
✅ Clean and professional interface  

---

## 🧠 Algorithm Used

### Constraint Satisfaction Problem (CSP)

Sudoku is modeled as a CSP where:

- Variables = Empty Cells  
- Domain = Numbers 1 to 9  
- Constraints:
  - No repetition in Row  
  - No repetition in Column  
  - No repetition in 3×3 Box  

### Backtracking Search

The solver tries values recursively and backtracks when constraints fail.

---

## 🖥️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Core Programming |
| Tkinter | GUI Interface |
| CSP | AI Problem Solving |
| Backtracking | Puzzle Solver |

---

## 📂 Project Structure

```text
Sudoku-CSP-Solver/
│── main.py
│── README.md
