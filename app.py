from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import psycopg2.extras
import random

app = Flask(__name__)

# PostgreSQL config
db_config = {
    'host': 'c7s7ncbk19n97r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
    'user': 'u7tqojjihbpn7s',
    'password': 'p1b1897f6356bab4e52b727ee100290a84e4bf71d02e064e90c2c705bfd26f4a5',
    'dbname': 'd8lp4hr6fmvb9m',
    'port': 5432
}

# Test connection
try:
    conn = psycopg2.connect(**db_config)
    print("✅ Connected to PostgreSQL database")
    conn.close()
except Exception as err:
    print(f"❌ Error: {err}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inquiry.html', methods=['GET', 'POST'])
def inquiry():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            query = """INSERT INTO users (first_name, last_name, phone_number, email, password, service) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (name, "", phone, email, "", message))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('index'))
        except Exception as err:
            print(f"Error: {err}")
            return jsonify({'status': 'error', 'message': 'Failed to sign up'}), 500

    return render_template('inquiry.html')


@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    phone = request.form.get('phoneNumber')
    email = request.form.get('email')
    service = request.form.get('service')
    requirement = request.form.get('requirement')

    print(f"""
    Inquiry Received:
    Name: {first_name} {last_name}
    Phone: {phone}
    Email: {email}
    Service: {service}
    Requirement: {requirement}
    """)

    return jsonify({
        "status": "success",
        "message": "Your inquiry has been submitted successfully!"
    })


@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    phone_number = request.form.get('phoneNumber')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')
    service = request.form.get('service')

    if password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Passwords do not match'}), 400

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = """INSERT INTO users (first_name, last_name, phone_number, email, password, service) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (first_name, last_name, phone_number, email, password, service))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Your account has been created. You will be redirected to the login page.'}), 200
    except Exception as err:
        print(f"Error: {err}")
        return jsonify({'status': 'error', 'message': 'Failed to create account'}), 500


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            query = """INSERT INTO contacts (name, email, phone, service, message) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (name, email, phone, service, message))
            conn.commit()

            cursor.close()
            conn.close()

            return render_template('thank_you.html', name=name)
        except Exception as err:
            print(f"Error: {err}")
            return jsonify({'status': 'error', 'message': 'Failed to send message'}), 500

    return render_template('contact.html')


# Shop & Mall Billing Software Page
@app.route("/shopmall_billing_software")
def shopmall_billing_software():
    return render_template("shopmall_billing_software.html")

@app.route("/transport_management")
def transport_management():
    return render_template("transport_management.html")

@app.route("/dlms")
def dlms():
    return render_template("dlms.html")
@app.route("/wms")
def wms():
    return render_template("wms.html")

if __name__ == '__main__':
    app.run(debug=True)
