
from big_ol_pile_of_manim_imports import *
from active_projects.eop.reusable_imports import *
from active_projects.eop.chapter1.morph_brick_row_into_histogram import *
from active_projects.eop.chapter1.stacking_coins import *


class Conclusion(MorphBrickRowIntoHistogram100, StackingCoins):
    CONFIG = {
        "level" : 100,
        "bar_anchor_height" : -3,
        "brick_row_height" : 2,
        "scaled_width" : 5,
        "scaled_height" : 5.0,
        "coin_scale" : 0.5,
        "stack_gap" : 0.4,
        "stack_anchor" : 4 * LEFT + 2 * DOWN
    }

    def construct(self):

        self.force_skipping()
        super(Conclusion, self).construct()
        self.nb_flips = self.level
        self.histogram.to_edge(RIGHT, buff = 1.5)
        self.nb_tails_label.next_to(self.x_labels, RIGHT)
        self.nb_tails_label.shift(UP + 1.3 * LEFT)
        self.nb_flips_text.shift(0.5 * DOWN)

        self.revert_to_original_skipping_status()

        for i in range(20):
            stack = self.build_up_stack(self.nb_flips)
            nb_tails = stack[1].size
            rect = SurroundingRectangle(stack)
            rect.set_stroke(width = 0)
            rect.target = SurroundingRectangle(self.bars[nb_tails], buff = 0).copy()
            rect.target.set_stroke(width = 0)
            rect.target.set_fill(color = YELLOW, opacity = 0.2)
            stack.target = stack.copy()
            stack.target.fade(1)
            stack.target.move_to(rect.target)
            self.play(
                MoveToTarget(stack),
                MoveToTarget(rect),
            )
            print "========", i, "========"

        