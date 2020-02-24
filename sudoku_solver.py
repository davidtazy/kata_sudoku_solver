
class SudokuSolver:
    '''
        grid is column based grid[column][row]
    '''
    def __init__(self,grid):
        self._grid  = grid
        self._dead_end_counter = 0

    def brut_force(self):
        '''
        recursive function
        test randomly all solutions
        '''
        solved = True
        for col in range(9):
            for row in range(9):
                if self._grid[col][row] == 0:
                    solved = False
                    # need to solve this position
                    for number in range(1,10):
                        if self._is_possible(col,row,number):
                            # found a possible solution
                            self._grid[col][row] = number
                            # continue to solve recursivly 
                            if self.brut_force() is True:
                                # continue solving next position
                                return True
                            else:
                                # reset position and continue searching for a solution
                                self._dead_end_counter += 1
                                self._grid[col][row] = 0
                                if self._dead_end_counter %100000 == 0:
                                    self._debug()
                 
        return solved
    
    def safest_first_solver(self):
        '''
        recursive function
        fill positions with minimal solutions number first
        '''

        if self.is_filled():
            return True

        pos = self.find_safest_position_to_solve()
        
        for try_solution in  pos[1] :
            col, row = pos[0]
            
            self._grid[col][row] = try_solution
            
            if self.safest_first_solver() is True:
                # rewind 
                return self.is_filled()
            else:
                # try_solution is dead end
                self._dead_end_counter += 1
                # reset position and continue
                self._grid[col][row] = 0
                    
        return self.is_filled()

    def find_safest_position_to_solve(self):
        '''
        return tuple ( (col,row),[solutions])
        try to find position where solutions numbers are the smallest
        '''

        safest_count = 10

        ret = None

        for col in range(9): 
            for row in range(9):
                if self._grid[col][row] == 0:
                    #its a free position

                    #count possible solution
                    pcount = 0
                    possibilities = []
                    for number in range(1,10):
                        if self._is_possible(col,row,number):
                            pcount += 1
                            possibilities.append(number)
                    
                    if pcount == 1:
                        # only one number possible on this position
                        # can return directly
                        return ( (col, row),possibilities)
                    elif pcount < safest_count:
                        #found safer position
                        safest_count = pcount
                        ret = ( (col, row),possibilities)
        return ret

    
    def is_filled(self):
        '''
        return True if all positions are set
        Warning: do not check if it is correct
        ''' 
        progress = 0
        for col in range(9):
            for row in range(9):
                if self._grid[col][row] != 0:
                    progress += 1
        
        return progress == 81

    def check(self):
        '''
            from https://stackoverflow.com/a/49514404
        '''
        n = len(self._grid)
        digit = 1  #start from one
        while (digit<=n):
            i=0
            while i<n:  # go through each row and column
                row_count=0
                column_count=0
                j=0
                while j < n: # for each entry in the row / column
                    if self._grid[i][j] == digit: # check row count
                        row_count = row_count+1
                    if self._grid[j][i]== digit :
                        column_count = column_count+1
                    j=j+1
                if row_count !=1 or column_count!=1:
                    return False
                i=i+1 # next row/column
            digit = digit+1 #next digit
        return True
          
    def _debug(self):
        ''' 
        helper function to print grid and some stats
        '''
        print("dead end {}".format(self._dead_end_counter))
        try:
            import numpy as np
            non_zero = np.count_nonzero(self._grid)
            print("{}%".format(int(non_zero*100.0/81.0)))
            print(np.matrix(self._grid))
        except :
            pass
        print("-----------")


    def _is_possible(self, col, row, number):
        ''' 
        return True if @param number can be set in position [col,row]
        '''

        #check if position is free
        if self._grid[col][row] > 0:
            return False 
        
        for index in range(9):
            #check row
            if self._grid[index][row] == number :
                return False 
            
            #check column
            if self._grid[col][index] == number :
                return False 

        #check block
        for sub_col in self._range_for_block(col):
            for sub_row in self._range_for_block(row):
                if self._grid[sub_col][sub_row] == number:
                    return False

        return True

    def _range_for_block(self,index):
        ''' 
        helper function to generate correct range for block containing @param index
        '''
        if index < 3:
            return range(2)
        elif index < 6:
            return range(3,6)
        else:
            return range(6,9)

#######################################################################
#####################  Data Set #######################################


def create_zero_grid():
    return [
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,],
        [0,0,0,0,0,0,0,0,0,]]

def create_solved_grid():
    return [
        [4,7,1, 2,8,5, 9,6,3],
        [8,2,9, 4,3,6, 5,1,7],
        [5,3,6, 9,7,1, 4,8,2],

        [6,8,7, 3,9,4, 2,5,1],
        [1,5,2, 7,6,8, 3,4,9],
        [9,4,3, 5,1,2, 8,7,6],

        [2,1,5, 6,4,3, 7,9,8],
        [3,9,8, 1,5,7, 6,2,4],
        [7,6,4, 8,2,9, 1,3,5]]

def create_real_world_grid():
    return [
        [0,3,2, 0,7,0, 5,0,4],
        [0,8,1, 0,0,3, 6,9,0],
        [0,9,0, 0,0,0, 0,1,2],

        [0,0,0, 0,8,1, 0,2,0],
        [0,7,0, 2,9,5, 4,6,0],
        [0,5,0, 7,6,4, 0,3,0],

        [8,0,5, 0,3,7, 9,0,0],
        [7,1,0, 9,0,8, 2,0,3],
        [3,4,9, 5,1,0, 0,7,0]]

def create_hard_sudoku():
    return[
        [0,0,0, 0,1,3, 0,0,0],
        [0,0,0, 6,8,0, 0,1,0],
        [7,0,9, 0,0,0, 0,8,0],
        
        [0,0,0, 0,4,5, 0,0,1],
        [0,0,5, 0,0,6, 3,0,0],
        [3,4,0, 0,0,0, 0,0,0],

        [5,0,0, 0,0,9, 0,0,0],
        [0,7,0, 0,6,2, 5,9,0],
        [0,2,0, 0,0,0, 0,0,4]
    ]