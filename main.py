from matplotlib import pyplot as plt
import math
import numpy as np


class App:
    class LineEquations:
        # Equation for the right diagonal line
        def get_line_right(x):
            return math.cos(math.radians(60)) * x

        # Equation for the left diagonal line
        def get_line_left(x):
            return -math.cos(math.radians(60)) * x

    def __init__(self):
        # Initialize the plot with figure and axes
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_xlim(-1, 1)  # Set x-axis limits
        self.ax.set_ylim(-1, 1)  # Set y-axis limits

        self.fig.canvas.manager.set_window_title("Region Tracker")

        # Draw the dividing lines
        self.draw_lines()

        # Variable to store the current filled region
        self.region_fill = None

        plt.connect("motion_notify_event", self.mouse_move)

    # Method to draw dividing lines for the regions
    def draw_lines(self):
        # Draw the right diagonal line
        plt.axline(xy1=(0, 0), slope=math.cos(math.radians(60)))
        # Draw the left diagonal line
        plt.axline(xy1=(0, 0), slope=-math.cos(math.radians(60)))
        # Draw the vertical line
        plt.axline(xy1=(0, 0), xy2=(0, 1))

    # Mouse movement handler
    def mouse_move(self, event):
        x, y = event.xdata, event.ydata  # Get mouse coordinates

        region = ""  # Variable to store which region the mouse is in
        if not (x, y) == (None, None):  # Ensure the mouse is within the axes
            # Check conditions relative to the dividing lines
            greaterThanLineRight = y > self.LineEquations.get_line_right(x)
            greaterThanLineLeft = y > self.LineEquations.get_line_left(x)
            greaterThanLineVertical = x > 0

            # Determine the region based on conditions
            if greaterThanLineVertical and greaterThanLineRight:  # Top right
                region = 1
            elif not greaterThanLineRight and greaterThanLineLeft:  # Right
                region = 2
            elif not greaterThanLineLeft and greaterThanLineVertical:  # Bottom right
                region = 3
            elif (
                not greaterThanLineVertical and not greaterThanLineRight
            ):  # Bottom left
                region = 4
            elif greaterThanLineRight and not greaterThanLineLeft:  # Left
                region = 5
            elif not greaterThanLineVertical and greaterThanLineLeft:  # Top Left
                region = 6

        # Call the method to highlight the region
        self.draw_region(region)

    # Method to highlight the appropriate region
    def draw_region(self, region):
        x = np.linspace(-1, 1)  # Generate x-values

        # Compute y-values for the diagonal lines
        y_right = np.array([self.LineEquations.get_line_right(xi) for xi in x])
        y_left = np.array([self.LineEquations.get_line_left(xi) for xi in x])
        y_top = np.full_like(x, 1)  # Top boundary
        y_bottom = np.full_like(x, -1)  # Bottom boundary

        # Remove the previous filled region if it exists
        if self.region_fill and self.region_fill in self.ax.collections:
            self.region_fill.remove()

        match region:
            case 1:  # Top right region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_top,
                    y_right,
                    where=(x >= 0),
                    color="lightpink",
                )
            case 2:  # Right region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_left,
                    y_right,
                    where=(x >= 0),
                    color="lightpink",
                )
            case 3:  # Bottom right region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_bottom,
                    y_left,
                    where=(x >= 0),
                    color="lightpink",
                )
            case 4:  # Bottom left region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_bottom,
                    y_right,
                    where=(x <= 0),
                    color="lightpink",
                )
            case 5:  # Left region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_left,
                    y_right,
                    where=(x <= 0),
                    color="lightpink",
                )
            case 6:  # Top left region
                self.region_fill = self.ax.fill_between(
                    x,
                    y_top,
                    y_left,
                    where=(x <= 0),
                    color="lightpink",
                )

        # Update the figure to reflect the changes
        self.ax.figure.canvas.draw()

    # Run the application
    def run(self):
        plt.show()


# Entry point of the program
if __name__ == "__main__":
    app = App()
    app.run()
