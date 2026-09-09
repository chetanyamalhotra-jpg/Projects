# Health Learning Projects

Small Python command-line projects created for learning and portfolio use.
They are not production applications and must not be used to make clinical
decisions or to store real patient information.

## Projects

| Project | Purpose | Run |
| --- | --- | --- |
| [Drug Dose Calculator](Drug-Dose-Calculator/Readme.md) | Demonstrates validation and bounded arithmetic with fictional educational examples. | `python Drug-Dose-Calculator/maindrug.py` |
| [Patient Record Manager](Patient-Record-Manager/README.md) | Demonstrates a local SQLite CRUD CLI with validation. | `python Patient-Record-Manager/main.py` |
| [Smart BMI Calculator](smart-BMI-Calculator/Readme.md) | Demonstrates input validation and BMI category logic. | `python smart-BMI-Calculator/main.py` |

## Development

Use Python 3.11 or newer. Install development tools and run all checks from
the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m ruff check .
```

## Safety and privacy

- The healthcare-themed examples are educational only and are not clinically
  validated.
- Do not enter, commit, or share real patient data. The Patient Record Manager
  stores its local database outside this repository by default.
- Report security concerns privately as described in [SECURITY.md](SECURITY.md).

## License

This repository is licensed under the [MIT License](LICENSE).

