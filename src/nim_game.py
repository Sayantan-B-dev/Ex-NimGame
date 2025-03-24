import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from game_logic import GameLogic

class NimGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NIM Game")
        self.root.geometry("600x450")  # Adjusted for 5 piles
        self.game_logic = GameLogic(num_piles=5, max_pile_size=10)
        self.against_ai = tk.BooleanVar()
        self.selected_pile = tk.IntVar(value=0)
        self.remove_choice = tk.StringVar()

        # Prompt for player names
        self.player1_name = simpledialog.askstring("Player 1", "Enter Player 1's name:", parent=self.root)
        if not self.player1_name:
            self.player1_name = "Player 1"
        self.player2_name = simpledialog.askstring("Player 2", "Enter Player 2's name:", parent=self.root)
        if not self.player2_name:
            self.player2_name = "Player 2"

        # Set ttk style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Turn.TLabel", font=("Arial", 14))

        self.create_menu()
        self.create_canvas()
        self.create_controls()
        self.update_ui()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=lambda: self.new_game(randomize=False))
        game_menu.add_command(label="Randomize Piles", command=lambda: self.new_game(randomize=True))
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Rules", command=self.show_rules)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, width=500, height=250, bg="white")  # Wider for 5 piles
        self.canvas.pack(pady=10)

    def create_controls(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        pile_frame = ttk.Frame(control_frame)
        pile_frame.pack()
        for i in range(5):  # 5 piles
            rb = ttk.Radiobutton(pile_frame, text=f"Pile {i+1}", variable=self.selected_pile,
                                 value=i, command=self.update_remove_choice)
            rb.pack(side="left")

        remove_frame = ttk.Frame(control_frame)
        remove_frame.pack()
        ttk.Label(remove_frame, text="Remove:").pack(side="left")
        self.remove_combobox = ttk.Combobox(remove_frame, textvariable=self.remove_choice,
                                            state="readonly", width=5)
        self.remove_combobox.pack(side="left")
        self.remove_button = ttk.Button(remove_frame, text="Remove", command=self.make_move)
        self.remove_button.pack(side="left")

        ai_frame = ttk.Frame(control_frame)
        ai_frame.pack()
        ttk.Checkbutton(ai_frame, text="Play against computer", variable=self.against_ai).pack()

        self.turn_label = ttk.Label(self.root, text=f"{self.player1_name}'s turn", style="Turn.TLabel")
        self.turn_label.pack(pady=10)

    def update_ui(self):
        self.draw_piles()
        self.update_remove_choice()
        if self.game_logic.is_game_over():
            winner = 1 - self.game_logic.get_current_player()
            winner_name = self.player1_name if winner == 0 else self.player2_name
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            self.remove_button.config(state="disabled")
        else:
            player = self.game_logic.get_current_player()
            player_name = self.player1_name if player == 0 else self.player2_name
            self.turn_label.config(text=f"{player_name}'s turn")

    def draw_piles(self):
        self.canvas.delete("all")
        piles = self.game_logic.get_piles()
        for j in range(5):  # 5 piles
            x = 50 + j * 90  # Adjusted spacing
            # Draw base
            base_color = "yellow" if self.selected_pile.get() == j else "gray"
            self.canvas.create_rectangle(x - 20, 220, x + 20, 225, fill=base_color)
            # Draw sticks
            n = piles[j]
            for k in range(n):
                y_bottom = 220 - k * 22
                y_top = y_bottom - 20
                self.canvas.create_rectangle(x - 5, y_top, x + 5, y_bottom, fill="sienna")
            # Label
            self.canvas.create_text(x, 235, text=f"Pile {j+1}")

    def update_remove_choice(self):
        pile = self.selected_pile.get()
        num_objects = self.game_logic.get_piles()[pile]
        choices = [str(i) for i in range(1, num_objects + 1)]
        self.remove_combobox["values"] = choices
        if choices:
            self.remove_choice.set(choices[0])
            self.remove_button.config(state="normal")
        else:
            self.remove_choice.set("")
            self.remove_button.config(state="disabled")

    def make_move(self):
        pile = self.selected_pile.get()
        if self.remove_choice.get():
            number = int(self.remove_choice.get())
            if self.game_logic.make_move(pile, number):
                self.update_ui()
                if self.against_ai.get() and not self.game_logic.is_game_over() and self.game_logic.get_current_player() == 1:
                    self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        self.game_logic.make_ai_move()
        self.update_ui()

    def new_game(self, randomize=False):
        self.game_logic.reset(randomize=randomize)
        self.update_ui()
        self.remove_button.config(state="normal")

    def show_rules(self):
        messagebox.showinfo("Rules", "The Game of NIM: Two players take turns removing objects "
                                     "from piles. On each turn, a player must remove at least one "
                                     "object from a single pile. The player who removes the last "
                                     "object wins.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = NimGame()
    game.run()