from flask import Flask, flash, redirect, render_template, request, url_for
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "contact_management"),
}

CATEGORIES = ["Family", "Friend", "College", "Work", "Other"]


def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def get_contact(contact_id):
    """Fetch one contact by ID."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
        return cursor.fetchone()
    except Error as error:
        flash(f"Database error: {error}", "danger")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


@app.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    connection = None
    cursor = None
    contacts = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if search_query:
            like_query = f"%{search_query}%"
            sql = """
                SELECT * FROM contacts
                WHERE name LIKE %s
                   OR phone LIKE %s
                   OR email LIKE %s
                   OR category LIKE %s
                ORDER BY id DESC
            """
            cursor.execute(sql, (like_query, like_query, like_query, like_query))
        else:
            cursor.execute("SELECT * FROM contacts ORDER BY id DESC")

        contacts = cursor.fetchall()
    except Error as error:
        flash(f"Could not load contacts: {error}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return render_template("index.html", contacts=contacts, search_query=search_query)


@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        category = request.form.get("category", "Other").strip()

        if not name or not phone:
            flash("Name and phone number are required.", "warning")
            return render_template("add_contact.html", categories=CATEGORIES)

        if category not in CATEGORIES:
            category = "Other"

        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
                INSERT INTO contacts (name, phone, email, address, category)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, phone, email, address, category))
            connection.commit()
            flash("Contact added successfully.", "success")
            return redirect(url_for("index"))
        except Error as error:
            if connection:
                connection.rollback()
            flash(f"Could not add contact: {error}", "danger")
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template("add_contact.html", categories=CATEGORIES)


@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    contact = get_contact(contact_id)

    if not contact:
        flash("Contact not found.", "warning")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        category = request.form.get("category", "Other").strip()

        if not name or not phone:
            flash("Name and phone number are required.", "warning")
            contact.update({
                "name": name,
                "phone": phone,
                "email": email,
                "address": address,
                "category": category,
            })
            return render_template("edit_contact.html", contact=contact, categories=CATEGORIES)

        if category not in CATEGORIES:
            category = "Other"

        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = """
                UPDATE contacts
                SET name = %s,
                    phone = %s,
                    email = %s,
                    address = %s,
                    category = %s
                WHERE id = %s
            """
            cursor.execute(sql, (name, phone, email, address, category, contact_id))
            connection.commit()
            flash("Contact updated successfully.", "success")
            return redirect(url_for("index"))
        except Error as error:
            if connection:
                connection.rollback()
            flash(f"Could not update contact: {error}", "danger")
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    return render_template("edit_contact.html", contact=contact, categories=CATEGORIES)


@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        connection.commit()

        if cursor.rowcount == 0:
            flash("Contact not found.", "warning")
        else:
            flash("Contact deleted successfully.", "success")
    except Error as error:
        if connection:
            connection.rollback()
        flash(f"Could not delete contact: {error}", "danger")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
