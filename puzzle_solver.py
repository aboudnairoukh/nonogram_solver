#################################################################
# FILE : puzzle_solver.py
# WRITER : Abed EL Rahman Nairoukh , aboudnairoukh , 213668700
# EXERCISE : intro2cs2 ex8 2022
# DESCRIPTION : A puzzle solver
#################################################################
from typing import List, Tuple, Set, Optional

EXACT = 1
VIOLATION = 0
POSSIBLE = 2
BLACK = 0
WHITE = 1
UNKNOWN = -1

# We define the types of a partial picture and a constraint
# (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def seen_in_col(picture: Picture, row: int, col: int, unknown_cell: str) \
        -> int:
    """This function returns the number of the seen cells in the col
     of (row,col) cell"""
    seen_cells = 0
    for i in range(len(picture)):
        if picture[i][col] == BLACK and i > row:
            return seen_cells
        if picture[i][col] == BLACK:
            seen_cells = 0
        else:
            if picture[i][col] == UNKNOWN:
                if unknown_cell == 'black':
                    if i > row:
                        return seen_cells
                    seen_cells = 0
                else:
                    seen_cells += 1
            else:
                seen_cells += 1
    return seen_cells


def seen_in_row(picture: Picture, row: int, col: int, unknown_cell: str) \
        -> int:
    """This function returns the number of the seen cells in the row
     of (row,col) cell"""
    seen_cells = 0
    for i in range(len(picture[0])):
        if picture[row][i] == BLACK and i > col:
            return seen_cells
        if picture[row][i] == BLACK:
            seen_cells = 0
        else:
            if picture[row][i] == UNKNOWN:
                if unknown_cell == 'black':
                    if i > col:
                        return seen_cells
                    seen_cells = 0
                else:
                    seen_cells += 1
            else:
                seen_cells += 1
    return seen_cells


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function returns the number of the seen cells of (row,col) cell
    while unknown cells are considered as white cells"""
    if picture[row][col] == BLACK:
        return 0
    else:
        return seen_in_col(picture, row, col, "white") + \
               seen_in_row(picture, row, col, "white") - 1


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function returns the number of the seen cells of (row,col) cell
    while unknown cells are considered as black cells"""
    if picture[row][col] == BLACK or picture[row][col] == UNKNOWN:
        return 0
    else:
        return seen_in_col(picture, row, col, "black") + \
               seen_in_row(picture, row, col, "black") - 1


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) \
        -> int:
    """This function returns how successful the partial image is using
    the numbers 0-2"""
    possible = False
    exact = True
    for constraint in constraints_set:
        min_seen = min_seen_cells(picture, constraint[0], constraint[1])
        max_seen = max_seen_cells(picture, constraint[0], constraint[1])
        if min_seen != constraint[2] or max_seen != constraint[2]:
            exact = False
        if min_seen <= constraint[2] <= max_seen:
            possible = True
        else:
            return VIOLATION
    if exact:
        return EXACT
    elif possible:
        return POSSIBLE
    return VIOLATION


def solve_puzzle_helper(picture: Picture, constraints_set: Set[Constraint],
                        row: int, col: int,
                        unchangeable_cells: Set[Tuple[int, int]],
                        search_type: str, num_of_solutions: List[int],
                        colors: Tuple[int, int] = (BLACK, WHITE)) -> bool:
    """This function is a helper function to solve_puzzle"""
    if col == len(picture[0]) and row == 0:
        num_of_solutions[0] += 1
        if search_type == 'how_many':
            return False
        else:
            return True
    if (row, col) not in unchangeable_cells:
        for color in colors:
            picture[row][col] = color
            if check_constraints(picture, constraints_set) != VIOLATION:
                if row == len(picture) - 1:
                    if solve_puzzle_helper(picture, constraints_set, 0,
                                           col + 1, unchangeable_cells,
                                           search_type, num_of_solutions):
                        return True
                else:
                    if solve_puzzle_helper(picture, constraints_set, row + 1,
                                           col, unchangeable_cells,
                                           search_type, num_of_solutions):
                        return True
        picture[row][col] = UNKNOWN
        return False
    if row == len(picture) - 1:
        if solve_puzzle_helper(picture, constraints_set, 0, col + 1,
                               unchangeable_cells, search_type,
                               num_of_solutions):
            return True
    else:
        if solve_puzzle_helper(picture, constraints_set, row + 1, col,
                               unchangeable_cells, search_type,
                               num_of_solutions):
            return True
    return False


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) \
        -> Optional[Picture]:
    """This function returns a solution to the given puzzle"""
    picture = [[-1] * m for _ in range(n)]
    unchangeable_cells = set()
    for constraints in constraints_set:
        unchangeable_cells.add((constraints[0], constraints[1]))
        if constraints[2] == 0:
            picture[constraints[0]][constraints[1]] = BLACK
        else:
            picture[constraints[0]][constraints[1]] = WHITE
    if check_constraints(picture, constraints_set) == VIOLATION:
        return None
    if solve_puzzle_helper(picture, constraints_set, 0, 0,
                           unchangeable_cells, 'solve', [0]):
        return picture
    return None


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) \
        -> int:
    """This function returns the number of potential solutions of the given
     puzzle"""
    picture = [[-1] * m for _ in range(n)]
    unchangeable_cells = set()
    for constraints in constraints_set:
        unchangeable_cells.add((constraints[0], constraints[1]))
        if constraints[2] == 0:
            picture[constraints[0]][constraints[1]] = BLACK
        else:
            picture[constraints[0]][constraints[1]] = WHITE
    if check_constraints(picture, constraints_set) == VIOLATION:
        return 0
    num_of_solutions = [0]
    solve_puzzle_helper(picture, constraints_set, 0, 0, unchangeable_cells,
                        'how_many', num_of_solutions)
    return num_of_solutions[0]


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """This function returns a constraints set of the given picture"""
    all_constraints_set1 = set()
    all_constraints_set2 = set()
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            if picture[i][j] == WHITE and min_seen_cells(picture, i, j) == 1:
                all_constraints_set1.add((i, j, 1))
                all_constraints_set2.add((i, j, 1))
            else:
                all_constraints_set1.add((i, j, min_seen_cells(picture, i, j)))
                all_constraints_set2.add((i, j, min_seen_cells(picture, i, j)))
    for constraints in all_constraints_set2:
        all_constraints_set1.remove(constraints)
        if (how_many_solutions(all_constraints_set1, len(picture),
                               len(picture[0])) != 1):
            all_constraints_set1.add(constraints)
    return all_constraints_set1
