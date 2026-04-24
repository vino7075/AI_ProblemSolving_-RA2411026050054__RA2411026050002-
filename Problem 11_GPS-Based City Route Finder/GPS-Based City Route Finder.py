import tkinter as tk
from tkinter import ttk, messagebox
import heapq

class AStarRouteFinder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPS-Based City Route Finder (A* Algorithm)")
        self.geometry("850x600")
        self.configure(bg="#2b2b2b")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(".", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 11))
        self.style.configure("TLabel", background="#2b2b2b", foreground="#ffffff")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#007acc", foreground="#ffffff", borderwidth=0, padding=10)
        self.style.map("TButton", background=[("active", "#005999")])
        self.style.configure("TFrame", background="#2b2b2b")
        self.style.configure("TEntry", fieldbackground="#3c3f41", foreground="#ffffff", borderwidth=0)
        self.setup_ui()
        self.load_sample_data()

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        ttk.Label(input_frame, text="Graph Edges (Node1 Node2 Cost):", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.edges_text = tk.Text(input_frame, height=8, bg="#3c3f41", fg="#ffffff", font=("Consolas", 11), insertbackground="white", relief=tk.FLAT)
        self.edges_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        ttk.Label(input_frame, text="Heuristics (Node Value):", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.heuristics_text = tk.Text(input_frame, height=5, bg="#3c3f41", fg="#ffffff", font=("Consolas", 11), insertbackground="white", relief=tk.FLAT)
        self.heuristics_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        node_frame = ttk.Frame(input_frame)
        node_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(node_frame, text="Start Node:").pack(side=tk.LEFT)
        self.start_entry = ttk.Entry(node_frame, width=10)
        self.start_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(node_frame, text="Goal Node:").pack(side=tk.LEFT)
        self.goal_entry = ttk.Entry(node_frame, width=10)
        self.goal_entry.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Button(input_frame, text="Calculate Optimal Route", command=self.calculate_route).pack(fill=tk.X, pady=10)

        output_frame = ttk.Frame(main_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(output_frame, text="Output:", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        self.output_text = tk.Text(output_frame, bg="#1e1e1e", fg="#4af626", font=("Consolas", 12), insertbackground="white", relief=tk.FLAT, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def load_sample_data(self):
        sample_edges = "A B 1\nA C 4\nB D 2\nB E 5\nC D 1\nD F 3\nE F 1"
        self.edges_text.insert(tk.END, sample_edges)
        
        sample_heuristics = "A 7\nB 6\nC 4\nD 2\nE 1\nF 0"
        self.heuristics_text.insert(tk.END, sample_heuristics)
        
        self.start_entry.insert(0, "A")
        self.goal_entry.insert(0, "F")

    def parse_inputs(self):
        graph = {}
        for line in self.edges_text.get("1.0", tk.END).strip().split('\n'):
            if not line.strip(): continue
            parts = line.split()
            if len(parts) == 3:
                u, v, cost = parts[0], parts[1], float(parts[2])
                if u not in graph: graph[u] = {}
                if v not in graph: graph[v] = {}
                graph[u][v] = cost

        heuristics = {}
        for line in self.heuristics_text.get("1.0", tk.END).strip().split('\n'):
            if not line.strip(): continue
            parts = line.split()
            if len(parts) == 2:
                heuristics[parts[0]] = float(parts[1])

        start = self.start_entry.get().strip()
        goal = self.goal_entry.get().strip()

        return graph, heuristics, start, goal

    def a_star_search(self, graph, heuristics, start, goal):
        open_set = []
        heapq.heappush(open_set, (heuristics.get(start, 0), start))
        came_from = {}
        g_score = {node: float('inf') for node in graph}
        g_score[start] = 0
        explored = []
        explored_set = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current not in explored_set:
                explored.append(current)
                explored_set.add(current)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1], g_score[goal], explored

            for neighbor, cost in graph.get(current, {}).items():
                tentative_g = g_score[current] + cost
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristics.get(neighbor, 0)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None, 0, explored

    def calculate_route(self):
        try:
            graph, heuristics, start, goal = self.parse_inputs()
            
            if not start or not goal:
                raise ValueError("Start and Goal nodes must be provided.")
            if start not in graph:
                raise ValueError("Start node not found in graph.")

            path, cost, explored = self.a_star_search(graph, heuristics, start, goal)

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)

            if path:
                self.output_text.insert(tk.END, "Optimal Path (A*):\n")
                self.output_text.insert(tk.END, " → ".join(path) + "\n\n")
                
                self.output_text.insert(tk.END, "Total Cost:\n")
                if len(path) > 1:
                    cost_breakdown = " + ".join([str(int(graph[path[i]][path[i+1]])) for i in range(len(path)-1)])
                    self.output_text.insert(tk.END, f"{cost_breakdown} = {int(cost)}\n\n")
                else:
                    self.output_text.insert(tk.END, f"{int(cost)}\n\n")

                self.output_text.insert(tk.END, "Nodes Explored:\n")
                self.output_text.insert(tk.END, ", ".join(explored) + "\n")
            else:
                self.output_text.insert(tk.END, "No valid path found.\n\n")
                self.output_text.insert(tk.END, "Nodes Explored:\n")
                self.output_text.insert(tk.END, ", ".join(explored) + "\n")

            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = AStarRouteFinder()
    app.mainloop()
