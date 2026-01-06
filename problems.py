import sympy
import math
import re

# θ = L/r
# sin(θ) = Opp./Hyp.
# cos(θ) = Adj./Hyp.
# tan(θ) = Opp./Adj.
# sin²(θ) + cos²(θ) = 1
# tan(θ) = sin(θ)/cos(θ)
# Aₛₑ꜀ₜₒᵣ = 1/2 Lr = 1/2 Qr²
# Aₛₑ₉ₘₑₙₜ = 1/2 r² (θ - sin(θ))

pi = sympy.pi

quantites = ["Central Angle", "Angle", "Sine", "Cosine", "Tangent", "Arc Length", "Side Length", "Radius", "Area"]

quantites_units = {
    "Central Angle": ["Degrees", "Radians"],
    "Angle": ["Degrees", "Radians"],
    "Sine": [],
    "Cosine": [],
    "Tangent": [],
    "Arc Length": ["units", "m", "cm", "km"],
    "Side Length": ["units", "m", "cm", "km"],
    "Side Length": ["units", "m", "cm", "km"],
    "Radius": ["units", "m", "cm", "km"],
    "Area": ["units²", "m²", "cm²"],
}

def RadiansToDegrees(radians):
    if "pi" not in str(radians) or "sympy" not in str(type(radians)):
        radians = sympy.nsimplify(radians*sympy.pi/math.pi)

    return float(sympy.N((radians/sympy.pi)*180))

unit_conversion = {
    "Degrees-Radians": lambda x: x*pi/180,
    "Radians-Degrees": RadiansToDegrees,
    "m-cm": lambda x: x*100,
    "m-km": lambda x: x*0.001,
    "cm-km": lambda x: x*0.1,
    "cm-m": lambda x: x*0.01,
    "km-m": lambda x: x*1000,
    "km-cm": lambda x: x*10,
    "m²-cm²": lambda x: x*10000,
    "cm²-m²": lambda x: x*0.0001,
    "units-cm": lambda x: x,
    "cm-units": lambda x: x,
    "cm²-units²": lambda x: x,
    "units²-cm²": lambda x: x,
}

def Round(x,y):
    if type(x) == int or type(x) == float: return round(x,y)
    else: return sympy.nsimplify(x)

def toInt(number):
    if type(number) == int or type(number) == float or number == int(number): number = int(number)
    return number

class Value:
    def __init__(self, quantity: str, value, unit: str, objects: list):
        self.value = sympy.nsimplify(value)
        self.quantity = quantity
        self.unit = unit
        self.objects = objects

    def change_unit(self, newUnit: str):
        if self.unit != newUnit:
            self.value = toInt(Round(unit_conversion[f'{self.unit}-{newUnit}'](self.value), 9))
            self.unit = newUnit

    def in_another_unit(self, newUnit: str):
        if self.unit != newUnit:
            return Value(self.quantity, toInt(Round(unit_conversion[f'{self.unit}-{newUnit}'](self.value), 2)), unit=newUnit, objects=self.objects)
        
    def LaTeX(self):
        return sympy.latex(sympy.nsimplify(self.value)) + " " + self.unit.replace("Degrees", "\\degree").replace("Radians", "")
    
def findValue(quantity: str, objects: list, values: list[Value]):
    for value in values:
        if (type(value) == Value) and (value.quantity == quantity) and (value.objects == objects):
            return value

def getSolution(givenValues: list[Value], requiredValues: list[dict]) -> tuple[str, list[Value]]:
    for index, g in enumerate(givenValues):
        g[1] = eval(g[1])
        g[3] = [obj.strip() for obj in g[3].split(",")]

        givenValues[index] = Value(*g)

    for index, r in enumerate(requiredValues):
        r[2] = [obj.strip() for obj in r[2].split(",")]

        requiredValues[index] = {"quantity": r[0], "unit": r[1], "objects": r[2]}

    if givenValues and requiredValues:
        listOfSolutions = []

        unit_circle_values = []

        for value in requiredValues:
            requiredFunction: function = eval(value["quantity"].replace(" ", "_"))
            solution = requiredFunction(givenValues, value["objects"], value["unit"]) if len(quantites_units[value["quantity"]]) > 1 else requiredFunction(givenValues, value["objects"])

            if solution is None:
                listOfSolutions.append(f"Sorry$, we couldn't find the {value["quantity"]} of {", ".join(value["objects"])}$.")

            else:
                listOfSolutions.append(solution[0])
                givenValues.append(solution[1])

                if solution[1].quantity in ["Central Angle", "Tangent", "Sine", "Cosine"]: unit_circle_values.append(solution[1])

        return "$\n\n$".join(listOfSolutions), unit_circle_values
    
def get_A_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[0], objects[1]]

def get_B_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[1], objects[1]]

def get_C_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[2], objects[1]]

def get_AB_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[0]+points[1], objects[1]]

def get_AC_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[0]+points[2], objects[1]]

def get_BC_objects(objects):
    points = list(re.match("Triangle ([A-Z]{3})", objects[1]).groups()[0])
    return [points[1]+points[2], objects[1]]

def Central_Angle(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []
    if ("sector:Qr^2" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        sector_area = findValue("Area", objects, values)
        radius = findValue("Radius", objects, values)

        if (sector_area is None) and (find_sector_area := Area(values, objects, "cm²", exceptions+["sector:Qr^2"])):
            steps += 1; sol += find_sector_area[0] + "$\n$"
            sector_area = find_sector_area[1]
 
        if (radius is None) and (find_radius := Radius(values, objects, "cm", exceptions+["sector:Qr^2"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if sector_area and radius:
            if sector_area.unit[:-1] != radius.unit:
                if a := (sector_area.unit != "cm²"):
                    sol += "A_{sector}$ $=$ $" + sector_area.LaTeX() + "$ $=$ $" + (sector_area := sector_area.in_another_unit("cm²")).LaTeX() + "$\n"

                if radius.unit != "cm":
                    if a: sol += "$"
                    sol += "r$ $=$ $" + radius.LaTeX() + "$ $=$ $" + (radius := radius.in_another_unit("cm")).LaTeX() + "$\n"

                sol += "\n$"

            result = Value("Central Angle", sympy.nsimplify((2*sector_area.value) / (radius.value*radius.value)), "Radians", objects)
            sol += "A_{sector}$ $=$ $\\frac{1}{2} \\theta r^{2}$\n$" + sector_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times \\theta \\times (" + radius.LaTeX() + ")^{2}$\n$\\frac{2 \\times " + sector_area.LaTeX() + "}{" + sympy.latex(radius.value**2) + radius.unit + "^{2}}$ $=$ $\\theta$\n$" + result.LaTeX() + "$ $=$ $\\theta"

            if unit != "Radians":
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $\\theta"

            solutions.append((sol, result, steps))

    if ("segment" not in exceptions) and ("Segment" in objects[-1]):
        sol = ""
        steps = 0

        segment_area = findValue("Area", objects, values)

        radius = findValue("Radius", objects, values)
        sine = findValue("Sine", objects, values)

        if (radius is None) and (find_radius := Radius(values, objects, "cm", exceptions+["segment"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if (sine is None) and (find_sine := Sine(values, objects, exceptions+["segment"])):
            steps += 1; sol += find_sine[0] + "$\n$"
            sine = find_sine[1]

        if sine and segment_area and radius:
            if segment_area.unit[:-1] != radius.unit:
                if a := (segment_area.unit != "cm²"):
                    sol += "A_{segment}$ $=$ $" + segment_area.LaTeX() + "$ $=$ $" + (segment_area := segment_area.in_another_unit("cm²")).LaTeX() + "$\n"

                if radius.unit != "cm":
                    if a: sol += "$"
                    sol += "r$ $=$ $" + radius.LaTeX() + "$ $=$ $" + (radius := radius.in_another_unit("cm")).LaTeX() + "$\n"

                sol += "\n$"

            result = Value("Central Angle", toInt(Round(((2 * segment_area.value) / (radius.value**2)) + sine.value, 3)), "Radians", objects)
            sol += "A_{segment}$ $=$ $\\frac{1}{2} r^{2} ( \\theta - sin ( \\theta ) )$\n$" + segment_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times ( " + radius.LaTeX() + " )^{2} \\times ( \\theta - " + sine.LaTeX() + " )$\n$\\frac{2 \\times " + segment_area.LaTeX() + "}{" + sympy.latex(radius.value**2) + radius.unit + "^{2}} + " + sine.LaTeX() + "$ $=$ $\\theta$\n$" + result.LaTeX() + "$ $=$ $\\theta"

            if unit != "Radians":
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $\\theta"

            solutions.append((sol, result, steps))

    if ("Q=L/r" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        arc_length = findValue("Arc Length", objects, values)
        radius = findValue("Radius", objects, values)

        if (arc_length is None) and (find_arc_length := Arc_Length(values, objects, "cm", exceptions+["Q=L/r"])):
            steps += 1; sol += find_arc_length[0] + "$\n$"
            arc_length = find_arc_length[1]

        if (radius is None) and (find_radius := Radius(values, objects, "cm", exceptions+["Q=L/r"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if arc_length and radius:
            if arc_length.unit != radius.unit:
                if a := (arc_length.unit != "cm"):
                    sol += "L$ $=$ $" + arc_length.LaTeX() + "$ $=$ $" + (arc_length := arc_length.in_another_unit("cm")).LaTeX() + "$\n"

                if radius.unit != "cm":
                    if a: sol += "$"
                    sol += "r$ $=$ $" + radius.LaTeX() + '$ $=$ $' + (radius := radius.in_another_unit("cm")).LaTeX() + "$\n"

                sol += '\n$'

            result = Value("Central Angle", toInt(Round(arc_length.value / radius.value, 3)), "Radians", objects)
            sol += "\\theta$ $=$ $\\frac{L}{r}$\n$\\theta$ $=$ $\\frac{" + arc_length.LaTeX() + "}{" + radius.LaTeX() + "}$\n$\\theta$ $=$ $" + result.LaTeX()

            if unit != "Radians":
                result.change_unit(unit)
                sol += "$\n$\\theta$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))

    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Sine(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []
    if (angle := findValue("Angle", objects, values)) is not None:
        sol = ""
        steps = 0

        if angle.unit != "Radians":
            sol += "\\theta$ $=$ $" + angle.LaTeX() + "$ $=$ $" + (angle := angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

        result = Value("Sine", sympy.sin(angle.value), "", objects)
        sol += "sin(\\theta)$ $=$ $sin( " + angle.LaTeX() + " )$ $=$ $" + result.LaTeX()

        solutions.append((sol, result, steps))

    if len(objects) == 2:
        if objects == get_A_objects(objects):
            if "sinA=BC/Hyp" not in exceptions:
                sol = ""
                steps = 0
                
                BC = findValue("Side Length", get_BC_objects(objects), values)
                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (BC is None) and (find_BC := Side_Length(values, get_BC_objects(objects), "cm", exceptions+["sinA=BC/Hyp"])):
                    steps += 1; sol += find_BC[0] + "$\n$"
                    BC = find_BC[1]

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["sinA=BC/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0] + "$\n$"
                    hypotenuse = find_hypotenuse[1]

                if BC and hypotenuse:
                    if BC.unit != hypotenuse.unit:
                        if a := (BC.unit != "cm"):
                            sol += "\\overline{BC}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit("cm")).LaTeX() + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{AC}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")).LaTeX() + "$\n"

                        sol += "\n$"

                    result = Value("Sine", BC.value / hypotenuse.value, "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "sinA=cosC" not in exceptions:
                sol = ""
                steps = 0
                
                cosine_C = findValue("Cosine", get_C_objects(objects), values)

                if (cosine_C is None) and (find_cosine_C := Cosine(values, get_C_objects(objects), exceptions+["sinA=cosC"])):
                    steps += 1; sol += find_cosine_C[0] + "$\n$"
                    cosine_C = find_cosine_C[1]

                if cosine_C is not None:
                    result = Value("Sine", cosine_C.value, "", objects)
                    sol += "sin(A)$ $=$ $cos(C)$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "sinA^2+cosA^2=1" not in exceptions:
                sol = ""
                steps = 0
                
                cosine_A = findValue("Cosine", objects, values)

                if (cosine_A is None) and (find_cosine_A := Cosine(values, objects, exceptions+["sinA^2+cosA^2=1"])):
                    steps += 1; sol += find_cosine_A[0] + "$\n$"
                    cosine_A = find_cosine_A[1]

                if cosine_A is not None:
                    result = Value("Sine", sympy.nsimplify(sympy.real_root(1 - cosine_A.value*cosine_A.value, 2)), "", objects)
                    sol += "sin^{2}(A)$ $+$ $cos^{2}(A)$ $=$ $1$\n$sin^{2}(A)$ $+$ $(" + cosine_A.LaTeX() + ")^{2}$ $=$ $1$\n$sin^{2}(A)$ $=$ $1$ $-$ $" + sympy.latex(sympy.nsimplify(cosine_A.value*cosine_A.value)) + "$\n$sin^{2}(A)$ $=$ $" + sympy.latex(sympy.nsimplify(1 - cosine_A.value*cosine_A.value)) + "$\n$sin(A)$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "tanA=sinA/cosA" not in exceptions:
                sol = ""
                steps = 0

                cosine_A = findValue("Cosine", get_A_objects(objects), values)

                if (cosine_A is None) and (find_cosine_A := Cosine(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_cosine_A[0] + "$\n$"
                    cosine_A = find_cosine_A[1]

                tangent_A = findValue("Tangent", get_A_objects(objects), values)

                if (tangent_A is None) and (find_tangent_A := Tangent(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_tangent_A[0] + "$\n$"
                    tangent_A = find_tangent_A[1]

                if cosine_A and tangent_A:
                    result = Value("Sine", tangent_A.value * cosine_A.value, "", objects)
                    sol += "tan(A)$ $=$ $\\frac{sin(A)}{cos(A)}$\n$" + tangent_A.LaTeX() + "$ $=$ $\\frac{sin(A)}{" + cosine_A.LaTeX() + "}$\n$" + tangent_A.LaTeX() + " \\times " + cosine_A.LaTeX() + "$ $=$ $sin(A)$\n$" + result.LaTeX() + "$ $=$ $sin(A)"
                    
                    solutions.append(result, sol, steps)

        elif objects == get_C_objects(objects):
            if "sinC=AB/Hyp" not in exceptions:
                sol = ""
                steps = 0

                AB = findValue("Side Length", get_AB_objects(objects), values)
                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (AB is None) and (find_AB := Side_Length(values, get_AB_objects(objects), "cm", exceptions+["sinC=AB/Hyp"])):
                    steps += 1; sol += find_AB[0] + "$\n$"
                    AB = find_AB[1]

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["sinA=AC/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0] + "$\n$"
                    hypotenuse = find_hypotenuse[1]

                if AB and hypotenuse:
                    if AB.unit != hypotenuse.unit:
                        if a := (AB.unit != "cm"):
                            sol += "\\overline{AB}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit("cm")).LaTeX() + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{AC}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")).LaTeX() + "$\n"

                        sol += "\n$"

                    result = Value("Sine", AB.value / hypotenuse.value, "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "sinC=cosA" not in exceptions:
                sol = ""
                steps = 0
                
                cosine_A = findValue("Cosine", get_A_objects(objects), values)

                if (cosine_A is None) and (find_cosine_A := Cosine(values, get_A_objects(objects), exceptions+["sinA=cosC"])):
                    steps += 1; sol += find_cosine_A[0] + "$\n$"
                    cosine_A = find_cosine_A[1]

                if cosine_A is not None:
                    result = Value("Sine", cosine_A.value, "", objects)
                    sol += "sin(C)$ $=$ $cos(A)$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "sinC^2+cosC^2=1" not in exceptions:
                sol = ""
                steps = 0
                
                cosine_C = findValue("Cosine", objects, values)

                if (cosine_C is None) and (find_cosine_C := Cosine(values, objects, exceptions+["sinA^2+cosA^2=1"])):
                    steps += 1; sol += find_cosine_C[0] + "$\n$"
                    cosine_C = find_cosine_C[1]

                if cosine_C is not None:
                    result = Value("Sine", sympy.nsimplify(sympy.real_root(1 - cosine_C.value*cosine_C.value, 2)), "", objects)
                    sol += "sin^{2}(C)$ $+$ $cos^{2}(C)$ $=$ $1$\n$sin^{2}(C)$ $+$ $(" + cosine_C.LaTeX() + ")^{2}$ $=$ $1$\n$sin^{2}(C)$ $=$ $1$ $-$ $" + sympy.latex(sympy.nsimplify(cosine_C.value*cosine_C.value)) + "$\n$sin^{2}(C)$ $=$ $" + sympy.latex(sympy.nsimplify(1 - cosine_C.value*cosine_C.value)) + "$\n$sin(C)$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "tanC=sinC/cosC" not in exceptions:
                sol = ""
                steps = 0

                cosine_C = findValue("Cosine", objects, values)

                if (cosine_C is None) and (find_cosine_C := Cosine(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_cosine_C[0] + "$\n$"
                    cosine_C = find_cosine_C[1]

                tangent_C = findValue("Tangent", objects, values)

                if (tangent_C is None) and (find_tangent_C := Tangent(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_tangent_C[0] + "$\n$"
                    tangent_C = find_tangent_C[1]

                if cosine_C and tangent_C:
                    result = Value("Sine", tangent_C.value * cosine_C.value, "", objects)
                    sol += "tan(C)$ $=$ $\\frac{sin(C)}{cos(C)}$\n$" + tangent_C.LaTeX() + "$ $=$ $\\frac{sin(C)}{" + cosine_C.LaTeX() + "}$\n$" + tangent_C.LaTeX() + " \\times " + cosine_C.LaTeX() + "$ $=$ $sin(C)$\n$" + result.LaTeX() + "$ $=$ $sin(C)"
                    
                    solutions.append(result, sol, steps)

        elif objects == get_B_objects(objects):
            result = Value("Sine", 1, "", objects)
            sol = "sin(B)$ $=$ $sin(\\frac{\\pi}{2})$ $=$ $1"
            solutions.append((sol, result, 1))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Cosine(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []
    if (angle := findValue("Angle", objects, values)) is not None:
        sol = ""

        if angle.unit != "Radians":
            sol += "\\theta$ $=$ $" + angle.LaTeX() + "$ $=$ $" + (angle := angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

        result = Value("Cosine", sympy.cos(angle.value), "", objects)
        sol += "cos(\\theta)$ $=$ $cos( " + angle.LaTeX() + " )$ $=$ $" + result.LaTeX()

        return (sol, result)

    if len(objects) == 2:
        if objects == get_A_objects(objects):
            if "cosA=AB/Hyp" not in exceptions:
                sol = ""
                steps = 0

                AB = findValue("Side Length", get_AB_objects(objects), values)
                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (AB is None) and (find_AB := Side_Length(values, get_AB_objects(objects), "cm", exceptions+["cosA=AB/Hyp"])):
                    steps += 1; sol += find_AB[0] + "$\n$"
                    AB = find_AB[1]

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["cosA=AB/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0] + "$\n$"
                    hypotenuse = find_hypotenuse[1]

                if AB and hypotenuse:
                    AB_text = get_AB_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    if AB.unit != hypotenuse.unit:
                        if a := (AB.unit != "cm"):
                            sol += "\\overline{" + AB_text + "}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit("cm")).LaTeX() + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + hypotenuse_text + "}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")).LaTeX() + "$\n"

                        sol += "\n$"

                    steps += 1

                    result = Value("Cosine", sympy.nsimplify(AB.value/hypotenuse.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "sinC=cosA" not in exceptions:
                sol = ""
                steps = 0

                sine_C = findValue("Sine", get_C_objects(objects), values)

                if (sine_C is None) and (find_sine_C := Sine(values, get_C_objects(objects), exceptions+["sinC=cosA"])):
                    steps += 1; sol += find_sine_C[0] + "$\n$"
                    sine_C = find_sine_C[1]

                if sine_C:
                    steps += 1
                    A_text = objects[0]
                    C_text = get_C_objects(objects)[0]

                    result = Value("Cosine", sine_C.value, "", objects)
                    sol += "sin(" + C_text + ")$ $=$ $cos(" + A_text + ")$\n$" + sine_C.LaTeX() + "$ $=$ $cos(" + A_text + ")"

                    solutions.append((sol, result, steps))

            if "sinA^2+cosA^2=1" not in exceptions:
                sol = ""
                steps = 0

                sine_A = findValue("Sine", objects, values)

                if (sine_A is None) and (find_sine_A := Sine(values, objects, exceptions+["sinA^2+cosA^2=1"])):
                    steps += 1; sol += find_sine_A[0]
                    sine_A = find_sine_A[1]

                if sine_A:
                    steps += 1

                    A_text = objects[0]

                    result = Value("Cosine", sympy.nsimplify(sympy.real_root(1 - sine_A.value*sine_A.value)), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "tanA=sinA/cosA" not in exceptions:
                sol = ""
                steps = 0

                tangent_A = findValue("Tangent", objects, values)

                if (tangent_A is None) and (find_tangent_A := Tangent(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_tangent_A[0]
                    tangent_A = find_tangent_A[1]

                sine_A = findValue("Sine", objects, values)

                if (sine_A is None) and (find_sine_A := Sine(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_sine_A[0]
                    sine_A = find_sine_A[1]

                if tangent_A and sine_A:
                    steps += 1
                    A_text = objects[0]

                    result = Value("Cosine", sympy.nsimplify(sine_A.value/tangent_A.value))
                    sol += ""

                    solutions.append((sol, result, steps))

        elif objects == get_C_objects(objects):
            if "cosC=BC/Hyp" not in exceptions:
                sol = ""
                steps = 0

                BC = findValue("Side Length", get_BC_objects(objects), values)
                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (BC is None) and (find_BC := Side_Length(values, get_BC_objects(objects), "cm", exceptions+["cosC=BC/Hyp"])):
                    steps += 1; sol += find_BC[0] + "$\n$"
                    BC = find_BC[1]

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["cosC=BC/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0] + "$\n$"
                    hypotenuse = find_hypotenuse[1]

                if BC and hypotenuse:
                    BC_text = get_AB_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    if BC.unit != hypotenuse.unit:
                        if a := (BC.unit != "cm"):
                            sol += "\\overline{" + BC_text + "}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit("cm")).LaTeX() + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + hypotenuse_text + "}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")).LaTeX() + "$\n"

                        sol += "\n$"

                    steps += 1

                    result = Value("Cosine", sympy.nsimplify(BC.value/hypotenuse.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "sinA=cosC" not in exceptions:
                sol = ""
                steps = 0

                sine_A = findValue("Sine", get_A_objects(objects), values)

                if (sine_A is None) and (find_sine_A := Sine(values, get_A_objects(objects), exceptions+["sinA=cosC"])):
                    steps += 1; sol += find_sine_A[0] + "$\n$"
                    sine_A = find_sine_A[1]

                if sine_A:
                    steps += 1
                    A_text = get_A_objects(objects)[0]
                    C_text = objects[0]

                    result = Value("Cosine", sine_A.value, "", objects)
                    sol += "sin(" + A_text + ")$ $=$ $cos(" + C_text + ")$\n$" + sine_A.LaTeX() + "$ $=$ $cos(" + C_text + ")"

                    solutions.append((sol, result, steps))

            if "sinC^2+cosC^2=1" not in exceptions:
                sol = ""
                steps = 0

                sine_C = findValue("Sine", objects, values)

                if (sine_C is None) and (find_sine_C := Sine(values, objects, exceptions+["sinC^2+cosC^2=1"])):
                    steps += 1; sol += find_sine_C[0]
                    sine_C = find_sine_C[1]

                if sine_C:
                    steps += 1

                    C_text = objects[0]

                    result = Value("Cosine", sympy.nsimplify(sympy.real_root(1 - sine_C.value*sine_C.value)), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "tanC=sinC/cosC" not in exceptions:
                sol = ""
                steps = 0

                tangent_C = findValue("Tangent", objects, values)

                if (tangent_C is None) and (find_tangent_C := Tangent(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_tangent_C[0]
                    tangent_C = find_tangent_C[1]

                sine_C = findValue("Sine", objects, values)

                if (sine_C is None) and (find_sine_C := Sine(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_sine_C[0]
                    sine_C = find_sine_C[1]

                if tangent_C and sine_C:
                    steps += 1
                    C_text = objects[0]

                    result = Value("Cosine", sympy.nsimplify(sine_C.value/tangent_C.value))
                    sol += ""

                    solutions.append((sol, result, steps))

        elif objects == get_B_objects(objects):
            B_text = get_B_objects(objects)[0]
            result = Value("Cosine", 0, "", objects)
            sol = "cos(" + B_text + ")$ $=$ $cos(\\frac{\\pi}{2})$ $=$ $0"
            solutions.append((sol, result, 1)) 
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Tangent(values: list[Value], objects: list, exceptions: list[str]=[]):
    solutions = []
    if (angle := findValue("Angle", objects, values)) is not None:
        sol = ""
        steps = 0

        if angle.unit != "Radians":
            sol += "\\theta$ $=$ $" + angle.LaTeX() + "$ $=$ $" + (angle := angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

        if sympy.tan(angle.value).is_real:
            result = Value("Tangent", sympy.tan(angle.value), "", objects)
            sol += "tan(\\theta)$ $=$ $tan( " + angle.LaTeX() + " )$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))

        else: return

    if len(objects) == 2:
        if objects == get_A_objects(objects):
            if "tanA=BC/AB" not in exceptions:
                sol = ""
                steps = 0

                BC = findValue("Side Length", get_BC_objects(objects), values)

                if (BC is None) and (find_BC := Side_Length("Side Length", get_BC_objects(objects), "cm", exceptions+["tanA=BC/AB"])):
                    steps += 1; sol += find_BC[0] + "$\n$"
                    BC = find_BC[1]

                AB = findValue("Side Length", get_AB_objects(objects), values)

                if (AB is None) and (find_AB := Side_Length("Side Length", get_AB_objects(objects), "cm", exceptions+["tanA=BC/AB"])):
                    steps += 1; sol += find_AB[0] + "$\n$"
                    AB = find_AB[1]

                if AB and BC:
                    A_text = objects[0]
                    AB_text = get_AB_objects(objects)[0]
                    BC_text = get_BC_objects(objects)[0]

                    if AB.unit != BC.unit:
                        if a := (AB.unit != "cm"):
                            sol += "\\overline{" + AB_text + "}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit("cm")).LaTeX() + "$\n"

                        if BC.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + BC_text + "}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit("cm")).LaTeX() + "$\n$"

                        sol += "\n$"

                    steps += 1

                    result = Value("Tangent", sympy.nsimplify(BC.value/AB.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "tanA=sinA/cosA" not in exceptions:
                sol = ""
                steps = 0

                sine_A = findValue("Sine", objects, values)

                if (sine_A is None) and (find_sine_A := Sine(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_sine_A[0] + "$\n$"
                    sine_A = find_sine_A[1]

                cosine_A = findValue("Cosine", objects, values)

                if (cosine_A is None) and (find_cosine_A := Cosine(values, objects, exceptions+["tanA=sinA/cosA"])):
                    steps += 1; sol += find_cosine_A[0] + "$\n$"
                    cosine_A = find_cosine_A[1]

                if sine_A and cosine_A:
                    steps += 1
                    A_text = objects[0]

                    result = Value("Tangent", sympy.nsimplify(sine_A.value/cosine_A.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

        elif objects == get_C_objects(objects):
            if "tanC=AB/BC" not in exceptions:
                sol = ""
                steps = 0

                AB = findValue("Side Length", get_AB_objects(objects), values)

                if (AB is None) and (find_AB := Side_Length("Side Length", get_AB_objects(objects), "cm", exceptions+["tanC=AB/BC"])):
                    steps += 1; sol += find_AB[0] + "$\n$"
                    AB = find_AB[1]

                BC = findValue("Side Length", get_BC_objects(objects), values)

                if (BC is None) and (find_BC := Side_Length("Side Length", get_BC_objects(objects), "cm", exceptions+["tanC=AB/BC"])):
                    steps += 1; sol += find_BC[0] + "$\n$"
                    BC = find_BC[1]

                if AB and BC:
                    C_text = objects[0]
                    AB_text = get_AB_objects(objects)[0]
                    BC_text = get_BC_objects(objects)[0]

                    if AB.unit != BC.unit:
                        if a := (AB.unit != "cm"):
                            sol += "\\overline{" + AB_text + "}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit("cm")).LaTeX() + "$\n"

                        if BC.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + BC_text + "}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit("cm")).LaTeX() + "$\n$"

                        sol += "\n$"

                    steps += 1

                    result = Value("Tangent", sympy.nsimplify(AB.value/BC.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

            if "tanC=sinC/cosC" not in exceptions:
                sol = ""
                steps = 0

                sine_C = findValue("Sine", objects, values)

                if (sine_C is None) and (find_sine_C := Sine(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_sine_C[0] + "$\n$"
                    sine_C = find_sine_C[1]

                cosine_C = findValue("Cosine", objects, values)

                if (cosine_C is None) and (find_cosine_C := Cosine(values, objects, exceptions+["tanC=sinC/cosC"])):
                    steps += 1; sol += find_cosine_C[0] + "$\n$"
                    cosine_C = find_cosine_C[1]

                if sine_C and cosine_C:
                    steps += 1
                    C_text = objects[0]

                    result = Value("Tangent", sympy.nsimplify(sine_C.value/cosine_C.value), "", objects)
                    sol += ""

                    solutions.append((sol, result, steps))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:

        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Arc_Length(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []
    if "Q=L/r" not in exceptions:
        sol = ""
        steps = 0

        central_angle = findValue("Central Angle", objects, values)
        radius = findValue("Radius", objects, values)

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["Q=L/r"])):
            steps += 1; sol += find_central_angle[0] + "$\n$"
            central_angle = find_central_angle[1]

        if (radius is None) and (find_radius := Radius(values, objects, unit, exceptions+["Q=L/r"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if central_angle and radius:
            if central_angle.unit != "Radians":
                sol += "\\theta $ $=$ $ " + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n$"

            result = Value("Arc Length", toInt(Round(central_angle.value * radius.value, 3)), radius.unit, objects)
            sol += "\\theta$ $=$ $\\frac{L}{r}$\n$" + central_angle.LaTeX() + "$ $=$ $\\frac{L}{" + radius.LaTeX() + "}$\n$" + central_angle.LaTeX() + " \\times " + radius.LaTeX() + "$ $=$ $L$\n$" + result.LaTeX() + "$ $=$ $L"

            if result.unit != unit:
                result.change_unit(unit)
                sol = "$\n$" + result.LaTeX() + "$ $=$ $L"

            solutions.append((sol, result, steps))

    if "sector:Lr" not in exceptions:
        sol = ""
        steps = 0

        sector_area = findValue("Area", objects, values)
        radius = findValue("radius", objects, values)

        if (sector_area is None) and (find_sector_area := Area(values, objects, "cm²", exceptions+["sector:Lr"])):
            steps += 1; sol += find_sector_area[0] + "$\n$"
            sector_area = find_sector_area[1]
 
        if (radius is None) and (find_radius := Radius(values, objects, "cm", exceptions+["sector:Lr"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if sector_area and radius:
            if sector_area.unit[:-1] != radius.unit:
                if a := (sector_area.unit != "cm²"):
                    sol += "A_{sector}$ $=$ $" + sector_area.LaTeX() + "$ $=$ $" + (sector_area := sector_area.in_another_unit("cm²")).LaTeX() + "$\n"

                if radius.unit != "cm":
                    if a: sol += "$"
                    sol += "r$ $=$ $" + radius.LaTeX() + "$ $=$ $" + (radius := radius.in_another_unit("cm")).LaTeX() + "$\n"

                sol += "\n$"

            result = Value("Arc Length", toInt(Round(2 * sector_area.value / radius.value, 3)), radius.unit, objects)
            sol += "A_{sector}$ $=$ $\\frac{1}{2}Lr$\n$" + sector_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times L \\times " + radius.LaTeX() + "$\n$\\frac{2 \\times " + sector_area.LaTeX() + "}{" + radius.LaTeX() + "}$ $=$ $L$\n$" + result.LaTeX() + "$ $=$ $L"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $L"

            solutions.append((sol, result, steps))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Side_Length(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    if (len(objects) == 2) and (re.match("Triangle [A-Z]{3}", objects[1])):
        if objects == get_AB_objects(objects):
            solutions = []
            if "pythagorean" not in exceptions:
                sol = ""
                steps = 0

                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["pythagorean"])):
                    steps += 1; sol += find_hypotenuse[0]
                    hypotenuse = find_hypotenuse[1]

                BC = findValue("Side Length", get_BC_objects(objects), values)

                if (BC is None) and (find_BC := Side_Length(values, get_BC_objects(objects), "cm", exceptions+["pythagorean"])):
                    steps += 1; sol += find_BC[0]
                    BC = find_BC[1]

                if hypotenuse and BC:
                    steps += 1
                    AB_text = objects[0]
                    BC_text = get_BC_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    if BC.unit != hypotenuse.unit:
                        if a := (BC.unit != "cm"):
                            sol += "\\overline{" + BC_text + "}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit("cm")) + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + hypotenuse_text + "}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")) + "$\n"

                        sol += "\n$"

                    steps += 1

                    result = Value("Side Length", sympy.nsimplify(sympy.real_root(hypotenuse.value*hypotenuse.value - BC.value*BC.value, 2)), BC.unit, objects)
                    sol += ""

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "\\overline{" + AB_text + "}$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "sinC=AB/Hyp" not in exceptions:
                sol = ""
                steps = 0

                sine_C = findValue("Sine", get_C_objects(objects), values)

                if (sine_C is None) and (find_sine_C := Sine(values, get_C_objects(objects), exceptions+["sinC=AB/Hyp"])):
                    steps += 1; sol += find_sine_C[0]
                    sine_C = find_sine_C[1]

                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["sinC=AB/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0]
                    hypotenuse = find_hypotenuse[1]

                if sine_C and hypotenuse:
                    steps += 1
                    AB_text = objects[0]
                    C_text = get_C_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    result = Value("Side Length", sympy.nsimplify(sine_C.value*hypotenuse.value), hypotenuse.unit, objects)
                    sol += ""

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "$\n$" + result.LaTeX() + "$ $=$ $\\overline{" + AB_text + "}"

                    solutions.append((sol, result, steps))

            if "cosA=AB/Hyp" not in exceptions:
                sol = ""
                steps = 0

                cosine_A = findValue("Sine", get_A_objects(objects), values)

                if (cosine_A is None) and (find_cosine_A := Sine(values, get_A_objects(objects), exceptions+["sinC=AB/Hyp"])):
                    steps += 1; sol += find_cosine_A[0]
                    cosine_A = find_cosine_A[1]

                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["sinC=AB/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0]
                    hypotenuse = find_hypotenuse[1]

                if cosine_A and hypotenuse:
                    steps += 1
                    AB_text = objects[0]
                    A_text = get_A_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    result = Value("Side Length", sympy.nsimplify(cosine_A.value*hypotenuse.value), hypotenuse.unit, objects)
                    sol += ""

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "$\n$" + result.LaTeX() + "$ $=$ $\\overline{" + AB_text + "}"

                    solutions.append((sol, result, steps))

            if "tanA=BC/AB" not in exceptions:
                pass

            if "tanC=AB/BC" not in exceptions:
                pass

        elif objects == get_BC_objects(objects):
            solutions = []
            if "pythagorean" not in exceptions:
                sol = ""
                steps = 0
                
                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["pythagorean"])):
                    steps += 1; sol += find_hypotenuse[0]
                    hypotenuse = find_hypotenuse[1]

                AB = findValue("Side Length", get_AB_objects(objects), values)

                if (AB is None) and (find_AB := Side_Length(values, get_AB_objects(objects), "cm", exceptions+["pythagorean"])):
                    steps += 1; sol += find_AB[0]
                    AB = find_BC[1]

                print(hypotenuse, AB)

                if hypotenuse and AB:
                    steps += 1
                    BC_text = objects[0]
                    AB_text = get_AB_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    if AB.unit != hypotenuse.unit:
                        if a := (AB.unit != "cm"):
                            sol += "\\overline{" + AB_text + "}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit("cm")) + "$\n"

                        if hypotenuse.unit != "cm":
                            if a: sol += "$"
                            sol += "\\overline{" + hypotenuse_text + "}$ $=$ $" + hypotenuse.LaTeX() + "$ $=$ $" + (hypotenuse := hypotenuse.in_another_unit("cm")) + "$\n"

                        sol += "\n$"

                    steps += 1

                    result = Value("Side Length", sympy.nsimplify(sympy.real_root(hypotenuse.value*hypotenuse.value - AB.value*AB.value, 2)), AB.unit, objects)
                    sol += ""

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "\\overline{" + BC_text + "}$ $=$ $" + result.LaTeX()

                    solutions.append((sol, result, steps))

            if "sinA=BC/Hyp" not in exceptions:
                sol = ""
                steps = 0

                sine_A = findValue("Sine", get_A_objects(objects), values)

                if (sine_A is None) and (find_sine_A := Sine(values, get_A_objects(objects), exceptions+["sinA=BC/Hyp"])):
                    steps += 1; sol += find_sine_A[0]
                    sine_A = find_sine_A[1]

                hypotenuse = findValue("Side Length", get_AC_objects(objects), values)

                if (hypotenuse is None) and (find_hypotenuse := Side_Length(values, get_AC_objects(objects), "cm", exceptions+["sinA=BC/Hyp"])):
                    steps += 1; sol += find_hypotenuse[0]
                    hypotenuse = find_hypotenuse[1]

                if sine_A and hypotenuse:
                    steps += 1
                    BC_text = objects[0]
                    A_text = get_C_objects(objects)[0]
                    hypotenuse_text = get_AC_objects(objects)[0]

                    result = Value("Side Length", sympy.nsimplify(sine_A.value*hypotenuse.value), hypotenuse.unit, objects)
                    sol += ""

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "$\n$" + result.LaTeX() + "$ $=$ $\\overline{" + BC_text + "}"

                    solutions.append((sol, result, steps))

            if "cosC=BC/Hyp" not in exceptions:
                pass

            if "tanA=BC/AB" not in exceptions:
                pass

            if "tanC=AB/BC" not in exceptions:
                pass

        elif objects == get_AC_objects(objects):
            solutions = []
            if "pythagorean" not in exceptions:
                sol = ""
                steps = 0

                AB = findValue("Side Length", get_AB_objects(objects), values)
                BC = findValue("Side Length", get_BC_objects(objects), values)

                if AB and BC:
                    if AB.unit != BC.unit:
                        if a := (AB.unit != unit):
                            sol += "\\overline{AB}$ $=$ $" + AB.LaTeX() + "$ $=$ $" + (AB := AB.in_another_unit(unit)).LaTeX() + "$\n"

                        if BC.unit != unit:
                            if a: sol += "$"
                            sol += "\\overline{BC}$ $=$ $" + BC.LaTeX() + "$ $=$ $" + (BC := BC.in_another_unit(unit)).LaTeX() + "$\n"

                        sol += "\n$"

                    result = Value("Side Length", sympy.nsimplify(sympy.real_root(AB.value*AB.value + BC.value*BC.value, 2)), AB.unit, objects)
                    sol += "(\\overline{AB})^{2} + (\\overline{BC})^{2}$ $=$ $(\\overline{AC})^{2}$\n$( " + AB.LaTeX() + " )^{2} + ( " + BC.LaTeX() + " )^{2}$ $=$ $(\\overline{AC})^{2}$\n$\\sqrt{" + sympy.latex(AB.value**2) + ' ' + AB.unit + "^{2} + " + sympy.latex(BC.value**2) + ' ' + BC.unit + "^{2}}$ $=$ $\\overline{AC}$\n$" + result.LaTeX() + "$ $=$ $\\overline{AC}"

                    if result.unit != unit:
                        result.change_unit(unit)
                        sol += "$\n$" + result.LaTeX() + "$ $=$ $\\overline{AC}"

                    solutions.append((sol, result, steps))

            if "sinA=BC/Hyp" not in exceptions:
                pass

            if "cosA=AB/Hyp" not in exceptions:
                pass

            if "sinC=AB/Hyp" not in exceptions:
                pass

            if "cosC=BC/Hyp" not in exceptions:
                pass

            if len(solutions) == 0:
                return

            elif len(solutions) == 1:
                return solutions[0][:2]

            else:
                return min(solutions, key=lambda x: x[2])[:2]

def Radius(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []
    if ("Q=L/r" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        central_angle = findValue("Central Angle", objects, values)
        arc_length = findValue("Arc Length", objects, values)

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["Q=L/r"])):
            steps += 1; sol += find_central_angle[0] + "$\n$"
            central_angle = find_central_angle[1]

        if (arc_length is None) and (find_arc_length := Arc_Length(values, objects, unit, exceptions+["Q=L/r"])):
            steps += 1; sol += find_arc_length[0] + "$\n$"
            arc_length = find_arc_length[1]

        if central_angle and arc_length:
            if central_angle.unit != "Radians":
                sol += "\\theta$ $=$ $" + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

            result = Value("Radius", toInt(Round(arc_length.value/central_angle.value, 3)), arc_length.unit, objects)
            sol += "\\theta$ $=$ $\\frac{L}{r}$\n$" + central_angle.LaTeX() + "$ $=$ $\\frac{" + arc_length.LaTeX() + "}{r}$\n$r$ $=$ $\\frac{" + arc_length.LaTeX() + "}{" + central_angle.LaTeX() + "}$\n$r$ $=$ $" + result.LaTeX()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "r$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))
        
    if ("sector:Lr" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        sector_area = findValue("Area", objects, values)
        arc_length = findValue("Arc Length", objects, values)

        if (sector_area is None) and (find_sector_area := Area(values, objects, unit+"²", exceptions+["sector:Lr"])):
            steps += 1; sol += find_sector_area[0] + "$\n$"
            sector_area = find_sector_area[1]

        if (arc_length is None) and (find_arc_length := Arc_Length(values, objects, unit, exceptions+["sector:Lr"])):
            steps += 1; sol += find_arc_length[0] + "$\n$"
            arc_length = find_arc_length[1]

        if sector_area and arc_length:
            if sector_area.unit[:-1] != arc_length.unit:
                if a := (sector_area.unit != unit+"²"):
                    sol += "A_{sector}$ $=$ $" + sector_area.LaTeX() + "$ $=$ $" + (sector_area := sector_area.in_another_unit(unit+"²")).LaTeX() + "$\n"
                
                if arc_length.unit != unit:
                    if a: sol += "$"
                    sol += "L$ $=$ $" + arc_length.LaTeX() + "$ $=$ $" + (arc_length := arc_length.in_another_unit(unit)).LaTeX() + "$\n"

                sol += "\n$"

            result = Value("Radius", toInt(Round((2 * sector_area.value)/(arc_length.value), 3)), arc_length.unit, objects)
            sol += "A_{sector}$ $=$ $\\frac{1}{2} Lr $\n$" + sector_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times " + arc_length.LaTeX() + " \\times r$\n$\\frac{2 \\times " + sector_area.LaTeX() + "}{" + arc_length.LaTeX() + "}$ $=$ $r$\n$" + result.LaTeX() + "$ $=$ $r"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $r"

            solutions.append((sol, result, steps))

    if ("sector:Qr^2" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        sector_area = findValue("Area", objects, values)
        central_angle = findValue("Central Angle", objects, values)

        if (sector_area is None) and (find_sector_area := Area(values, objects, unit+"²", exceptions+["sector:Qr^2"])):
            steps += 1; sol += find_sector_area[0] + "$\n$"
            sector_area = find_sector_area[1]

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["sector:Qr^2"])):
            steps += 1; sol += find_central_angle[0] + "$\n$"
            central_angle = find_central_angle[1]

        if sector_area and central_angle:
            if central_angle.unit != "Radians": sol += "\\theta$ $=$ $" + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

            result = Value("Radius", toInt(Round(sympy.sqrt(2 * sector_area.value / central_angle.value), 3)), sector_area.unit[:-1], objects)
            sol += "A_{sector}$ $=$ $\\frac{1}{2} Q r^{2}$\n$" + sector_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times " + central_angle.LaTeX() + " \\times r^{2}$\n$ \\frac{2 \\times " + sector_area.LaTeX() + "}{" + central_angle.LaTeX() + "}$ $=$ $r^{2}$\n$\\sqrt{\\frac{2 \\times " + sector_area.LaTeX() + "}{" + central_angle.LaTeX() + "}}$ $=$ $r$\n$" + result.LaTeX() + "$ $=$ $r"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $r"

            solutions.append((sol, result, steps))
    
    if ("segment" not in exceptions) and ("Segment" in objects[-1]):
        sol = ""
        steps = 0

        segment_area = findValue("Area", objects, values)
        central_angle = findValue("Central Angle", objects, values)

        if (segment_area is None) and (find_segment_area := Area(values, objects, unit+"²", exceptions+["segment"])):
            steps += 1; sol += find_segment_area[0] + "$\n$"
            segment_area = find_segment_area[1]

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["segment"])):
            steps += 1; sol += find_segment_area[0] + "$\n$"
            segment_area = find_segment_area[1]

        if segment_area and central_angle:
            if central_angle.unit != "Radians": sol += "\\theta$ $=$ $" + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

            sine_value = sympy.sin(central_angle)

            result = Value("Radius", toInt(Round(sympy.sqrt((2 * segment_area.value) / (central_angle.value - sine_value)), 3)), segment_area.unit[:-1], objects)
            sol += "A_{segment}$ $=$ $\\frac{1}{2} r^{2} ( \\theta - sin ( \\theta ) )$\n$" + segment_area.LaTeX() + "$ $=$ $\\frac{1}{2} \\times r^{2} \\times ( " + central_angle.LaTeX() + " - sin ( " + central_angle.LaTeX() + " ) )$\n$\\frac{2 \\times " + segment_area.LaTeX() + "}{( " + central_angle.LaTeX() + " - " + sympy.latex(sine_value) + " )}$ $=$ $r^{2}$\n$\\sqrt{\\frac{2 \\times " + segment_area.LaTeX() + "}{( " + central_angle.LaTeX() + " - " + sympy.latex(sine_value) + " )}}$ $=$ $r$\n$" + result.LaTeX() + "$ $=$ $r"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $r"

            solutions.append((sol, result, steps))

    if "circle" not in exceptions:
        sol = ""
        steps = 0

        area = findValue("Area", objects, values)

        if (area is None) and (find_area := Area(values, objects, unit+"²", exceptions+["circle"])):
            steps += 1; sol += find_area[0] + "$\n$"
            area = find_area[1]

        if area:
            result = Value("Radius", toInt(Round(sympy.sqrt(area.value/pi), 3)), area.unit[:-1], objects)
            sol += "A_{circle}$ $=$ $ \\pi r^{2}$\n$" + area.LaTeX() + "$ $=$ $ \\pi + r^{2}$\n$\\frac{" + area.LaTeX() + "}{pi}$ $=$ $r^{2}$\n$\\sqrt{\\frac{" + area.LaTeX() + "}{pi}}$ $=$ $r$\n$" + result.LaTeX() + "$ $=$ $r"

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$" + result.LaTeX() + "$ $=$ $r"

            solutions.append((sol, result, steps))

    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

def Area(values: list[Value], objects: list, unit: str, exceptions: list[str]=[]):
    solutions = []

    if ("sector:Lr" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        arc_length = findValue("Arc Length", objects, values)
        radius = findValue("Radius", objects, values)

        if (arc_length is None) and (find_arc_length := Arc_Length(values, objects, "cm", exceptions+["sector:Lr"])):
            steps += 1; sol += find_arc_length[0] + "$\n$"
            arc_length = find_arc_length[1]

        if (radius is None) and (find_radius := Radius(values, objects, "cm", exceptions+["sector:Lr"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if arc_length and radius:
            if arc_length.unit != radius.unit:
                if a := (arc_length.unit != "cm"):
                    sol += "L$ $=$ $" + arc_length.LaTeX() + "$ $=$ $" + (arc_length := arc_length.in_another_unit("cm")).LaTeX() + "$\n"

                if radius.unit != "cm":
                    if a: sol += "$"
                    sol += "r$ $=$ $" + radius.LaTeX() + '$ $=$ $' + (radius := radius.in_another_unit("cm")).LaTeX() + "$\n"

                sol += '\n$'

            result = Value("Area", toInt(Round(arc_length.value * radius.value / 2, 3)), f"{radius.unit}²", objects)
            sol += "A_{sector}$ $=$ $\\frac{1}{2}Lr$\n$A_{sector}$ $=$ $\\frac{1}{2} \\times " + arc_length.LaTeX() + " \\times " + radius.LaTeX() + "$\n$A_{sector}$ $=$ $" + result.LaTeX()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$A_{sector}$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))
        
    if ("sector:Qr^2" not in exceptions) and ("Sector" in objects[-1]):
        sol = ""
        steps = 0

        central_angle = findValue("Central Angle", objects, values)
        radius = findValue("Radius", objects, values)

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["sector:Qr^2"])):
            steps += 1; sol += find_central_angle[0] + "$\n$"
            central_angle = find_central_angle[1]

        if (radius is None) and (find_radius := Radius(values, objects, unit[:-1], exceptions+["sector:Lr"])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if central_angle and radius:
            if central_angle.unit != "Radians": sol += "\\theta$ $=$ $" + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"

            result = Value("Area", toInt(Round((central_angle.value * (radius.value**2)) / 2, 3)), f"{radius.unit}²", objects)
            sol += "A_{sector} $ $=$ $ \\frac{1}{2} \\theta r^{2}$\n$A_{sector}$ $=$ $ \\frac{1}{2} \\times " + central_angle.LaTeX() + " \\times ( " + radius.LaTeX() + " )^{2}$\n$A_{sector}$ $=$ $" + result.LaTeX()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "A_{sector}$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))
        
    if ("segment" not in exceptions) and ("Segment" in objects[-1]):
        sol = ""
        steps = 0

        radius = findValue("Radius", objects, values)
        central_angle = findValue("Central Angle", objects, values)

        if (radius is None) and (find_radius := Radius(values, objects, unit[:-1], exceptions+['segment'])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]

        if (central_angle is None) and (find_central_angle := Central_Angle(values, objects, "Radians", exceptions+["segment"])):
            steps += 1; sol += find_central_angle[0] + "$\n$"
            central_angle = find_central_angle[1]

        if radius and central_angle:
            if central_angle.unit != "Radians":
                sol += "\\theta$ $=$ $" + central_angle.LaTeX() + "$ $=$ $" + (central_angle := central_angle.in_another_unit("Radians")).LaTeX() + "$\n\n$"
            
            sine_value = sympy.sin(central_angle.value)

            result = Value("Area", toInt(Round((radius.value**2) * (central_angle.value - sine_value) / 2, 3)), f"{radius.unit}²", objects)
            sol += "A_{segment}$ $=$ $ \\frac{1}{2} r^{2} ( \\theta - sin( \\theta ) )$\n$A_{segment}$ $=$ $\\frac{1}{2} \\times ( " + radius.LaTeX() + " )^{2} \\times ( " + central_angle.LaTeX() + " - sin( " + central_angle.LaTeX() + " ) )$\n$A_{segment}$ $=$ $\\frac{1}{2} \\times " + sympy.latex(radius.value**2) + radius.unit + "^{2} \\times ( " + central_angle.LaTeX() + " - " + sympy.latex(sine_value) + " )$\n$A_{segment}$ $=$ $" + result.LaTeX()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$A_{segment}$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))
        
    if ("circle" not in exceptions) and ("Circle" in objects[-1]):
        sol = ""
        steps = 0

        radius = findValue("Radius", objects, values)

        if (radius is None) and (find_radius := Radius(values, objects, unit[:-1], exceptions+['circle'])):
            steps += 1; sol += find_radius[0] + "$\n$"
            radius = find_radius[1]
            steps += 1

        if radius:
            result = Value("Area", toInt(Round(pi*(radius.value**2), 3)), radius.unit+'²', objects)
            sol += "A_{circle}$ $=$ $ \\pi r^{2}$ $=$ $ \\pi \\times ( " + radius.LaTeX() + " )^{2}$ $=$ $" + result.LaTeX()

            if result.unit != unit:
                result.change_unit(unit)
                sol += "$\n$A_{circle}$ $=$ $" + result.LaTeX()

            solutions.append((sol, result, steps))
    
    if len(solutions) == 0:
        return

    elif len(solutions) == 1:
        return solutions[0][:2]

    else:
        return min(solutions, key=lambda x: x[2])[:2]

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams["mathtext.default"] = "regular"

    #======> Random Examples:

    # g = [["Radius", "6", "m", "Sector"], ["Area", "9*pi", "m²", "Sector"]]
    # r = [["Central Angle", "Radians", "Sector"]]

    # g = [["Radius", "6", "m", "Sector"], ["Central Angle", "pi/2", "Radians", "Sector"]]
    # r = [["Area", "m²", "Sector"]]

    # g = [["Central Angle", "90", "Degrees", "Sector"], ["Area", "9*pi", "m²", "Sector"]]
    # r = [["Radius", "m", "Sector"]]

    # g = [["Side Length", "4", "cm", "AB, Triangle ABC"], ["Side Length", "3", "cm", "BC, Triangle ABC"]]
    # r = [["Side Length", "cm", "AC, Triangle ABC"]]

    #======> Examples from the textbook:

    #--> Page 66, Excercises (4-1), Q4
    # g = [["Central Angle", "135", "Degrees", "Circle"], ["Radius", "8", "cm", "Circle"]]
    # r = [["Arc Length", "cm", "Circle"]]

    #--> Page 66, Excercises (4-1), Q3
    # g = [["Central Angle", "5/6", "Radians", "Sector"], ["Arc Length", "25", "cm", "Sector"]]
    # r = [["Radius", "cm", "Sector"]]

    #--> Page 78, Example 13
    # g = [["Central Angle", "60", "Degrees", "Sector"], ["Radius", "8", "cm", "Sector"]]
    # r = [["Area", "cm²", "Sector"]]

    #--> Page 78, Example 14
    g = [["Area", "15", "cm²", "Sector"], ["Arc Length", "6", "cm", "Sector"]]
    r = [["Central Angle", "Degrees", "Sector"]]

    text, _ = getSolution(g,r)

    plt.text(0,0, f"${text}$", fontsize=32)
    plt.show()