import matplotlib.pyplot as plt
import sympy
import math

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["mathtext.default"] = "regular"

def toInt(number):
    if number == int(number): number = int(number)
    return number

def degreesToAngle(degrees):
    radians = degrees*sympy.pi/180
    return Angle(degrees, radians, sympy.sin(radians), sympy.cos(radians), sympy.tan(radians))

def radiansToAngle(radians):
    if "pi" not in str(radians): radians = sympy.nsimplify(radians*sympy.pi/math.pi)

    degrees = (radians/sympy.pi)*180
    return Angle(degrees, radians, sympy.sin(radians), sympy.cos(radians), sympy.tan(radians))

class Angle:
    def __init__(self, degrees, radians, sine, cosine, tangent):
        self.degrees = degrees
        self.radians = radians
        self.sine = sine
        self.cosine = cosine
        self.tangent = tangent

    def __repr__(self) -> str:
        return f"Degrees: {self.degrees}, Radians: {self.radians}, Sine: {self.sine}, Cosine: {self.cosine}, Tangent: {self.tangent}"

def getAnglesBySine(sine) -> list[Angle]:
    x = sympy.Symbol("x", real=True, positive=True)
    equation = sympy.Eq(sympy.sin(x), sine)
    solution_set = sympy.solve(equation)

    return [radiansToAngle(radians) for radians in solution_set]

def getAnglesByCosine(cosine) -> list[Angle]:
    x = sympy.Symbol("x", real=True)
    equation = sympy.Eq(sympy.cos(x), cosine)
    solution_set = sympy.solve(equation)

    return [radiansToAngle(radians) for radians in solution_set]

def getAnglesByTangent(tangent) -> list[Angle]:
    x = sympy.Symbol("x", real=True)
    equation = sympy.Eq(sympy.tan(x), tangent)
    solution_set = sympy.solve(equation)

    return [radiansToAngle(radians) for radians in solution_set]

def showAngle(angle: Angle):
    text = "Degrees: $" + sympy.latex(angle.degrees) + "\\degree$, Radians: $" + sympy.latex(angle.radians) + "$\nSine: $" + sympy.latex(sympy.N(angle.sine, 3)) + "$, Cosine: $" + sympy.latex(sympy.N(angle.cosine, 3)) + "$, Tangent: $" + sympy.latex(sympy.N(angle.tangent, 3)) + "$"

    figure = plt.figure(figsize=(6,6))
    ax = figure.add_subplot()

    circle = plt.Circle((0,0), 1, color="black", fill=False, linewidth=1.5)
    ax.add_patch(circle)
    ax.set_aspect('equal', adjustable='box')
    figure.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    
    ax.set_xticks(range(-10, 11, 1))
    ax.set_yticks(range(-10, 11, 1))

    line1 = plt.plot([0, angle.cosine], [0, angle.sine], color="black", linewidth=1.5)
    line2 = plt.plot([angle.cosine, angle.cosine], [0, angle.sine], color="blue", linestyle="dashed", linewidth=1.5)
    line3 = plt.plot([0, angle.cosine], [0, 0], color="red", linestyle="dotted", linewidth=2)

    label = plt.text(angle.cosine, angle.sine, text, fontsize=16, color="orange")

    plt.grid(axis='both')
    plt.title("Unit Circle: " + str(angle.degrees) + "°")
    # plt.show()

if __name__ == "__main__":
    angle = degreesToAngle(90)
    showAngle(angle)
    plt.show()