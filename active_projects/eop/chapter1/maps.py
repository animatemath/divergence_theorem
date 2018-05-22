from big_ol_pile_of_manim_imports import *

class MapsOfPossibilities(TeacherStudentsScene):

    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": MAROON_E,
            "flip_at_start": True,
        },
    }

    def construct(self):

        self.wait(2)

        teacher_text = TextMobject("Coin flips are just a metaphor")

        self.teacher_says(teacher_text, target_mode = "happy")

        self.wait()

        self.play(
            self.students[0].change_mode, "thinking",
            self.students[1].change_mode, "conniving",
            self.students[2].change_mode, "tease"
        )

        self.wait(3)

        self.play(
            Uncreate(self.teacher.bubble),
            Uncreate(self.teacher.bubble.content),
            self.students[0].look_at, self.teacher,
            self.students[1].look_at, self.teacher,
            self.students[2].look_at, self.teacher,
            self.teacher.look_at, self.students,
        )

        self.play(
            self.change_all_student_modes, "happy",
            self.teacher.change_mode, "happy",
        ) 