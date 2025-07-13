import numpy as np
import matplotlib.pyplot as plt

# Define the function that we want to find the root for:
# 3sin(2x) + 4cos(x) = 5  =&gt;  3sin(2x) + 4cos(x) - 5 = 0
def equation_to_solve(x):
    return 3 * np.sin(2*x) + 4 * np.cos(x) - 5

def equation_to_solve_2(x):
    return 3 * np.sin(2*x) + 4 * np.cos(2*x) - 5

x = np.linspace(-np.pi, np.pi, 500) # Range for plotting (0 to 2pi for trigonometric functions)

for i in range(2):
    if i == 0:
        y = equation_to_solve(x)
        label = '3sin(2x) + 4cos(x) - 5'
    else:
        y = equation_to_solve_2(x)
        label = '3sin(2x) + 4cos(2x) - 5'

    x_crossings = []

    # for y not crossing the zero but tangent it ------------------------------------------
    zero_indices = np.where(np.round(y, 2) == 0)[0]

    if len(zero_indices) > 0:
        diff = np.diff(zero_indices)

        # Find split positions where the difference is not 1.
        # Adding 1 shifts the breakup index to the start of the new segment.
        split_indices = np.where(diff != 1)[0] + 1

        # Split the original array into segments of consecutive numbers.
        segments = np.split(zero_indices, split_indices)

        # For each segment, if there's more than one element, take the element just before the end.
        result = [seg[-2] if seg.size > 1 else seg[0] for seg in segments]

        for index in np.unique(result):
            x_crossings.append(x[index])

    # for y crossing the zero --------------------------------------------------------------
    # Find indices where the sign of y changes.
    # This means consecutive points where y values have opposite signs.
    crossing_indices = np.where(np.diff(np.sign(y)) != 0)[0]
    # print("Indices where sign changes:", crossing_indices)

    # Compute the zero crossing points via linear interpolation
    for idx in crossing_indices:
        # Get points on either side of the crossing
        x1, x2 = x[idx], x[idx+1]
        y1, y2 = y[idx], y[idx+1]

        # Avoid division by zero (if y2 == y1, it might need special handling)
        if y2 - y1 == 0:
            continue

        # Linear interpolation formula (x_zero - x1) / (0 - y1) = (x2 - x1) / (y2 - y1) = שיפוע הישר
        x_zero = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
        x_crossings.append(x_zero)

    x_crossings = np.unique(np.round(x_crossings, 2)) # Remove duplicates

    if len(x_crossings) > 0:
        print("Zero crossings (x-coordinates):", x_crossings)
    else:
        print("No zero crossings found.")

    # Plotting the equation and the solutions ------------------------------------------------
    plt.figure(figsize=(10, 6))
    # Show the solutionss on the plot
    if len(x_crossings) > 0:
        for sol in x_crossings:
            plt.annotate(f'{sol:.2f}', xy=(sol, 0), xytext=(0, 10),
                textcoords='offset points', ha='center', color='red')
        # Mark the solutionss as green o points
        plt.plot(x_crossings, np.zeros_like(x_crossings), 'go',
                  markersize=8, label='Solutions (roots)')

    # Plot the function
    plt.plot(x, y, label=label)
    plt.axhline(0, color='r', linestyle='--', label='y=0 (Target)') # Mark y=0

    plt.xlabel('x')
    plt.ylabel(label)
    plt.title('Plot of the equation and the solutions')
    plt.legend()
    plt.grid(True)
    plt.show()
