from pathlib import Path

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

path = Path(".")
municipalities = sorted(path.glob("data/reviews_*.json"))

choices = [
    (p.stem.lstrip("reviews_"), p.stem.lstrip("reviews_").replace("-", " "))
    for p in municipalities
]


class MunicipalitySelectForm(FlaskForm):
    municipality = SelectField(
        f"Municipality",
        choices=choices,
        validators=[DataRequired()],
        coerce=lambda s: s if s else None,
    )

    submit = SubmitField("Show visualizations")
