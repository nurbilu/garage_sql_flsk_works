from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def create_connection():
    return sqlite3.connect("cars.db")

# Function to create the cars table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            color TEXT NOT NULL,
            owner TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
# Initialize the database and table
create_table()


@app.route('/')
def home():
    return render_template("home.html")

#add new car to db
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        owner = request.form['owner']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cars (model, year, color, owner) VALUES (?, ?, ?, ?)", (model, year, color, owner))
        conn.commit()
        conn.close()
        return redirect(url_for('display_cars'))
    return render_template("add.html")

# display all cars in db
@app.route('/display_cars', methods=['GET'])
def display_cars():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return render_template("cars.html", cars=cars)

@app.route('/delete/<int:car_id>', methods=['GET'])
def delete(car_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('display_cars'))


# update a chosen <int:car_id> and alter one or more of the value in colums 
@app.route('/upd/', methods=["GET", "POST"])
@app.route('/upd/<int:car_id>', methods=["GET", "POST"])
def upd(car_id=None):
    conn = create_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        owner = request.form['owner']

        if car_id is not None:
            # Update the record in the database for the specified car ID
            cursor.execute("UPDATE cars SET model=?, year=?, color=?, owner=? WHERE id=?", (model, year, color, owner, car_id))
        else:
            # Insert a new record in the database if no car ID is provided
            cursor.execute("INSERT INTO cars (model, year, color, owner) VALUES (?, ?, ?, ?)", (model, year, color, owner))

        conn.commit()
        conn.close()

        return redirect(url_for('display_cars'))

    else:
        if car_id is not None:
            # Fetch the car information to pre-fill the form for the specified car ID
            cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
            car = cursor.fetchone()
            conn.close()

            if car:
                return render_template("upd.html", car=car)
            else:
                return "Car not found"
        else:
            # Render the update form without pre-filled information for a new car
            conn.close()
            return render_template("upd.html", car=None)

if __name__ == "__main__":
    app.run(debug=True)