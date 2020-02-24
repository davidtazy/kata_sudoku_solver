import unittest
from sudoku_solver import  SudokuSolver, create_zero_grid, create_solved_grid, create_real_world_grid,create_hard_sudoku


class TestSudokuSolver(unittest.TestCase):

    def test_all_positions_and_numbers_are_possible_on_zero_grid(self):
        grid = create_zero_grid()
        solver = SudokuSolver(grid)

        for number in range(1, 10):
            for col in range(9):
                for row in range(9):
                    self.assertTrue(solver._is_possible(col,row,number))

    def test_cannot_insert_number_if_it_is_already_on_same_row(self):
        grid = create_zero_grid()
        row = 3
        number = 8
        grid[2][row] = number

        solver = SudokuSolver(grid)

        self.assertFalse(solver._is_possible(4,row,number))
        # ok for neighbor row
        self.assertTrue(solver._is_possible(4,row + 1,number))

    def test_cannot_insert_number_if_it_is_already_on_same_column(self):
        grid = create_zero_grid()
        col = 3
        number = 8
        grid[col][2] = number

        solver = SudokuSolver(grid)

        self.assertFalse(solver._is_possible(col,4,number))
        # ok for neighbor col
        self.assertTrue(solver._is_possible(col + 1, 4 ,number))

    def test_cannot_insert_number_if_it_is_already_on_same_block(self):
        grid = create_zero_grid()
        
        number = 8
        grid[1][1] = number
        grid[4][4] = number
        grid[7][7] = number
        solver = SudokuSolver(grid)

        self.assertFalse(solver._is_possible(2,2,number))
        self.assertFalse(solver._is_possible(5,5,number))
        self.assertFalse(solver._is_possible(8,8,number))

    def test_solve_missing_one_number(self):
         grid = create_solved_grid()
         grid[0][0] = 0

         solver = SudokuSolver(grid)

         self.assertTrue( solver.brut_force() )

         self.assertEqual(solver._grid , create_solved_grid() )

    def test_solve_missing_two_number(self):
         grid = create_solved_grid()
         grid[0][0] = 0
         grid[7][8] = 0

         solver = SudokuSolver(grid)

         self.assertTrue( solver.brut_force() )

         self.assertEqual(solver._grid , create_solved_grid() )

    @unittest.skip("brut force is too long")
    def test_solve_real_word_sudoku(self):
         grid = create_real_world_grid()

         solver = SudokuSolver(grid)

         import time
         start = time.monotonic()

         self.assertTrue( solver.brut_force() )
         
         end = time.monotonic()
         print ("elapsed = {} s".format(end - start))

         self.assertTrue( solver.check())
         solver._debug()

    def test_find_safest_position_to_solve(self):

        grid = create_solved_grid()
        solution = grid[8][8]
        grid[8][8] = 0

        solver = SudokuSolver(grid)

        self.assertEqual( solver.find_safest_position_to_solve(), ( (8, 8),[solution])  )


    def test_safest_first_solver(self):
        print("test_safest_first_solver")
        grid = create_real_world_grid()
        solver = SudokuSolver(grid)
        self.assertTrue( solver.safest_first_solver() )
        self.assertTrue( solver.check())
        solver._debug()

   
    def test_safest_first_solver_with_hard_one(self):
        print("test_safest_first_solver_with_hard_one")
        grid = create_hard_sudoku()
        solver = SudokuSolver(grid)
        self.assertTrue( solver.safest_first_solver() )
        self.assertTrue( solver.check() )
        solver._debug()

    def test_safest_first_solver_with_other_hard_one(self):
        print("test_safest_first_solver_with__other_hard_one")
        grid = [
            [1,0,0, 0,0,0, 0,0,0],
            [3,8,0, 0,0,1, 0,0,0],
            [0,7,0, 0,0,3, 5,0,0],

            [8,0,0, 0,3,5, 7,2,0],
            [0,0,3, 0,7,0, 4,0,0],
            [0,9,2, 8,4,0, 0,0,3],

            [0,0,8, 2,0,0, 0,4,0],
            [0,0,0, 4,0,0, 0,6,7],
            [0,0,0, 0,0,0, 0,0,1]
        ] 

        solver = SudokuSolver(grid)
        self.assertTrue( solver.safest_first_solver() )
        self.assertTrue( solver.check())
        solver._debug()



    


    

if __name__ == '__main__':
    unittest.main()