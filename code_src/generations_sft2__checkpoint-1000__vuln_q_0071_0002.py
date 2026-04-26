from flask import Flask, request, render_template_string, escape
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
import bleach

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure random key

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

def sanitize_comment(comment):
    # Use bleach to sanitize user input
    return bleach.clean(comment, tags=[], strip=True)

@app.route('/', methods=['GET', 'POST'])
def comment_section():
    form = CommentForm()
    comments = []
    
    if form.validate_on_submit():
        sanitized_comment = sanitize_comment(form.comment.data)
        comments.append(sanitized_comment)
        form.comment.data = ''  # Clear the form
        
    # Use a secure template with proper escaping
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comment Section</title>
    </head>
    <body>
        <h1>Leave a Comment</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <p>
                {{ form.comment.label }}<br>
                {{ form.comment(size=50) }}<br>
                {% for error in form.comment.errors %}
                    <span style="color: red;">[{{ error }}]</span>
                {% endfor %}
            </p>
            <p>
                {{ form.submit() }}
            </p>
        </form>
        <h2>Comments:</h2>
        {% for comment in comments %}
            <p>{{ comment }}</p>
        {% endfor %}
    </body>
    </html>
    '''
    
    return render_template_string(template, form=form, comments=comments)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production