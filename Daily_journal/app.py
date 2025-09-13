




from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, JournalEntry
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    search = request.args.get("search", "")
    if search:
        entries = JournalEntry.query.filter(
            (JournalEntry.title.like(f"%{search}%")) |
            (JournalEntry.content.like(f"%{search}%"))
        ).order_by(JournalEntry.date_created.desc()).all()
    else:
        entries = JournalEntry.query.order_by(JournalEntry.date_created.desc()).all()
    return render_template("index.html", entries=entries, search=search)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash("Title and Content cannot be empty!", "danger")
            return redirect(url_for('add_entry'))
        entry = JournalEntry(title=title, content=content)
        db.session.add(entry)
        db.session.commit()
        flash("Entry added successfully!", "success")
        return redirect(url_for('index'))
    return render_template("add_entry.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        db.session.commit()
        flash("Entry updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template("edit_entry.html", entry=entry)

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted successfully!", "info")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)








<input type="text" name="title" value="{{ entry.title }}" class="form-control" required>
<textarea name="content" class="form-control" rows="4" required>{{ entry.content }}</textarea>