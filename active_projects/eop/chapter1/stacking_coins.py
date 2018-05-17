from big_ol_pile_of_manim_imports import *
from active_projects.eop.reusable_imports import *


class StackingCoins(Scene):

    CONFIG = {
        "nb_flips" : 120,
        "stack_gap" : 1,
        "stack_scale" : 1,
        "stack_anchor" : 3 * DOWN
    }

    def build_up_stack(self, nb_flips):

        h = t = 3
        heads_anchor = self.stack_anchor + 0.5 * self.stack_gap * LEFT
        tails_anchor = self.stack_anchor + 0.5 * self.stack_gap * RIGHT

        heads_stack = HeadsStack(size = h).scale(self.stack_scale)
        heads_stack.next_to(heads_anchor, UP)
        tails_stack = TailsStack(size = t).scale(self.stack_scale)
        tails_stack.next_to(tails_anchor, UP)
        self.add(heads_stack, tails_stack)

        for i in range(nb_flips):
            flip = np.random.choice(["H", "T"])
            if flip == "H":
                h += 1
                new_heads_stack = HeadsStack(size = h).scale(self.stack_scale)
                new_heads_stack.next_to(heads_anchor, UP)
                self.play(Transform(heads_stack, new_heads_stack,
                    run_time = 0.2))
            elif flip == "T":
                t += 1
                new_tails_stack = TailsStack(size = t).scale(self.stack_scale)
                new_tails_stack.next_to(tails_anchor, UP)
                self.play(Transform(tails_stack, new_tails_stack,
                    run_time = 0.2))

        heads_stack.size, tails_stack.size = h, t                
        return VGroup(heads_stack, tails_stack)


    def construct(self):

        stack = self.build_up_stack(self.nb_flips)