import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) is self.count:
            return self.cells
        return {None}

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count is 0:
            return self.cells
        return {None}

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def get_sentence(self):
        """
        Getter for the information in the sentence.
        """
        return self.cells, self.count

    def update(self, cells, count):
        """
        Updates sentence if it can be inferred"
        """
        self.cells = cells
        self.count = count


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Select neighbouring cells that are not in moves_made
        cells = set()
        (x, y) = cell
        for i in range(x - 1, x + 2):
            if i < 0 or i >= self.height:
                continue

            for j in range(y - 1, y + 2):
                if j < 0 or j >= self.width:
                    continue

                if (i, j) in self.mines:
                    count = count - 1
                elif (i, j) not in self.moves_made and \
                        (i, j) not in self.safes:
                    cells.add((i, j))
        # Add the new gained knowledge to the knowledge base
        self.knowledge.append(Sentence(cells, count))

        # Look if any sentence in the knowledge base knows any safes or mines or if two sentences can be inferred
        # until no sentences can be inferred
        while True:
            self.safe_mines()
            inferred = self.inferred_knowledge()
            if not inferred:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Safe moves are the difference between safes moves_made
        moves = self.safes - self.moves_made

        # If a safe move exists choose a random one
        if len(moves) is not 0:
            return moves.pop()

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                moves.add((i, j))

        moves = moves.difference(self.moves_made)
        moves = moves.difference(self.mines)

        if len(moves) is not 0:
            return moves.pop()  # random.sample(moves, 1)

        return None

    def safe_mines(self):
        """
        Check if any sentence in the knowledge base can determine if
        """
        new_mines = set()
        new_safes = set()
        for sentence in self.knowledge:
            # Add new mines and safes to the respective sets
            new_mines = new_mines | sentence.known_mines()
            new_safes = new_safes | sentence.known_safes()

        # Remove None from the sets
        new_mines = new_mines - {None}
        new_safes = new_safes - {None}

        # Mark any new mines and safes in the knowledge base accordingly
        for mine in new_mines:
            self.mark_mine(mine)
        for safe in new_safes:
            self.mark_safe(safe)

    def inferred_knowledge(self):
        """
        Check if any sentence can be inferred and does so if there are any.
        Returns true if sentences were inferred.
        """
        inferred = False
        for i in range(len(self.knowledge) - 1):
            (cells_i, count_i) = self.knowledge[i].get_sentence()
            if len(cells_i) is 0:
                continue

            for j in range(i + 1, len(self.knowledge)):
                (cells_j, count_j) = self.knowledge[j].get_sentence()
                if len(cells_j) is 0:
                    continue

                # Check if cell_j is subset of cell_i
                if cells_i >= cells_j:
                    self.knowledge[i].update(cells_i - cells_j, count_i - count_j)
                    inferred = True
                # Check if cell_i is subset of cell_j
                elif cells_i <= cells_j:
                    self.knowledge[j].update(cells_j - cells_i, count_j - count_i)
                    inferred = True

        return inferred
