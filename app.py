from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lunch.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class LunchSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lunch_time = db.Column(db.String(5), nullable=False)
    lunch_date = db.Column(db.Date, nullable=False, default=date.today)

    __table_args__ = (
        UniqueConstraint("name", "lunch_date", name="uq_name_date"),
    )

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        lunch_time = request.form.get("lunch_time", "").strip()

        if not name:
            flash("Please enter your name.", "error")
            return redirect(url_for("index"))

        if lunch_time not in {"12:00", "12:30", "13:00", "13:30", "14:00"}:
            flash("Please select a valid lunch time.", "error")
            return redirect(url_for("index"))

        today = date.today()
        selection = LunchSelection.query.filter_by(
            name=name, lunch_date=today
        ).first()

        if selection:
            selection.lunch_time = lunch_time
        else:
            db.session.add(
                LunchSelection(
                    name=name,
                    lunch_time=lunch_time,
                    lunch_date=today,
                )
            )

        db.session.commit()
        flash(f"Lunch selected for {lunch_time}.", "success")
        return redirect(url_for("index"))

    today = date.today()
    selections = (
        LunchSelection.query
        .filter_by(lunch_date=today)
        .order_by(LunchSelection.lunch_time, LunchSelection.name)
        .all()
    )

    counts = {}
    for selection in selections:
        counts[selection.lunch_time] = counts.get(selection.lunch_time, 0) + 1

    return render_template(
        "index.html",
        selections=selections,
        counts=counts,
        today=today,
    )

@app.post("/clear")
def clear_selection():
    name = request.form.get("name", "").strip()
    if name:
        selection = LunchSelection.query.filter_by(
            name=name, lunch_date=date.today()
        ).first()
        if selection:
            db.session.delete(selection)
            db.session.commit()
            flash("Your lunch selection was cleared.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
