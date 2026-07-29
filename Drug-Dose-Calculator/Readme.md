# 💊 Drug Dose Calculator

An educational Python application that calculates approximate weight-based doses for commonly used medications.

> ⚠️ **Disclaimer:** This project is for educational purposes only and **must not** be used for real clinical decision-making. Always consult current clinical guidelines and a qualified healthcare professional before prescribing or administering medication.

---

## Features

- Calculate weight-based doses for:
  - Paracetamol
  - Amoxicillin
  - ORS (simplified maintenance fluid calculation)
- Input validation
  - Prevents empty inputs
  - Prevents negative or zero values
  - Handles non-numeric input
- Menu-driven interface
- Displays:
  - Patient information
  - Drug selected
  - Recommended dose
  - Frequency
  - Educational notes
- Uses named constants instead of magic numbers
- Modular and well-documented code

---

## Drugs Supported

### Paracetamol
- Dose: **15 mg/kg per dose**
- Frequency: Every **4–6 hours**
- Maximum single dose: **1000 mg**
- Maximum daily dose: **4000 mg**

### Amoxicillin
- Dose: **25 mg/kg/day**
- Divided into **3 doses**
- Maximum single dose: **500 mg**

### ORS
- Simplified maintenance fluid calculation:
- **20 mL/kg/day**
- *(Educational approximation — future versions may implement the Holliday–Segar method.)*

---

## Example

```text
Welcome to Drug Dose Calculator

Enter patient name: Rahul
Enter patient age: 8
Enter patient weight: 20

Select a drug
1. Paracetamol
2. Amoxicillin
3. ORS

Choice: 1

===========================
PATIENT SUMMARY
===========================

Name: Rahul
Age: 8 years
Weight: 20 kg

Drug: Paracetamol
Dose: 300 mg
Frequency: every 4–6 hours

Notes:
Maximum 4000 mg total per day
```

---

## Project Structure

```text
Drug-Dose-Calculator/
│
├── main.py
├── README.md
└── LICENSE
```

---

## Skills Demonstrated

- Python functions
- Dictionaries
- Constants
- Conditional statements
- Loops
- Input validation
- Error handling
- Modular programming
- Clean code practices

---

## Future Improvements

- Implement Holliday–Segar maintenance fluid calculation
- Add more medications
- Use age-specific dosing where appropriate
- Save patient records to a file
- Add a graphical user interface (GUI)
- Store drug information in external configuration files
- Add automated unit tests

---

## Author

Developed as part of my software engineering learning journey and building projects for my software engineering portfolio.

---