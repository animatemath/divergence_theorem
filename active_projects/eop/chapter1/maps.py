from big_ol_pile_of_manim_imports import *

class MapsOfPossibilities(TeacherStudentsScene):

    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": MAROON_E,
            "flip_at_start": True,
        },
    }

    def construct(self):

        self.wait(8)

        teacher_text = TextMobject("It's all about", "mapping out", "possibilities")
        teacher_text.set_color_by_tex("mapping out", YELLOW)

        self.teacher_says(teacher_text, target_mode = "happy")

        self.wait()

        self.play(
            self.students[0].change_mode, "thinking",
            self.students[1].change_mode, "conniving",
            self.students[2].change_mode, "tease"
        )

        self.wait(8)
