from big_ol_pile_of_manim_imports import *
from active_projects.eop.reusable_imports import *

class Chapter1OpeningQuote(OpeningQuote):
    CONFIG = {
        "fade_in_kwargs": {
            "submobject_mode": "lagged_start",
            "rate_func": None,
            "lag_factor": 9,
            "run_time": 5,
        },
        "text_size" : "\\normalsize",
        "use_quotation_marks": False,
        "quote" : [
            "How dare we speak of the laws of chance?\\\\",
            "\phantom{r}Is not chance the antithesis of all law?",
        ],
        "quote_arg_separator" : " ",
        "highlighted_quote_terms" : {},
        "author" : "Joseph Bertrand", # 1899
    }

class Introduction(TeacherStudentsScene):

    CONFIG = {
        "default_pi_creature_kwargs": {
        "color": MAROON_E,
        "flip_at_start": True,
        },
        "wait_time_at_end" : 30
    }

    def construct(self):
        
        self.wait(5)
        
        self.change_student_modes(
            "confused", "frustrated", "dejected",
            look_at_arg = UP + 2 * RIGHT
        )

        self.wait()

        self.play(
            self.get_teacher().change_mode,"raise_right_hand"
        )
        self.wait()

        self.wait(30)
        # put examples here in video editor


        # # # # # # # # # # # # # # # # # #
        # show examples of the area model #
        # # # # # # # # # # # # # # # # # #

class UncertaintyInYourMind(Introduction):
    CONFIG = {
        "wait_time_at_end" : 1
    }

    def construct(self):

        self.force_skipping()
        super(UncertaintyInYourMind, self).construct()

        old_r = 3
        die_faces = [DieFace(i).scale(0.5) for i in range(1,7)]
        initial_die = die_faces[old_r]
        q_mark = TextMobject("?").next_to(initial_die, RIGHT)
        thought = VGroup(initial_die, q_mark)
        self.revert_to_original_skipping_status()

        self.student_thinks(thought, student_index = 1, target_mode = "maybe")

        r = 0
        for i in range(10):
            while r == old_r:
                r = np.random.randint(6)
            thought.submobjects[0] = die_faces[r].next_to(q_mark, LEFT)
            self.wait(0.8)
            old_r = r



class VariousFormulas(Scene):

    def construct(self):

        formula1 = TexMobject("P(A\mid B) = P(B\mid A)\cdot{P(A) \over P(B)}")

        formula2 = TexMobject("E[f(X)] = \sum_{i=1}^N p_i f(x_i)")
        formula2.next_to(formula1, DOWN, buff =0.5)

        formula3 = TexMobject("\\text{Var}(aX) = a^2 \\text{Var}X")
        formula3.next_to(formula2, DOWN, buff = 0.5)
        

        self.play(LaggedStart(FadeIn,formula1, run_time = 2))
        self.play(LaggedStart(FadeIn,formula2, run_time = 2))
        self.play(LaggedStart(FadeIn,formula3, run_time = 2))













