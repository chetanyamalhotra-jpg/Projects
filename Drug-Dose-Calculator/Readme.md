# Educational Drug Dose Calculator

An educational Python exercise that demonstrates input validation and bounded
arithmetic. It is **not** clinically validated and must not be used for real
prescribing, administration, or treatment decisions.

## What it demonstrates

- Finite, positive numeric input validation
- A menu-driven command-line interface
- Named constants and bounded calculations
- Explicit separation between an educational amount and a clinical schedule

The application intentionally does not produce a clinical administration
schedule. Age is collected for display only because this simplified exercise
does not implement age-specific rules.

## Run

```bash
python maindrug.py
```

## Test

From the repository root:

```bash
python -m pytest Drug-Dose-Calculator
```

## Safety

The formulas are fixed classroom examples, not medical guidance. Consult a
qualified healthcare professional and current clinical guidance for any real
decision.

