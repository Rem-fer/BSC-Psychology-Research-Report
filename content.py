

INTRO_TEXT = """This dashboard explores the relationship between trait mindfulness, inhibition, and phone checking frequency. The data includes:
- **MAAS Score**: A measure of trait mindfulness.
- **Inhibition Score**: A measure of inhibitory control based on a cognitive task.
- **Z-Pickups**: A z-scored measure of phone checking frequency."""

HYPOTHESES = {
            "H1": "Trait mindfulness scores (MAAS) will predict phone checking frequency.",
            "H2": "Inhibitory control (Go/No-Go correct responses) will predict phone checking frequency.",
            "H3": "Trait mindfulness scores (MAAS) will predict inhibitory control (Go/No-Go performance)."
            }

MULTIPLE_REGRESSION_TEXT = """
A multiple linear regression was conducted to examine the relationship between 
trait mindfulness (MAAS), inhibition (Go/No-Go performance), and phone checking 
frequency (Z-Pickups). The model1 included MAAS scores and inhibition scores as 
predictors of Z-Pickups.
"""

SIMPLE_REGRESSION_TEXT = """
A simple linear regression was conducted to examine the relationship between 
trait mindfulness (MAAS) and inhibition (Go/No-Go performance). MAAS scores 
were entered as a predictor of inhibition scores.
"""

