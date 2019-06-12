from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    """ Upload form to specify import file """

    upload_file = FileField("Data File", validators=[DataRequired()])
