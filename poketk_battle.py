import tkinter as tk
import random
import json
import os

SAVE_FILE = "poketk_save.json"

class PixelLabel(tk.Canvas):
    """A simple canvas to draw pixel-style text with a shadow."""
    def __init__(self, master, text="", font=("Courier", 16, "bold"), fg="white", bg="black", **kwargs):
        super().__init__(master, bg=bg, height=30, **kwargs)
        self.text = text
        self.font = font
        self.fg = fg
        self.bg = bg
        self.bind("<Configure>", self.redraw)

    def redraw(self, event=None):
        self.delete("all")
        # Draw shadow
        self.create_text(2, 18, text=self.text, font=self.font, fill="black", anchor="w")
        # Draw main text
        self.create_text(0, 16, text=self.text, font=self.font, fill=self.fg, anchor="w")

    def set_text(self, text):
        self.text = text
        self.redraw()

class PixelHPBar(tk.Canvas):
    """Draws a pixelated health bar with colors."""
    def __init__(self, master, width=200, height=20, max_hp=100, hp=100, **kwargs):
        super().__init__(master, width=width, height=height, bg="black", **kwargs)
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.hp = hp
        self.redraw()

    def redraw(self):
        self.delete("all")
        block_w = 4
        blocks = self.width // block_w
        hp_blocks = int(blocks * (self.hp / self.max_hp)) if self.max_hp > 0 else 0
        for i in range(blocks):
            x0 = i * block_w
            color = "red" if i < hp_blocks else "grey20"
            self.create_rectangle(x0, 0, x0 + block_w - 1, self.height, fill=color, outline="black")

    def update_hp(self, hp):
        self.hp = max(0, hp)
        self.redraw()

class PokemonBattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 PokéTk Battle - Pixel Edition 🔥")
        self.root.geometry("820x620")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        print("Current working directory:", os.getcwd())
        # No external sprites: everything drawn with code now
        self.setup_game_data()
        self.main_menu()

    def setup_game_data(self):
        self.type_chart = {
            "Fire": {"Grass": 2.0, "Electric": 1.0, "Water": 0.5, "Fire": 0.5, "Normal": 1.0},
            "Electric": {"Water": 2.0, "Grass": 0.5, "Fire": 1.0, "Electric": 0.5, "Normal": 1.0},
            "Grass": {"Water": 2.0, "Fire": 0.5, "Electric": 1.0, "Grass": 0.5, "Normal": 1.0},
            "Normal": {"Fire": 1.0, "Electric": 1.0, "Grass": 1.0, "Normal": 1.0},
            "Flying": {"Grass": 2.0, "Electric": 0.5, "Fire": 1.0, "Flying": 1.0, "Normal": 1.0},
            "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5},
            "Rock": {"Fire": 2.0, "Flying": 2.0, "Water": 0.5, "Grass": 0.5},
            "Ground": {"Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Flying": 0.0},
            "Dark": {"Psychic": 2.0, "Ghost": 2.0, "Fighting": 0.5},
            # etc. Add more if needed
        }

        self.player_pokemon = {
            "name": "Charizard",
            "type": "Fire",
            "level": 5,
            "exp": 0,
            "next_level_exp": 50,
            "max_hp": 120,
            "hp": 120,
            "moves": {
                "Flamethrower": {"power": (25, 35), "type": "Fire"},
                "Slash": {"power": (15, 25), "type": "Normal"},
                "Fly": {"power": (20, 30), "type": "Flying"},
                "Smokescreen": {"power": (5, 10), "type": "Normal"},
            },
            "sprite_key": "fire",
        }

        # Expanded enemy pool with 50 Pokémon generated procedurally
        pokemon_types = ["Fire", "Water", "Grass", "Electric", "Normal", "Flying", "Psychic", "Rock", "Ground", "Dark"]

        basic_moves = {
            "Fire": {"Flamethrower": (25, 35), "Ember": (15, 25)},
            "Water": {"Water Gun": (15, 25), "Bubble": (10, 20)},
            "Grass": {"Vine Whip": (15, 25), "Razor Leaf": (20, 30)},
            "Electric": {"Thunderbolt": (20, 30), "Spark": (15, 25)},
            "Normal": {"Tackle": (10, 20), "Scratch": (10, 20)},
            "Flying": {"Gust": (15, 25), "Peck": (10, 20)},
            "Psychic": {"Confusion": (20, 30), "Psybeam": (25, 35)},
            "Rock": {"Rock Throw": (20, 30), "Smash": (25, 35)},
            "Ground": {"Mud Slap": (15, 25), "Earthquake": (30, 40)},
            "Dark": {"Bite": (15, 25), "Slash": (20, 30)},
        }

        def generate_pokemon(name, poke_type):
            moves = {}
            possible_moves = basic_moves.get(poke_type, basic_moves["Normal"])
            selected_moves = random.sample(list(possible_moves.items()), k=2)
            for mv_name, power_range in selected_moves:
                moves[mv_name] = {"power": power_range, "type": poke_type}
            max_hp = random.randint(90, 130)
            return {
                "name": name,
                "type": poke_type,
                "max_hp": max_hp,
                "hp": max_hp,
                "moves": moves,
                "sprite_key": poke_type.lower()
            }

        pokemon_names = [
            "Pidgey", "Rattata", "Zubat", "Geodude", "Onix", "Psyduck", "Growlithe", "Poliwag",
            "Abra", "Machop", "Magnemite", "Gastly", "Krabby", "Voltorb", "Exeggcute", "Cubone",
            "Hitmonlee", "Koffing", "Rhyhorn", "Horsea", "Goldeen", "Staryu", "Scyther", "Jynx",
            "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto",
            "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Kabuto", "Aerodactyl",
            "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"
        ]

        self.enemy_pool = [generate_pokemon(name, random.choice(pokemon_types)) for name in pokemon_names]

        self.message_queue = []
        self.load_game()

    def save_game(self):
        data = {
            "player": {
                "level": self.player_pokemon["level"],
                "exp": self.player_pokemon["exp"]
            }
        }
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
            print("Game saved.")
        except Exception as e:
            print(f"Failed to save game: {e}")

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    pl = data.get("player", {})
                    self.player_pokemon["level"] = pl.get("level", self.player_pokemon["level"])
                    self.player_pokemon["exp"] = pl.get("exp", self.player_pokemon["exp"])
                    print(f"Loaded player level {self.player_pokemon['level']} exp {self.player_pokemon['exp']}")
            except Exception as e:
                print(f"Failed to load save file: {e}")

    def main_menu(self):
        self.clear_root()
        title = PixelLabel(self.root, text="🔥 PokéTk Battle 🔥", font=("Courier", 24, "bold"), fg="orange")
        title.pack(pady=10)
        start_btn = tk.Button(self.root, text="Start Battle", font=("Courier", 18), command=self.start_battle)
        start_btn.pack(pady=15)
        quit_btn = tk.Button(self.root, text="Quit", font=("Courier", 18), command=self.root.quit)
        quit_btn.pack(pady=5)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_battle(self):
        self.clear_root()
        self.enemy_pokemon = random.choice(self.enemy_pool)
        self.player_pokemon["hp"] = self.player_pokemon["max_hp"]
        self.enemy_pokemon["hp"] = self.enemy_pokemon["max_hp"]
        self.battle_frame = tk.Frame(self.root, bg="#111111")
        self.battle_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Player info
        player_info = tk.Frame(self.battle_frame, bg="#111111")
        player_info.grid(row=0, column=0, sticky="w")

        self.player_name_label = PixelLabel(player_info, text=self.player_pokemon["name"], fg="yellow", font=("Courier", 20, "bold"))
        self.player_name_label.pack(anchor="w")
        self.player_hp_bar = PixelHPBar(player_info, max_hp=self.player_pokemon["max_hp"], hp=self.player_pokemon["hp"])
        self.player_hp_bar.pack(anchor="w", pady=5)
        self.player_sprite = tk.Canvas(player_info, width=120, height=120, bg="#222222", highlightthickness=0)
        self.player_sprite.pack(pady=10)
        self.draw_pokemon_sprite(self.player_sprite, self.player_pokemon)

        # Enemy info
        enemy_info = tk.Frame(self.battle_frame, bg="#111111")
        enemy_info.grid(row=0, column=1, sticky="e", padx=100)

        self.enemy_name_label = PixelLabel(enemy_info, text=self.enemy_pokemon["name"], fg="red", font=("Courier", 20, "bold"))
        self.enemy_name_label.pack(anchor="e")
        self.enemy_hp_bar = PixelHPBar(enemy_info, max_hp=self.enemy_pokemon["max_hp"], hp=self.enemy_pokemon["hp"])
        self.enemy_hp_bar.pack(anchor="e", pady=5)
        self.enemy_sprite = tk.Canvas(enemy_info, width=120, height=120, bg="#222222", highlightthickness=0)
        self.enemy_sprite.pack(pady=10)
        self.draw_pokemon_sprite(self.enemy_sprite, self.enemy_pokemon)

        # Battle text
        self.battle_text = tk.Text(self.battle_frame, height=8, width=60, bg="#222222", fg="white", font=("Courier", 14), state="disabled")
        self.battle_text.grid(row=1, column=0, columnspan=2, pady=15)

        # Moves buttons
        self.moves_frame = tk.Frame(self.battle_frame, bg="#111111")
        self.moves_frame.grid(row=2, column=0, columnspan=2)

        self.move_buttons = []
        for move in self.player_pokemon["moves"]:
            btn = tk.Button(self.moves_frame, text=move, font=("Courier", 14), width=15,
                            command=lambda m=move: self.player_move(m))
            btn.pack(side="left", padx=5, pady=5)
            self.move_buttons.append(btn)

        self.message_queue = []
        self.battle_turn = "player"  # player or enemy
        self.append_battle_text(f"A wild {self.enemy_pokemon['name']} appeared!")
        self.update_buttons_state(True)

    def draw_pokemon_sprite(self, canvas, pokemon):
        colors = {
            "fire": "#ff4500",
            "water": "#1e90ff",
            "grass": "#32cd32",
            "electric": "#ffd700",
            "normal": "#d3d3d3",
            "flying": "#87ceeb",
            "psychic": "#ee82ee",
            "rock": "#a0522d",
            "ground": "#deb887",
            "dark": "#2f4f4f",
        }
        color = colors.get(pokemon["sprite_key"], "#555555")
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 120, 120, fill=color)
        canvas.create_text(60, 60, text=pokemon["name"], fill="white", font=("Courier", 14, "bold"))

    def append_battle_text(self, text):
        self.battle_text.config(state="normal")
        self.battle_text.insert("end", text + "\n")
        self.battle_text.see("end")
        self.battle_text.config(state="disabled")

    def update_buttons_state(self, enabled):
        state = "normal" if enabled else "disabled"
        for btn in self.move_buttons:
            btn.config(state=state)

    def player_move(self, move_name):
        if self.battle_turn != "player":
            return
        self.update_buttons_state(False)
        self.process_turn(self.player_pokemon, self.enemy_pokemon, move_name)

    def enemy_choose_move(self):
        return random.choice(list(self.enemy_pokemon["moves"].keys()))

    def process_turn(self, attacker, defender, move_name):
        move = attacker["moves"][move_name]
        base_power = random.randint(*move["power"])
        effectiveness = self.type_chart.get(move["type"], {}).get(defender["type"], 1.0)
        damage = int(base_power * effectiveness * (1 + 0.05 * attacker.get("level", 1)))
        defender["hp"] = max(0, defender["hp"] - damage)

        eff_text = ""
        if effectiveness > 1:
            eff_text = "It's super effective!"
        elif effectiveness < 1 and effectiveness > 0:
            eff_text = "It's not very effective..."
        elif effectiveness == 0:
            eff_text = "It had no effect..."

        self.append_battle_text(f"{attacker['name']} used {move_name}!")
        if eff_text:
            self.append_battle_text(eff_text)
        self.append_battle_text(f"{defender['name']} lost {damage} HP!")

        self.update_hp_bars()

        self.root.after(1500, self.post_turn, attacker, defender)

    def update_hp_bars(self):
        self.player_hp_bar.update_hp(self.player_pokemon["hp"])
        self.enemy_hp_bar.update_hp(self.enemy_pokemon["hp"])

    def post_turn(self, attacker, defender):
        if defender["hp"] <= 0:
            if defender == self.enemy_pokemon:
                self.append_battle_text(f"{defender['name']} fainted! You won!")
                self.player_win()
            else:
                self.append_battle_text(f"{defender['name']} fainted! You lost...")
                self.battle_end(False)
            return

        if attacker == self.player_pokemon:
            self.battle_turn = "enemy"
            self.root.after(1000, self.enemy_turn)
        else:
            self.battle_turn = "player"
            self.update_buttons_state(True)
            self.append_battle_text("Your turn! Choose a move.")

    def enemy_turn(self):
        move = self.enemy_choose_move()
        self.process_turn(self.enemy_pokemon, self.player_pokemon, move)

    def player_win(self):
        gained_exp = random.randint(10, 30)
        self.append_battle_text(f"You gained {gained_exp} EXP!")
        self.player_pokemon["exp"] += gained_exp
        while self.player_pokemon["exp"] >= self.player_pokemon["next_level_exp"]:
            self.player_pokemon["exp"] -= self.player_pokemon["next_level_exp"]
            self.player_pokemon["level"] += 1
            self.player_pokemon["next_level_exp"] = int(self.player_pokemon["next_level_exp"] * 1.5)
            self.player_pokemon["max_hp"] += 10
            self.player_pokemon["hp"] = self.player_pokemon["max_hp"]
            self.append_battle_text(f"{self.player_pokemon['name']} leveled up! Level {self.player_pokemon['level']}!")
        self.save_game()
        self.root.after(2000, self.main_menu)

    def battle_end(self, player_won):
        self.update_buttons_state(False)
        self.root.after(2000, self.main_menu)

def main():
    root = tk.Tk()
    game = PokemonBattleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
