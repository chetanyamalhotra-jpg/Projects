print("Welcome to Smart BMI calculator")

#Ask for user's name
name = input("Enter your name:")

#Ask for age
Age = int(input("Enter your Age:"))

#Ask for Height(in meters)
Height = float(input("Enter your Height in meter:"))

#Ask for Weight(in Kg)
Weight = float(input("Enter your weight in kg:"))

#BMI formula
BMI = (Weight / Height ** 2)
print(f"Hello {name}")
print(f"Your BMI is: {BMI:.2f}")

#BMI Classification
if BMI <=18.5:
    print("You are Underweight")
elif BMI >18.5 and BMI <=24.9:
    print("You are Normalweight")
elif BMI >24.9 and BMI <=29.9:
    print("You are Overweight")
elif BMI >29.9:
    print("You are Obese")