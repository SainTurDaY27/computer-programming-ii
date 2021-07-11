import tkinter as tk
import tkinter.ttk as ttk
from turtle import RawTurtle
from tkinter import messagebox
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500


class TurtleAdventure(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.create_widgets()
        self.turtle = Turtle(self.canvas)
        self.canvas.bind("<Button-1>", lambda e: self.turtle.set_waypoint(e.x, e.y))
        self.is_animating = False
        self.home = Home(self.canvas, size=30, pos=(CANVAS_WIDTH - 100, CANVAS_HEIGHT / 2))
        self.enemies = [
            BasicEnemy(self.canvas, size=50, pos=(300, 200)),
            BasicEnemy(self.canvas, size=30, pos=(600, 300)),
            MovingEnemy(self.canvas, size=30),
            MovingEnemy(self.canvas, size=20, speed=5),
            FencingEnemy(self.canvas, size=20, speed=5, fence=(200, 100, 500, 300)),
            # this guy should be guarding the home
            FencingEnemy(self.canvas, size=20,
                         fence=(
                             CANVAS_WIDTH - 150, CANVAS_HEIGHT // 2 - 50, CANVAS_WIDTH - 50, CANVAS_HEIGHT // 2 + 50)),
            OwnEnemy(self.canvas, size=45, speed=15),
            OwnEnemy(self.canvas, size=40, speed=20),
            OwnEnemy(self.canvas, size=35, speed=25),
            OwnEnemy(self.canvas, size=30, speed=30),
            OwnEnemy(self.canvas, size=25, speed=35),
            OwnEnemy(self.canvas, size=30, speed=40),
            OwnEnemy(self.canvas, size=35, speed=45),
            OwnEnemy(self.canvas, size=40, speed=50),
        ]

    def create_widgets(self):
        self.canvas = tk.Canvas(self, borderwidth=0,
                                width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2,
                         sticky="news", padx=10, pady=10)
        self.btn_start_top = ttk.Button(self, text="Start",
                                        command=self.toggle_animation)
        self.btn_start_top.grid(row=1, column=0, pady=10)
        ttk.Button(self, text="Quit", command=root.destroy).grid(
            row=1, column=1, pady=10)

    def toggle_animation(self):
        self.is_animating = not self.is_animating
        if self.is_animating:
            self.btn_start_top.config(text="Stop")
            self.animate()
        else:
            self.btn_start_top.config(text="Start")

    def animate(self):
        self.turtle.animate()
        if self.is_animating:  # schedule the next update
            timer = self.after(33, self.animate)
        if self.home.contains_turtle(self.turtle):
            self.after_cancel(timer)
            messagebox.showinfo(title="Turtle Game",
                                message="Turtle is home!  You win.")
            root.destroy()
            return
        for enemy in self.enemies:
            enemy.animate()
            if enemy.hits_turtle(self.turtle):
                self.after_cancel(timer)
                messagebox.showinfo(title="Turtle Game",
                                    message="Turtle is dead!  You lose.")
                root.destroy()
                return


class Turtle(RawTurtle):

    def __init__(self, canvas, speeed=3):
        super().__init__(canvas)
        self.screen.setworldcoordinates(0, CANVAS_HEIGHT - 1, CANVAS_WIDTH - 1, 0)
        self.shape("turtle")
        self.color("green")
        self.penup()
        self.goto(10, CANVAS_HEIGHT / 2)
        self.speed = speeed
        self.waypoint = None
        self.screen.tracer(False)  # disable turtle's built-in animation

    def animate(self):
        if self.waypoint is not None:
            x, y = self.waypoint
            if self.distance(x, y) >= self.speed:
                self.setheading(self.towards(x, y))
                self.forward(self.speed)
        self.screen.update()

    def set_waypoint(self, x, y):
        self.waypoint = (x, y)


class Home:
    def __init__(self, canvas, size, pos):
        self.canvas = canvas
        self.size = size
        self.pos = pos
        x, y = pos
        self._id = canvas.create_rectangle(
            x - size / 2, y - size / 2, x + size / 2, y + size / 2,
            outline="red", width=3)

    def contains_turtle(self, turtle):
        x, y = self.pos
        size = self.size
        x1, x2 = x - size / 2, x + size / 2
        y1, y2 = y - size / 2, y + size / 2
        tx, ty = turtle.pos()
        return x1 <= tx <= x2 and y1 <= ty <= y2


class BasicEnemy:

    def __init__(self, canvas, size=30, pos=(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)):
        self.canvas = canvas
        self.size = size
        self._id = canvas.create_oval(0, 0, size, size)
        self.pos = pos
        self.set_color("yellow")
        self.render()

    def set_color(self, color):
        self.canvas.itemconfigure(self._id, fill=color)

    def render(self):
        x, y = self.pos
        # self.canvas.moveto(self._id, x - self.size / 2, y - self.size / 2)
        self.canvas.coords(self._id,
                           x - self.size / 2, y - self.size / 2,
                           x + self.size / 2, y + self.size / 2,
                           )

    def animate(self):
        pass

    def hits_turtle(self, turtle):
        x, y = self.pos
        return turtle.distance(x, y) < self.size / 2


class MovingEnemy(BasicEnemy):

    def __init__(self, canvas, size=30, speed=2):
        super().__init__(canvas, size=size)
        self.speed = speed
        self.set_color("orange")
        self._coro = self.script()

    def move(self, x, y):
        self.pos = (x, y)

    def animate(self):
        if self._coro is None:
            return
        try:
            next(self._coro)
            self.render()
        except StopIteration:
            self._coro = None

    def script(self):
        while True:
            x, y = self.pos
            newx = x + random.randint(-self.speed, self.speed)
            newy = y + random.randint(-self.speed, self.speed)
            newx = min(max(newx, 0), CANVAS_WIDTH)
            newy = min(max(newy, 0), CANVAS_HEIGHT)
            self.move(newx, newy)
            yield


class FencingEnemy(MovingEnemy):

    def __init__(self, canvas, size=30, speed=2, fence=(50, 50, 100, 100)):
        super().__init__(canvas, size=size, speed=speed)
        self.fence = fence
        self.set_color("red")

    def script(self):
        x1, y1, x2, y2 = self.fence
        while True:
            # Add your code so that the enemy moves in a rectangular pattern
            # whose top-left corner is (x1,y1) and bottom-right corner is (x2,y2).
            # The enemy must also move at the speed defined by the 'speed' attribute.
            for x in range(x1, x2, self.speed):
                self.move(x, y1)
                yield
            for y in range(y1, y2, self.speed):
                self.move(x2, y)
                yield
            for x in range(x2, x1, -self.speed):
                self.move(x, y2)
                yield
            for y in range(y2, y1, -self.speed):
                self.move(x1, y)
                yield


class OwnEnemy(MovingEnemy):

    def __init__(self, canvas, size=5, speed=5):
        super().__init__(canvas, size=size, speed=speed)
        self.speed = speed
        self._id = canvas.create_rectangle(20
                                           , 20, 20, 20,
                                           outline="purple", width=3)

    def script(self):
        x_first, y_first = 1200, 300
        while True:
            for i in range(0, x_first, self.speed):
                self.move(i, y_first)
                yield
            x_first -= 50
            for i in range(0, y_first, self.speed):
                self.move(x_first, i)
                yield
            y_first -= 50
            for i in range(x_first, 0, -self.speed):
                self.move(i, y_first)
                yield
            x_first += 50
            for i in range(y_first, 0, -self.speed):
                self.move(x_first, i)
                yield
            y_first -= 50
            if y_first <= 100:
                y_first += 300


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Turtle's Adventure")

    # do not allow window resizing
    root.resizable(False, False)
    app = TurtleAdventure(root)
    root.mainloop()
