from fractions import Fraction

from big_ol_pile_of_manim_imports import *


EXAMPLE_MATRIX = [
    [2, -1, -1],
    [0, 3, -4],
    [-3, 2, 1],
]
EXAMPLE_OUTPUT = [[1], [2], [3]]


class FractionMobject(VGroup):
    CONFIG = {
        "max_height": 1,
    }

    def __init__(self, fraction, **kwargs):
        VGroup.__init__(self, **kwargs)
        fraction = Fraction(fraction)
        numerator = self.numerator = Integer(fraction.numerator)
        self.add(numerator)
        if fraction.denominator != 1:
            denominator = Integer(fraction.denominator)
            # line = TexMobject("/")
            # numerator.next_to(line, LEFT, SMALL_BUFF)
            # denominator.next_to(line, RIGHT, SMALL_BUFF)
            frac = TexMobject(
                str(numerator.number), "\\over", str(denominator.number)
            )
            line = frac[1]
            numerator.replace(frac[0])
            denominator.replace(frac[2])
            self.add(numerator, line, denominator)
        self.scale_to_fit_height(min(self.max_height, self.get_height()))
        self.value = fraction

    def add_plus_if_needed(self):
        if self.value > 0:
            plus = TexMobject("+")
            plus.next_to(self, LEFT, SMALL_BUFF)
            plus.match_color(self)
            self.add_to_back(plus)

    def add_background_rectangle(self):
        self.add_to_back(BackgroundRectangle(self))


class RowReductionScene(Scene):
    CONFIG = {
        "h_spacing": 2,
        "extra_h_spacing": 0.5,
        "v_spacing": 1.5,
        "element_aligned_edge": ORIGIN,
        "include_separation_lines": True,
        "include_brackets": True,
        "changing_row_color": YELLOW,
        "reference_row_color": BLUE,
    }

    def initialize_terms(self):
        full_matrix = reduce(
            lambda m, v: np.append(m, v, axis=1),
            self.matrices
        )
        mobject_matrix = np.vectorize(FractionMobject)(full_matrix)
        rows = self.rows = VGroup(*it.starmap(VGroup, mobject_matrix))
        for i, row in enumerate(rows):
            for j, term in enumerate(row):
                term.move_to(
                    i * self.v_spacing * DOWN +
                    j * self.h_spacing * RIGHT,
                    aligned_edge=self.element_aligned_edge,
                )

        # Visually seaprate distinct parts
        separation_lines = self.separation_lines = VGroup()
        lengths = [len(m[0]) for m in self.matrices]
        for cs in np.cumsum(lengths)[:-1]:
            VGroup(*mobject_matrix[:, cs:].flatten()).shift(
                self.extra_h_spacing * RIGHT
            )
            columns = VGroup(*mobject_matrix[:, cs - 1: cs + 1].flatten())
            line = DashedLine(columns.get_top(), columns.get_bottom())
            line.move_to(columns)
            separation_lines.add(line)

        lb, rb = brackets = self.brackets = TexMobject("[]")
        brackets.stretch(0.5, 0)
        brackets.match_height(rows)
        lb.next_to(rows, LEFT)
        rb.next_to(rows, RIGHT)

        group = VGroup(rows)
        if self.include_separation_lines:
            group.add(separation_lines)
        if self.include_brackets:
            group.add(brackets)
        group.center().to_edge(DOWN, buff=2)
        self.add(group)

    def add_variables(self):
        # If it is meant to represent a system of equations
        variables = self.variables = VGroup()
        symbols = self.symbols = VGroup()
        colors = [X_COLOR, Y_COLOR, Z_COLOR]
        for row in self.rows:
            for e1, e2, char, color in zip(row, row[1:], "xyz", colors):
                variable = TexMobject(char)
                variable.set_color(color)
                variable.next_to(e1, RIGHT, SMALL_BUFF, aligned_edge=DOWN)
                # What's the right way here...
                if char == "y":
                    variable.shift(SMALL_BUFF * DOWN)
                if e2 is row[-1]:
                    symbol = TexMobject("=")
                else:
                    symbol = TexMobject("+")
                symbol.move_to(VGroup(variable, e2))
                variables.add(variable)
                symbols.add(symbol)
        self.add(variables, symbols)

    def apply_row_rescaling(self, row_index, scale_factor):
        row = self.rows[row_index]
        new_row = VGroup()
        for element in row:
            target = FractionMobject(element.value * scale_factor)
            target.move_to(element, aligned_edge=self.element_aligned_edge)
            new_row.add(target)
        new_row.set_color(self.changing_row_color)

        label = VGroup(
            TexMobject("r_%d" % (row_index + 1)),
            TexMobject("\\rightarrow"),
            TexMobject("("),
            FractionMobject(scale_factor),
            TexMobject(")"),
            TexMobject("r_%d" % (row_index + 1)),
        )
        label.arrange_submobjects(RIGHT, buff=SMALL_BUFF)
        label.to_edge(UP)
        VGroup(label[0], label[-1]).set_color(self.changing_row_color)
        parens = VGroup(label[2], label[4])
        parens.match_height(label[3], stretch=True)

        scalar_mob = FractionMobject(scale_factor)
        scalar_mob.add_to_back(
            TexMobject("\\times").next_to(scalar_mob, LEFT, SMALL_BUFF)
        )
        scalar_mob.scale(0.5)
        scalar_mob.next_to(row[0], DR, SMALL_BUFF)
        scalar_mob.add_background_rectangle()

        # Do do, fancier illustrations here
        self.play(
            FadeIn(label),
            row.set_color, self.changing_row_color,
        )
        self.play(FadeIn(scalar_mob))
        for elem, new_elem in zip(row, new_row):
            self.play(scalar_mob.next_to, elem, DR, SMALL_BUFF)
            self.play(
                FadeIn(new_elem),
                FadeOut(elem)
            )
        self.play(FadeOut(scalar_mob))
        self.play(new_row.set_color, WHITE)
        self.play(FadeOut(label))
        self.rows.submobjects[row_index] = new_row

    def add_row_multiple_to_row(self, row1_index, row2_index, scale_factor):
        row1 = self.rows[row1_index]
        row2 = self.rows[row2_index]
        new_row1 = VGroup()
        scaled_row2 = VGroup()
        for elem1, elem2 in zip(row1, row2):
            target = FractionMobject(elem1.value + scale_factor * elem2.value)
            target.move_to(elem1, aligned_edge=self.element_aligned_edge)
            new_row1.add(target)

            scaled_term = FractionMobject(scale_factor * elem2.value)
            scaled_term.move_to(elem2)
            scaled_row2.add(scaled_term)
        new_row1.set_color(self.changing_row_color)
        scaled_row2.set_color(self.reference_row_color)

        for elem1, elem2 in zip(row1, scaled_row2):
            elem2.add_plus_if_needed()
            elem2.scale(0.5)
            elem2.next_to(elem1, UL, buff=SMALL_BUFF)

        label = VGroup(
            TexMobject("r_%d" % (row1_index + 1)),
            TexMobject("\\rightarrow"),
            TexMobject("r_%d" % (row1_index + 1)),
            TexMobject("+"),
            TexMobject("("),
            FractionMobject(scale_factor),
            TexMobject(")"),
            TexMobject("r_%d" % (row2_index + 1)),
        )
        label.arrange_submobjects(RIGHT, buff=SMALL_BUFF)
        label.to_edge(UP)
        VGroup(label[0], label[2]).set_color(self.changing_row_color)
        label[-1].set_color(self.reference_row_color)

        self.play(
            FadeIn(label),
            row1.set_color, self.changing_row_color,
            row2.set_color, self.reference_row_color,
        )
        row1.target.next_to(self.rows, UP, buff=2)
        row1.target.align_to(row1, LEFT)

        row2.target.next_to(row1.target, DOWN, buff=MED_LARGE_BUFF)
        lp, rp = row2_parens = TexMobject("()")
        row2_parens.scale_to_fit_height(row2.get_height() + 2 * SMALL_BUFF)
        lp.next_to(row2, LEFT, SMALL_BUFF)
        rp.next_to(row2, RIGHT, SMALL_BUFF)
        scalar = FractionMobject(scale_factor)
        scalar.next_to(lp, LEFT, SMALL_BUFF)
        scalar.add_plus_if_needed()

        self.play(
            FadeIn(row2_parens),
            Write(scalar),
        )
        self.play(ReplacementTransform(row2.copy(), scaled_row2))
        self.wait()
        for elem, new_elem, s_elem in zip(row1, new_row1, scaled_row2):
            s_elem.add_background_rectangle()
            self.play(
                FadeOut(elem),
                FadeIn(new_elem),
                s_elem.move_to, new_elem,
                s_elem.fade, 1,
            )
            self.remove(s_elem)
        self.wait()
        self.play(
            FadeOut(label),
            FadeOut(row2_parens),
            FadeOut(scalar),
            new_row1.set_color, WHITE,
            row2.set_color, WHITE,
        )
        self.rows.submobjects[row1_index] = new_row1


class SystemsOfEquationsExample(RowReductionScene):
    CONFIG = {
        "matrices": [EXAMPLE_MATRIX, EXAMPLE_OUTPUT],
        "element_aligned_edge": RIGHT,
        "include_separation_lines": False,
        "include_brackets": False,
    }

    def construct(self):
        self.initialize_terms()
        self.add_variables()
        self.solve_example_matrix()

    def solve_example_matrix(self):
        self.apply_row_rescaling(0, Fraction(1, 2))
        self.add_row_multiple_to_row(2, 0, 3)
        self.apply_row_rescaling(1, Fraction(1, 3))
        self.add_row_multiple_to_row(2, 1, Fraction(-1, 2))
        self.apply_row_rescaling(2, Fraction(6))
        self.add_row_multiple_to_row(0, 1, Fraction(1, 2))
        self.add_row_multiple_to_row(0, 2, Fraction(7, 6))
        self.add_row_multiple_to_row(1, 2, Fraction(4, 3))
        self.wait()


class SystemsOfEquationsWithoutVariables(SystemsOfEquationsExample):
    CONFIG = {
        "element_aligned_edge": ORIGIN,
        "include_separation_lines": True,
    }

    def construct(self):
        self.initialize_terms()
        self.solve_example_matrix()


class FindInverse(SystemsOfEquationsWithoutVariables):
    CONFIG = {
        "matrices": [EXAMPLE_MATRIX, np.identity(3)]
    }
