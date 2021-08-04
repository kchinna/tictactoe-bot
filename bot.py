import os
import discord
from discord.ext import commands
client = commands.Bot(command_prefix="!")

grid = []
P1 = ""
P2 = ""
currentTurn = ""
gameOn = False
count = 0


# Makeshift method of making this a constant (unchangeable) value
def getConstant():
    startGrid = [":one:", ":two:", ":three:",
                 ":four:", ":five:", ":six:",
                 ":seven:", ":eight:", ":nine:"]
    return startGrid


# outlines positions that would result in a win (3 in a row)
winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.command()
async def tictactoe(ctx, p1:discord.Member, p2:discord.Member):
    global P1
    global P2
    global currentTurn
    global gameOn
    global count

    if gameOn is False:  # only allow you to start game if it is not already running
        global grid
        grid = [":one:", ":two:", ":three:",
                ":four:", ":five:", ":six:",
                ":seven:", ":eight:", ":nine:"]
        currentTurn = ""
        gameOn = True  # game has been started
        P1 = p1
        P2 = p2

        # print tictactoe grid
        line = ""
        for i in range(len(grid)):
            if i == 2 or i == 5 or i == 8:
                line += " " + grid[i]
                await ctx.send(line)
                line = ""
            else:
                line += " " + grid[i]

        # P1 goes first
        currentTurn = P1
        await ctx.send("<@" + str(P1.id) + ">'s Turn")

    else:
        await ctx.send("Error: Game in Progress\nEnd it with !end")


@client.command()
async def place(ctx, pos:int):
    global currentTurn
    global P1
    global P2
    global grid
    global count
    global gameOn

    if gameOn:
        mark = ""
        if currentTurn == ctx.author:
            if currentTurn == P1:
                mark = ":negative_squared_cross_mark:"
            elif currentTurn == P2:
                mark = ":o2:"

            if 0 < pos < 10 and grid[pos-1] in getConstant():  # if valid !place command
                grid[pos-1] = mark
                count += 1

                # print tictactoe grid
                line = ""
                for i in range(len(grid)):
                    if i == 2 or i == 5 or i == 8:
                        line += " " + grid[i]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + grid[i]

                checkWinner(winConditions, mark)

                if gameOn is False:
                    await ctx.send(mark + " wins!")
                    count = 0
                elif count >= 9:
                    gameOn = False
                    count = 0
                    await ctx.send("tie!")

                # change turns
                if currentTurn == P1:
                    currentTurn = P2
                elif currentTurn == P2:
                    currentTurn = P1

            else:  # invalid !place command
                if pos >= 10 or pos <= 0:
                    await ctx.send("The value must be between 1-9")
                else:
                    await ctx.send("This position has already been filled")
        else:
            await ctx.send("Wait your turn, it's <@" + str(currentTurn.id) + ">'s turn")
    else:
        await ctx.send("No game running, say !tictactoe to start one")


# Ends game and notifies user
@client.command()
async def end(ctx):
    global gameOn
    gameOn = False
    global count
    count = 0
    await ctx.send("You have ended the game :(")


# Checks if position of mark is 3 in-a-row
# Uses possible win conditions from winConditions 2D list
def checkWinner(winConditions, mark):
    global gameOn
    for winPossible in winConditions:
        if grid[winPossible[0]] == mark and grid[winPossible[1]] == mark and grid[winPossible[2]] == mark:
            gameOn = False


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Must tag 2 players to play")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Tag by saying @username")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Enter a position you would like to mark")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Value must be an integer")


client.run(os.environ['TOKEN'])
