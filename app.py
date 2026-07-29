from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, create_table

app = Flask(__name__)
app.secret_key = "employee_secret_key"

create_table()


@app.route("/")
def index():

    conn = get_connection()
    employees = conn.execute(
        "SELECT * FROM employees ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO employees(name,email,department,salary)
            VALUES(?,?,?,?)
            """,
            (name, email, department, salary),
        )

        conn.commit()
        conn.close()

        flash("Employee Added Successfully!")

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id=?",
        (id,),
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn.execute(
            """
            UPDATE employees
            SET name=?, email=?, department=?, salary=?
            WHERE id=?
            """,
            (name, email, department, salary, id),
        )

        conn.commit()
        conn.close()

        flash("Employee Updated Successfully!")

        return redirect(url_for("index"))

    conn.close()

    return render_template("edit.html", employee=employee)


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM employees WHERE id=?",
        (id,),
    )

    conn.commit()
    conn.close()

    flash("Employee Deleted Successfully!")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
