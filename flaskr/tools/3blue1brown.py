# https://docs.manim.community/en/stable/examples.html
# winget install ffmpeg
# manim filemane.py className -pql
# manim -pql 3blue1brown.py Main
# vlc open first
# run from debug select "Python:Manim"

# https://github.com/3b1b/manim
# https://www.youtube.com/watch?v=d9nbtyO2YcU
from manim import *

# https://docs.manim.community/en/stable/examples.html#pointmovingonshapes
class Main(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()
