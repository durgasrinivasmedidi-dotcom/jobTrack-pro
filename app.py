from flask import Flask, render_template, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# Home page + Search + Filter + Dashboard Statistics
@app.route("/")
def home():

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Search and filter
    query = """
        SELECT * FROM jobs
        WHERE (company LIKE %s OR role LIKE %s)
    """

    search_value = "%" + search + "%"

    parameters = [search_value, search_value]

    if status:
        query += " AND status = %s"
        parameters.append(status)

    query += " ORDER BY application_date DESC"

    cursor.execute(query, parameters)

    jobs = cursor.fetchall()

    # Dashboard statistics
    cursor.execute("SELECT COUNT(*) AS total FROM jobs")
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS count FROM jobs WHERE status = 'Interview'"
    )
    interviews = cursor.fetchone()["count"]

    cursor.execute(
        "SELECT COUNT(*) AS count FROM jobs WHERE status = 'Selected'"
    )
    selected = cursor.fetchone()["count"]

    cursor.execute(
        "SELECT COUNT(*) AS count FROM jobs WHERE status = 'Rejected'"
    )
    rejected = cursor.fetchone()["count"]

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        jobs=jobs,
        search=search,
        status=status,
        total=total,
        interviews=interviews,
        selected=selected,
        rejected=rejected
    )


# Add Job
@app.route("/add", methods=["GET", "POST"])
def add_job():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        application_date = request.form["application_date"]
        status = request.form["status"]

        db = get_db_connection()
        cursor = db.cursor()

        query = """
        INSERT INTO jobs
        (company, role, application_date, status)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            company,
            role,
            application_date,
            status
        )

        cursor.execute(query, values)
        db.commit()

        cursor.close()
        db.close()

        return redirect("/")

    return render_template("add_job.html")


# Edit Job
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_job(id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        application_date = request.form["application_date"]
        status = request.form["status"]

        query = """
        UPDATE jobs
        SET company = %s,
            role = %s,
            application_date = %s,
            status = %s
        WHERE id = %s
        """

        values = (
            company,
            role,
            application_date,
            status,
            id
        )

        cursor.execute(query, values)
        db.commit()

        cursor.close()
        db.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM jobs WHERE id = %s",
        (id,)
    )

    job = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "edit_job.html",
        job=job
    )


# Delete Job
@app.route("/delete/<int:id>")
def delete_job(id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)   



