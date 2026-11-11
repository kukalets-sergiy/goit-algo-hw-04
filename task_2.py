"""Draw a Koch snowflake using recursive turtle graphics."""

import argparse
from typing import Any


def koch_curve(pen: Any, length: float, level: int) -> None:
    """Draw one Koch curve segment recursively."""
    # level is the current recursion depth, and length is the length of the line segment to draw.
    #recursion depth is the number of times the function will call itself to create smaller segments of the Koch curve.
    # If the recursion level is 0, draw a straight line segment of the specified length.
    if level == 0:
        # Move the turtle forward by the specified length without drawing.
        pen.forward(length)
        return

    # part is the length of each segment in the next recursion level, which is one-third of the current length.
    part = length / 3
    # recursive call to draw the first segment of the Koch curve. level is decreased by 1 to move to the next recursion level.
    koch_curve(pen, part, level - 1)
    # Turn the turtle left by 60 degrees to prepare for the second segment.
    pen.left(60)
    # recursive call to draw the second segment of the Koch curve.
    koch_curve(pen, part, level - 1)
    # Turn the turtle right by 120 degrees to prepare for the third segment.
    pen.right(120)
    # recursive call to draw the third segment of the Koch curve.
    koch_curve(pen, part, level - 1)
    # Turn the turtle left by 60 degrees to prepare for the fourth segment.
    pen.left(60)
    # recursive call to draw the fourth segment of the Koch curve.
    koch_curve(pen, part, level - 1)


def draw_snowflake(level: int, length: float = 300) -> None:
    """Open a turtle window and draw a three-sided Koch snowflake."""
    # turtle is a built-in Python library for creating simple graphics and animations.
    # It provides a way to control a turtle that can move around the screen, drawing lines as it goes.
    import turtle

    # Create a turtle screen with a title and background color.
    screen = turtle.Screen()
    screen.title(f"Koch snowflake, recursion level {level}")
    # Set the background color of the turtle screen.
    screen.bgcolor("yellow")

    # Create a turtle object (pen) to draw the Koch snowflake.
    pen = turtle.Turtle()
    # Set the drawing speed of the turtle to the fastest setting (0).
    pen.speed(0)
    # Set the color of the turtle's pen to "royal blue" for drawing the snowflake.
    pen.color("royal blue")
    # Move the turtle to the starting position for drawing the snowflake without drawing a line.
    pen.penup()
    # .goto(x, y) moves the turtle to the specified (x, y) coordinates on the screen.
    pen.goto(-length / 2, length / 3)
    # .pendown() puts the turtle's pen down, allowing it to draw lines as it moves.
    pen.pendown()

    # iterate three times to draw the three sides of the Koch snowflake.
    for _ in range(3):
        # Call the koch_curve function to draw one side of the snowflake with the specified length and recursion level.
        koch_curve(pen, length, level)
        # Turn the turtle right by 120 degrees to prepare for drawing the next side of the snowflake.
        pen.right(120)

    # .hideturtle() hides the turtle cursor after drawing is complete, making the final image cleaner.
    pen.hideturtle()
    # .mainloop() starts the turtle graphics event loop, allowing the window to remain open until the user closes it.
    screen.mainloop()


def parse_arguments() -> argparse.Namespace:
    """Parse the optional recursion level."""
    # Create an argument parser with a description of the program.
    parser = argparse.ArgumentParser(description="Draw a Koch snowflake.")
    #
    parser.add_argument(
        "level", # The name of the command-line argument that specifies the recursion level for drawing the Koch snowflake.
        nargs="?", # Makes the argument optional (0 or 1 value).
        type=int,
        help="recursion level from 0 to 6",
    )
    # Return the parsed arguments as a Namespace object, which allows access to the argument values using dot notation (e.g., arguments.level).
    return parser.parse_args()


def main() -> None:
    """Read the recursion level and draw the snowflake."""
    # Parse command-line arguments to get the recursion level.
    arguments = parse_arguments()
    # Get the recursion level from the parsed arguments.
    level = arguments.level
    if level is None:
        level = int(input("Enter recursion level (0-6): "))
    if not 0 <= level <= 6:
        raise SystemExit("Recursion level must be between 0 and 6.")
    # Call the draw_snowflake function with the specified recursion level to draw the Koch snowflake.
    draw_snowflake(level)


# The following code is executed when the script is run directly (not imported as a module).
if __name__ == "__main__":
    main()
