from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .mongo_models import BookEntry
import json
import datetime
from .webscraper import get_cover, sort_entries, format

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        title = request.form.get("title")
        line_entries = request.form.get("lineEntries")
        if line_entries:
            entries = line_entries.split("\r\n")
            print(entries)
            total = len(entries)
            for i, entry in enumerate(entries):
                split_entry = entry.split()
                # If there is an extra line that doesn't seem to be long enough, ignore it
                if len(split_entry) < 4:
                    continue

                print(split_entry)
                try:
                    rating = int(int(split_entry[0]))
                except RuntimeError:
                    rating = 0

                review = ""
                genre = ""

                if entry.count("(") == 1:
                    title = entry[entry.find(" ") + 1: entry.find("by") - 1]
                    series = ""
                    num_in_series = 1

                else:
                    title = entry[entry.find(" ") + 1: entry.rfind("(", 0, entry.rfind("(")) - 1]
                    series = entry[entry.rfind("(", 0, entry.rfind("(")) + 1: entry.find("#", entry.rfind("(", 0, entry.rfind("(")))]
                    try:
                        num_in_series = float(entry[entry.find("#", entry.find(series)) + 1: entry.find(")", entry.find(series))])
                    except RuntimeError:
                        num_in_series = 1

                author = entry[entry.rfind("by") + 3 : entry.find("(", entry.rfind("by")) - 1]

                raw_date = entry[entry.find("(", entry.find(author)) + 1 : entry.find(")", entry.find(author))]
                year, month, day = "-1","-1","-1"
                try:
                    month, day, year = raw_date.split("/")
                except ValueError:
                    print(raw_date)

                try:
                    date = datetime.date(2000 + int(year), int(month), int(day))
                except ValueError:
                    date = datetime.date.today()

                new_entry = BookEntry(title=title,
                                      author=author,
                                      is_series=bool(series),
                                      series=series,
                                      num_in_series=num_in_series,
                                      date=date,
                                      rating=rating,
                                      review=review,
                                      cover=get_cover(title, author),
                                      genre=genre,
                                      is_reread=False,
                                      user_id=current_user.id)
                new_entry.save()
                append_entry(new_entry)
                # new_entry.cover = str(new_entry.id) + ".jpg"
                print(f"{i+1}/{total} books added")

            flash("Book has been successfully added to the log", category="success")
            return redirect(url_for("views.home"))

        elif title:

            author = request.form.get("author")
            series = request.form.get("series")
            rating = request.form.get("rating")
            review = request.form.get("review")
            month = request.form.get("month")
            day = request.form.get("day")
            year = request.form.get("year")
            genre = request.form.get("genre")
            # print(month, day, year)
            try:
                num_in_series = float(request.form.get("seriesNumber"))
            except ValueError:
                num_in_series = 1

            try:
                rating = int(rating)
                if rating not in range(101):
                    rating = 0
            except ValueError:
                rating = 0

            # print(rating)

            try:
                date = datetime.date(int(year), int(month), int(day))
            except ValueError:
                date = datetime.date.today()

            new_entry = BookEntry(title=title,
                                  author=author,
                                  is_series=bool(series),
                                  series=series,
                                  num_in_series=num_in_series,
                                  date=date,
                                  rating=rating,
                                  review=review,
                                  cover=get_cover(title, author),
                                  genre=genre,
                                  is_reread=False,
                                  user_id=current_user.id)
            new_entry.save()
            append_entry(new_entry)

            flash("Book has been successfully added to the log", category="success")
            return redirect(url_for("views.home"))

        else:
            title = request.form.get("editTitle")
            author = request.form.get("editAuthor")
            series = request.form.get("editSeries")
            rating = request.form.get("editRating")
            review = request.form.get("editReview")
            month = request.form.get("editMonth")
            day = request.form.get("editDay")
            year = request.form.get("editYear")
            entry_id = request.form.get("entryId")
            genre = request.form.get("editGenre")
            # print(month, day, year)

            try:
                num_in_series = float(request.form.get("editSeriesNumber"))
            except ValueError:
                num_in_series = 1

            try:
                rating = int(rating)
                if rating not in range(101):
                    rating = 0
            except ValueError:
                rating = 0

            # print(rating)

            try:
                date = datetime.date(int(year), int(month), int(day))
            except ValueError:
                date = datetime.date.today()

            entry = BookEntry.objects(id=entry_id).first()
            if entry:
                if entry.user_id == current_user.id:
                    entry.title = title
                    entry.author = author
                    entry.series = series
                    entry.rating = rating
                    entry.review = review
                    entry.date = date
                    entry.genre = genre
                    entry.num_in_series = num_in_series
                    entry.is_series = bool(series)
                    # print(entry.is_series)
                    entry.save()
                    print("Database updated")
            return redirect(url_for("views.home"))
    for entry in current_user.entries:
        if len(BookEntry.objects(title = entry.title)) == 2:
            current_user.entries.remove(entry)
            entry.delete()
            current_user.save()
    current_user.entries = sorted(current_user.entries, key=sort_entries, reverse=True)
    # print(len(current_user.entries))
    return render_template("home.html", user=current_user, str=str, rstrip="".rstrip, format=format)


def append_entry(entry):
    current_user.entries.append(entry)
    current_user.save()


@views.route("/delete-entry", methods=["POST"])
def delete_entry():
    # print("deleting")
    data = json.loads(request.data)
    entry_id = data["entryId"]
    entry = BookEntry.objects(id=entry_id).first()
    if entry:
        if entry.user_id == current_user.id:
            current_user.entries.remove(entry)
            entry.delete()
            current_user.save()
            flash("Successfully deleted the book entry: " + entry.title + " by " + entry.author)
            return jsonify({})
