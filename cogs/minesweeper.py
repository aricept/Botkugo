import discord
from discord.ext import commands
from discord import app_commands
import random
import math

class Minesweeper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @commands.command(name="minesweeper", aliases=["ms"])
    async def new_game(self, ctx, width: commands.Range[int, 3, 15]=9, height: commands.Range[int, 3, 15]=9, bombs: int=12):
        """
        Start a new game of minesweeper.

        Optionally, a game grid width, height, and number of bombs may be passed in.

        Parameters
        ----------
        width : int
            The width of the game grid (3-15) (optional)
        height : int
            The height of the game grid (3-15) (optional)
        bombs : int
            The number of bombs to include on the game grid (1- 1/3 the grid size) (optional)
        """
        max_bombs = math.floor((width * height) / 3)
        if bombs < 1:
            raise commands.RangeError(bombs, 1, (width * height) / 3)
        if bombs > max_bombs:
            bombs = max_bombs
            await ctx.send(f"Max bombs allowed for {width}x{height} board is {max_bombs}, using {max_bombs}.")
        board = Board(width, height, bombs)
        await ctx.send(f"Grid: {width}x{height} | Bombs: {bombs}\n{board.get_board()}")
        
    @new_game.error
    async def new_game_error(self, ctx, error):
        # Error handler for the new_game command. Used to alert on specific errors, otherwise just an alert for coder to check logs
        if isinstance(error, commands.RangeError):
            return await ctx.send("Board width and height must be between 3 and 15, and number of bombs must be at least one, up to 1/3 of the board size. Please try again.")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send("Please enter a valid number for width, height, and number of bombs.")
        else:
            await ctx.send(f"`ERROR` - we encountered an unknown error. Sorry about that.")
            raise error

class Board:
    def __init__(self, width: int, height: int, bombs: int):
        self._width = width
        self._height = height
        self._bombs = bombs
        # Dictionary emoji lookup
        self._icons = {
            0: "||:zero:||",
            1: "||:one:||",
            2: "||:two:||",
            3: "||:three:||",
            4: "||:four:||",
            5: "||:five:||",
            6: "||:six:||",
            7: "||:seven:||",
            8: "||:eight:||",
            "bomb": "||:boom:||"
        }
        # Creates game board width wide and height high
        self.board = [[0 for x in range(self._width)] for y in range(self._height)]
        for i in range(self._bombs):
            self._place_bomb()        

    def _place_bomb(self):
        column = random.randint(0, self._width - 1)
        row = random.randint(0, self._height - 1)
        if self.board[row][column] == "bomb":
            # If there is already a bomb in this spot, pick a different spot
            self._place_bomb()
        else:
            self.board[row][column] = "bomb"
            for x in [row - 1, row, row + 1]:
                # Stay within row boundary
                if x > self._height - 1 or x < 0:
                    continue
                for y in [column - 1, column, column + 1]:
                    # Stay within column boundary, ignore if there is a bomb
                    if y > self._width - 1 or y < 0 or self.board[x][y] == "bomb":
                        continue
                    else:
                        # Increment value at this coordinate
                        self.board[x][y] += 1

    def get_board(self):
        # Turns the 2D array into a string formatted with Discord emoji codes and spoiler tags
        rows = []
        for row in self.board:
            formatted = [self._icons[cell] for cell in row]
            rows.append("".join(formatted))
        return "\n".join(rows)

async def setup(bot):
    await bot.add_cog(Minesweeper(bot))
