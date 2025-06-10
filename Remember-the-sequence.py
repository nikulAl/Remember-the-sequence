import tkinter as tk
from tkinter import messagebox, Label, Entry
from tkinter.ttk import Button
import random      
from PIL import Image, ImageTk
import os

class MemoryGameApp:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Запомни последовательность")
        self.main_window_width = 1000
        self.main_window_height = 750
        self.center_window(self.main_window, self.main_window_width, self.main_window_height)
        self.main_window.resizable(False, False)
        
        self.set_background(self.main_window, self.main_window_width, self.main_window_height)
        
        self.create_main_menu()
        self.counter = 1  # Счетчик пройденных уровней
        self.initial_level = 1  # Начальный уровень, выбранный игроком
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def set_background(self, window, width, height):
        try:
            bg_image = Image.open("bg1.jpg")
            bg_image = bg_image.resize((width, height), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            
            background_label = tk.Label(window, image=bg_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            background_label.image = bg_photo
        except Exception as e:
            print(f"Unable to load image: {e}")
            window.configure(bg='lightblue')

    def create_main_menu(self):
        main_frame = tk.Frame(self.main_window, bg='white')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        Label(main_frame, text='Запомни последовательность', font=('Arial', 20), bg='white').pack(pady=40)
        btn1 = Button(main_frame, text="Начать", command=self.map_of_levels)
        btn1.pack(fill='x', padx=50, pady=10, ipady=5)

        best_result_btn = Button(main_frame, text="Лучший результат", command=self.show_best_result)
        best_result_btn.pack(fill='x', padx=50, pady=10, ipady=5)

        quit_button = Button(main_frame, text="Закрыть окно", command=self.main_window.destroy)
        quit_button.pack(fill='x', padx=50, pady=10, ipady=5)

    def show_best_result(self):
        try:
            if os.path.exists('game_results.txt'):
                with open('game_results.txt', 'r', encoding='utf-8') as file:
                    results = []
                    for line in file:
                        parts = line.strip().split(', ')
                        if len(parts) >= 3:
                            player = parts[0].split(': ')[1]
                            initial_level = int(parts[1].split(': ')[1])
                            passed_level = int(parts[2].split(': ')[1])
                            results.append((player, initial_level, passed_level))
                    
                    if results:
                        # Находим результат с максимальным количеством пройденных уровней
                        best_result = max(results, key=lambda x: x[2] - x[1] + 1)
                        best_player, initial_level, passed_level = best_result
                        levels_passed = passed_level - initial_level + 1
                        messagebox.showinfo(
                            "Лучший результат", 
                            f"Лучший результат:\nИгрок: {best_player}\n"
                            f"Начальный уровень: {initial_level}\n"
                            f"Пройдено уровней: {levels_passed}"
                        )
                    else:
                        messagebox.showinfo("Информация", "Файл с результатами пуст.")
            else:
                messagebox.showinfo("Информация", "Файл с результатами не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать результаты: {e}")

    def map_of_levels(self):
        self.main_window.withdraw()
        self.show_player_name_dialog()

    def show_player_name_dialog(self):
        self.name_window = tk.Toplevel(self.main_window)
        self.name_window.title("Введите имя")
        self.name_window_width = 450
        self.name_window_height = 300
        self.center_window(self.name_window, self.name_window_width, self.name_window_height)
        self.name_window.resizable(False, False)
        
        self.set_background(self.name_window, self.name_window_width, self.name_window_height)
        
        content_frame = tk.Frame(self.name_window, bg='white')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        Label(content_frame, text='Введите имя', bg='white').grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = Entry(content_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        submit_button = Button(content_frame, text="Подтвердить", command=self.handle_name_submission)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def handle_name_submission(self):
        player = self.name_entry.get().strip()
        if not player:
            messagebox.showwarning("Предупреждение!", "Не забудьте ввести имя!")
            return
        
        try:
            with open('players_names.txt', 'a', encoding='utf-8') as saving_names:
                saving_names.write(player + '\n')
            self.name_window.destroy()
            self.show_level_selection(player)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить имя игрока")

    def show_level_selection(self, player):
        self.level_window = tk.Toplevel(self.main_window)
        self.level_window.title("Запомни последовательность")
        self.level_window_width = 1000
        self.level_window_height = 750
        self.center_window(self.level_window, self.level_window_width, self.level_window_height)
        self.level_window.resizable(False, False)
        
        self.set_background(self.level_window, self.level_window_width, self.level_window_height)
        
        content_frame = tk.Frame(self.level_window, bg='white')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        Label(content_frame, text=f"Добро пожаловать, {player}!", bg='white').pack(pady=20)
        Label(content_frame, text='Выберите уровень', font=('Arial', 20), bg='white').pack(pady=40)

        for level in range(1, 5):
            btn = Button(content_frame, text=str(level), 
                       command=lambda lvl=level: self.start_level(lvl, player))
            btn.pack(fill='x', padx=10, pady=5, ipady=5)

        game_exit = Button(content_frame, text='Покинуть игру', command=self.confirm_exit)
        game_exit.pack(fill='x', padx=10, pady=20, ipady=5)

    def start_level(self, level, player):
        self.level_window.withdraw()
        self.current_level = level
        self.initial_level = level  # Сохраняем начальный уровень
        self.current_player = player
        self.counter = 1  # Сбрасываем счетчик пройденных уровней на 1 при старте нового уровня
        self.create_game_window()

    def create_game_window(self):
        self.game_window = tk.Toplevel(self.main_window)
        self.game_window.title(f"Уровень {self.current_level}")
        self.game_window.geometry("1000x750")
        self.center_window(self.game_window, 1000, 750)
        self.set_background(self.game_window, 1000, 750)
        
        MemoryGame(self.game_window, self.current_level, self.level_window, 
                self.current_player, self)
        
        self.game_window.focus_set()

    def confirm_exit(self):
        result = messagebox.askyesno('Покинуть игру', 'Вы уверены, что хотите покинуть игру?')
        if result:
            self.level_window.destroy()
            self.main_window.deiconify()

    def save_result(self, player, level):
        try:
            with open('game_results.txt', 'a', encoding='utf-8') as file:
                file.write(f"Игрок: {player}, Начальный уровень: {self.initial_level}, Пройденный уровень: {level}\n")
        except Exception as e:
            print(f"Ошибка при сохранении результата: {e}")

    def next_level(self, current_level, player):
        if hasattr(self, 'game_window') and self.game_window:
            self.game_window.destroy()
            self.counter += 1  # Увеличиваем счетчик пройденных уровней
            self.current_level = current_level + 1
            self.save_result(player, self.current_level)
            self.create_game_window()
            self.level_window.deiconify()

    def run(self):
        self.main_window.mainloop()

class MemoryGame:
    def __init__(self, root, level, parent_window, player, app):
        self.root = root
        self.level = level
        self.parent_window = parent_window
        self.player = player
        self.app = app
        self.sequence = []
        self.current_index = 0
        self.repeats_used = 0

        game_frame = tk.Frame(root, bg='white')
        game_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.welcome_label = Label(game_frame, text=f"Уровень {self.level}", 
                                 font=('Arial', 20), bg='white')
        self.welcome_label.pack(pady=10)

        self.sequence_label = Label(game_frame, text="", font=('Arial', 20), bg='white')
        self.sequence_label.pack(pady=10)

        self.input_label = Label(game_frame, 
                               text="Введите последовательность через пробел:", 
                               font=('Arial', 12), bg='white')
        self.input_label.pack(pady=10)

        self.entry = Entry(game_frame, font=('Arial', 14))
        self.entry.pack(pady=10, ipadx=40, ipady=7)

        self.check_button = Button(game_frame, text="Проверить", command=self.check_sequence)
        self.check_button.pack(pady=10)

        self.repeat_button = Button(game_frame, 
                                  text="Повторить последовательность (осталось: 1)", 
                                  command=self.repeat_sequence, 
                                  state="disabled")
        self.repeat_button.pack(pady=10)

        self.leave_button = Button(game_frame, text="Покинуть игру", command=self.quit_game)
        self.leave_button.pack(pady=10)

        self.start_game()

    def generate_sequence(self):
        sequence_length = self.level * 2
        return [random.randint(0, 9) for _ in range(sequence_length)]

    def repeat_sequence(self):
        if self.repeats_used < 1:
            self.repeats_used += 1
            self.repeat_button.config(text="Повторить последовательность (осталось: 0)")
            self.current_index = 0
            self.entry.config(state="disabled")
            self.check_button.config(state="disabled")
            self.repeat_button.config(state="disabled")
            self.display_sequence()
        else:
            self.repeat_button.config(state="disabled")
            messagebox.showinfo("Информация", "Вы уже использовали повтор!")

    def display_sequence(self):
        if self.current_index < len(self.sequence):
            self.sequence_label.config(text=str(self.sequence[self.current_index]))
            
            show_time = max(800, 1200 - self.level * 150)
            pause_time = 300
            
            self.root.after(show_time, lambda: 
                self.sequence_label.config(text="") or 
                self.root.after(pause_time, lambda: 
                    self.next_digit()))
        else:
            self.sequence_label.config(text="")
            self.current_index = 0
            self.entry.config(state="normal")
            self.check_button.config(state="normal")
            if self.repeats_used < 1:
                self.repeat_button.config(state="normal")
            else:
                self.repeat_button.config(state="disabled")

    def next_digit(self):
        self.current_index += 1
        self.display_sequence()

    def start_game(self):
        self.sequence = self.generate_sequence()
        self.current_index = 0
        self.repeats_used = 0
        self.entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.repeat_button.config(text="Повторить последовательность (осталось: 1)")
        self.repeat_button.config(state="normal")
        self.entry.delete(0, tk.END)
        self.display_sequence()

    def check_sequence(self):
        player_input = self.entry.get().strip()
        if not player_input:
            messagebox.showwarning("Ошибка", "Введите последовательность!")
            return
            
        try:
            player_sequence = [int(num) for num in player_input.split()]
        except ValueError:
            messagebox.showerror("Ошибка", "Введите только числа через пробел!")
            return
            
        if player_sequence == self.sequence:
            self.entry.focus_set()
            messagebox.showinfo("Правильно!", f"Отлично, {self.player}!")
            self.root.after(1000, lambda: self.app.next_level(self.level, self.player))
        else:
            self.app.save_result(self.player, self.level)
            self.entry.focus_set()
            messagebox.showerror("Неправильно!", f"Правильная последовательность: {' '.join(map(str, self.sequence))}")
            self.quit_game()

    def quit_game(self):
        self.root.destroy()
        self.parent_window.deiconify()

if __name__ == "__main__":
    app = MemoryGameApp()
    app.run()