from flask import Flask, render_template, request, redirect, url_for
import json, csv, os, datetime

app = Flask(__name__)

@app.route('/')
def home():
    csv_file_path = 'books.csv'
    try:
        all_books = csv.reader(open('books.csv', 'r'), delimiter=',')
    except FileNotFoundError:
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Date Added","Name", "Author", "Rating"])
                writer.writeheader()
    list_of_books = []
    for row in all_books:
        try:
            list_of_books.append(row)
        except:
            pass
    return render_template("index.html", books=list_of_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('book')
        email = request.form.get('author')
        rating = request.form.get('rating')
        new_book = {
            "Date Added": datetime.datetime.now().date(),
            "Name": name,
            "Author": email,
            "Rating": rating
        }
        csv_file_path = 'books.csv'

        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["Date Added","Name", "Author", "Rating"])
                writer.writeheader()

        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Date Added","Name", "Author", "Rating"])
            writer.writerow(new_book)

        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():

    csv_file_path = 'books.csv'
    header_row = []

    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        header_row = next(reader)

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_row) 

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

