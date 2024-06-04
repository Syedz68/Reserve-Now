from datetime import date

from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'asheq dbms'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reservedb'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/usersignup')
def userRegister():
    return render_template('user_signup.html')


@app.route('/restaurantsignup')
def restaurantRegister():
    return render_template('restaurant_signup.html')


# Admin Part Starts Here ------------------------------------------------------------------------------------------------------------------>
@app.route('/admin_dashboard')
def admin():
    if 'logged_in' in session and session['u_role'] == 'admin':
        return render_template('admin_dashboard.html', name=session['u_name'])
    return redirect(url_for('login'))


@app.route('/admin_custome')
def adminCust():
    if 'logged_in' in session and session['u_role'] == 'admin':
        role = 'customer'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE u_role = %s', (role,))
        data = cursor.fetchall()
        cursor.close()
        return render_template('admin_cutomer.html', name=session['u_name'], data=data)
    return redirect(url_for('login'))


@app.route('/admin_cust_delete/<string:id_data>', methods=['GET'])
def custDelete(id_data):
    if 'logged_in' in session and session['u_role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM users WHERE u_id = %s', (id_data,))
        mysql.connection.commit()
        flash("Customer has been deleted", "error")
        return redirect(url_for('adminCust'))
    return redirect(url_for('login'))


@app.route('/admin_cust_update/<string:id_data>', methods=['GET', 'POST'])
def custUpdate(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'admin':
        try:
            cursor = mysql.connection.cursor()
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            role = request.form['role']
            cursor.execute(
                'UPDATE users SET u_name = %s, u_email = %s, u_phone = %s, u_pass = %s, u_role = %s WHERE u_id = %s',
                (name, email, phone, password, role, id_data))
            mysql.connection.commit()  # Commit the changes to the database
            flash('Data updated successfully!!', 'success')
            return redirect(url_for('adminCust'))
        except Exception as e:
            # Log the error for debugging
            print("An error occurred:", e)
            flash('An error occurred while updating data!', 'error')
            return redirect(url_for('adminCust'))
    return redirect(url_for('login'))


@app.route('/admin_manage')
def adminManage():
    if 'logged_in' in session and session['u_role'] == 'admin':
        role = 'restaurant'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE u_role = %s', (role,))
        data = cursor.fetchall()
        cursor.close()
        return render_template('admin_manager.html', name=session['u_name'], data=data)
    return redirect(url_for('login'))


@app.route('/admin_manage_delete/<string:id_data>', methods=['GET'])
def managerDelete(id_data):
    if 'logged_in' in session and session['u_role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM users WHERE u_id = %s', (id_data,))
        mysql.connection.commit()
        flash("Manager has been deleted", "error")
        return redirect(url_for('adminManage'))
    return redirect(url_for('login'))


@app.route('/admin_manage_update/<string:id_data>', methods=['GET', 'POST'])
def managerUpdate(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'admin':
        try:
            cursor = mysql.connection.cursor()
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            role = request.form['role']
            cursor.execute(
                'UPDATE users SET u_name = %s, u_email = %s, u_phone = %s, u_pass = %s, u_role = %s WHERE u_id = %s',
                (name, email, phone, password, role, id_data))
            mysql.connection.commit()  # Commit the changes to the database
            flash('Data updated successfully!!', 'success')
            return redirect(url_for('adminManage'))
        except Exception as e:
            # Log the error for debugging
            print("An error occurred:", e)
            flash('An error occurred while updating data!', 'error')
            return redirect(url_for('adminManage'))
    return redirect(url_for('login'))


@app.route('/admin_rest')
def adminRest():
    if 'logged_in' in session and session['u_role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurants')
        data = cursor.fetchall()
        cursor.close()
        return render_template('admin_restaurants.html', name=session['u_name'], data=data)
    return redirect(url_for('login'))


@app.route('/admin_rest_delete/<string:id_data>', methods=['GET'])
def restaurantDelete(id_data):
    if 'logged_in' in session and session['u_role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM restaurants WHERE r_id = %s', (id_data,))
        mysql.connection.commit()
        flash("Restaurant has been deleted", "error")
        return redirect(url_for('adminRest'))
    return redirect(url_for('login'))


@app.route('/admin_rest_approve/<string:id_data>', methods=['GET'])
def restaurantApprove(id_data):
    if 'logged_in' in session and session['u_role'] == 'admin':
        status = 'approved'
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE restaurants SET r_status = %s WHERE r_id = %s', (status, id_data))
        mysql.connection.commit()
        flash("Restaurant approved", "success")
        return redirect(url_for('adminRest'))
    return redirect(url_for('login'))


@app.route('/admin_rest_update/<string:id_data>', methods=['GET', 'POST'])
def restaurantUpdate(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'admin':
        try:
            cursor = mysql.connection.cursor()
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            cuisine = request.form['cuisine']
            description = request.form['des']
            address = request.form['address']
            stat = request.form['stat']
            rat = request.form['rat']

            cursor.execute(
                'UPDATE restaurants SET r_name = %s, r_email = %s, r_phone = %s, cuisine = %s, description = %s, address = %s, r_status = %s, rating = %s WHERE r_id = %s',
                (name, email, phone, cuisine, description, address, stat,rat, id_data))
            mysql.connection.commit()  # Commit the changes to the database
            flash('Data updated successfully!!', 'success')
        except Exception as e:
            # Log the error
            print("An error occurred:", e)
            flash('An error occurred while updating data!', 'error')
        finally:
            # Close the cursor
            cursor.close()

        # Redirect based on the success of the update operation
        return redirect(url_for('adminRest'))
    return redirect(url_for('login'))


@app.route('/admin_assign')
def adminAssign():
    if 'logged_in' in session and session['u_role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT u_id, u_name FROM users WHERE u_role = %s', ('restaurant',))
        data1 = cursor.fetchall()
        cursor.execute('SELECT r_id, r_name FROM restaurants')
        data2 = cursor.fetchall()
        cursor.execute('''
            SELECT users.u_name, restaurants.r_name
            FROM users
            JOIN restaurant_managers ON users.u_id = restaurant_managers.u_id
            JOIN restaurants ON restaurant_managers.r_id = restaurants.r_id
        ''')
        assignment_data = cursor.fetchall()
        cursor.close()
        return render_template('admin_assign.html', data1=data1, data2=data2, assignments=assignment_data,
                               name=session['u_name'])
    return redirect(url_for('login'))


@app.route('/admin_assigment', methods=['GET', 'POST'])
def adminSetManager():
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'admin':
        user = request.form['name']
        restaurant = request.form['rest']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurant_managers WHERE u_id = %s AND r_id = %s', (user, restaurant))
        account = cursor.fetchone()
        if account:
            flash('Manager already assigned !', 'error')
        else:
            cursor.execute('INSERT INTO restaurant_managers (u_id, r_id) VALUES (%s, %s)',
                           (user, restaurant))
            mysql.connection.commit()
            cursor.execute('SELECT u_id, u_name FROM users WHERE u_role = %s', ('restaurant',))
            data1 = cursor.fetchall()
            cursor.execute('SELECT r_id, r_name FROM restaurants')
            data2 = cursor.fetchall()
            cursor.execute('''
                       SELECT users.u_name, restaurants.r_name
                       FROM users
                       JOIN restaurant_managers ON users.u_id = restaurant_managers.u_id
                       JOIN restaurants ON restaurant_managers.r_id = restaurants.r_id
                   ''')
            assignment_data = cursor.fetchall()
            cursor.close()
            return render_template('admin_assign.html', data1=data1, data2=data2, assignments=assignment_data,
                                   name=session['u_name'])
    return redirect('login')


# Admin Part Ends Here ------------------------------------------------------------------------------------------------------------------>
# Restaurant Manager Part Starts Here --------------------------------------------------------------------------------------------------->
@app.route('/rest')
def restDashboard():
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
        data2 = cursor.fetchone()
        cursor.execute('SELECT * FROM reservations WHERE r_id = %s', (data1['r_id'],))
        data = cursor.fetchall()
        return render_template('restaurant_dashboard.html', name=session['u_name'], data1=data1, data2=data2, data=data)


@app.route('/rest_confirm/<string:id_data>', methods=['GET'])
def seatConfirm(id_data):
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        status = 'Confirmed'
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE reservations SET status = %s WHERE reservation_id = %s', (status, id_data))
            mysql.connection.commit()
            flash("Restaurant approved", "success")
            return redirect(url_for('restDashboard'))
        except Exception as e:
            # Handle database exceptions here (e.g., log the error)
            flash(f"Reservation update failed: {str(e)}", "danger")
            return redirect(url_for('restDashboard'))
    return redirect(url_for('login'))


@app.route('/rest_served/<string:id_data>', methods=['GET'])
def seatServed(id_data):
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        status = 'Served'
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE reservations SET status = %s WHERE reservation_id = %s', (status, id_data))
            mysql.connection.commit()

            # Fetch table_id before update (or within a transaction)
            cursor.execute('SELECT table_id FROM reservations WHERE reservation_id = %s', (id_data,))
            data = cursor.fetchone()
            table_id = data['table_id']  # Extract table_id

            cursor.execute('UPDATE tables SET availability = %s WHERE table_id = %s', (1, table_id))
            mysql.connection.commit()
            flash("Customer Served", "success")
            return redirect(url_for('restDashboard'))
        except Exception as e:
            # Handle database exceptions here (e.g., log the error)
            flash(f"Customer update failed: {str(e)}", "danger")
            return redirect(url_for('restDashboard'))
    return redirect(url_for('login'))


@app.route('/rest_cancel/<string:id_data>', methods=['GET'])
def seatCanceled(id_data):
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        status = 'Canceled'
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE reservations SET status = %s WHERE reservation_id = %s', (status, id_data))
            mysql.connection.commit()

            # Fetch table_id before update (or within a transaction)
            cursor.execute('SELECT table_id FROM reservations WHERE reservation_id = %s', (id_data,))
            data = cursor.fetchone()
            table_id = data['table_id']  # Extract table_id

            cursor.execute('UPDATE tables SET availability = %s WHERE table_id = %s', (1, table_id))
            mysql.connection.commit()
            flash("Customer Canceled", "success")
            return redirect(url_for('restDashboard'))
        except Exception as e:
            # Handle database exceptions here (e.g., log the error)
            flash(f"Customer update failed: {str(e)}", "danger")
            return redirect(url_for('restDashboard'))
    return redirect(url_for('login'))


@app.route('/resttable')
def restTable():
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
        data2 = cursor.fetchone()
        cursor.execute('SELECT * FROM tables WHERE r_id = %s', (data1['r_id'],))
        table = cursor.fetchall()
        return render_template('rest_table.html', name=session['u_name'], data1=data1, data2=data2, table=table)
    return redirect('login')


@app.route('/resttableinsert', methods=['GET', 'POST'])
def insertTable():
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        table_num = request.form['table']
        capacity = request.form['cap']
        avail = request.form['availability']
        if avail == 'TRUE':
            avail = 1
        else:
            avail = 0
        cursor.execute('SELECT * FROM tables WHERE table_num = %s AND r_id = %s', (table_num, data1['r_id']))

        t = cursor.fetchone()
        if t:
            flash('Table already inserted!', 'error')
        else:
            cursor.execute('INSERT INTO tables (r_id, table_num, capacity, availability) VALUES (%s, %s, %s, %s)',
                           (data1['r_id'], table_num, capacity, avail))
            mysql.connection.commit()
            cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
            data2 = cursor.fetchone()
            cursor.execute('SELECT * FROM tables WHERE r_id = %s', (data1['r_id'],))
            table = cursor.fetchall()
            return render_template('rest_table.html', name=session['u_name'], data1=data1, data2=data2, table=table)
    return redirect('login')


@app.route('/rest_table_delete/<string:id_data>', methods=['GET'])
def deleteTable(id_data):
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tables WHERE table_id = %s', (id_data,))
        mysql.connection.commit()
        flash("Table has been deleted", "success")
        return redirect(url_for('restTable'))
    return redirect(url_for('login'))


@app.route('/rest_table_update/<string:id_data>', methods=['GET', 'POST'])
def tableUpdate(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'restaurant':
        try:
            cursor = mysql.connection.cursor()
            rest = request.form['rest1']
            table_num = request.form['table1']
            capacity = request.form['cap1']
            avail = request.form['availability1']
            if avail == 'TRUE':
                avail = 1
            else:
                avail = 0
            cursor.execute(
                'UPDATE tables SET r_id = %s, table_num = %s, capacity = %s, availability = %s WHERE table_id = %s',
                (rest, table_num, capacity, avail, id_data))
            mysql.connection.commit()  # Commit the changes to the database
            flash('Data updated successfully!!', 'success')
        except Exception as e:
            # Log the error
            print("An error occurred:", e)
            flash('An error occurred while updating data!', 'error')
        finally:
            # Close the cursor
            cursor.close()

        # Redirect based on the success of the update operation
        return redirect(url_for('restTable'))
    return redirect(url_for('login'))


@app.route('/restmenu')
def restMenu():
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
        data2 = cursor.fetchone()
        cursor.execute('SELECT * FROM menus WHERE r_id = %s', (data1['r_id'],))
        menu = cursor.fetchall()
        return render_template('rest_menu.html', name=session['u_name'], data1=data1, data2=data2, menu=menu)
    return redirect('login')


@app.route('/restmenuinsert', methods=['GET', 'POST'])
def insertMenu():
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        item = request.form['item']
        description = request.form['des']
        price = request.form['price']
        price = float(price)
        cursor.execute('SELECT * FROM menus WHERE item_name = %s AND r_id = %s', (item, data1['r_id']))
        food = cursor.fetchone()
        if food:
            flash('Item already inserted!', 'error')
        else:
            cursor.execute('INSERT INTO menus (r_id, item_name, description, price) VALUES (%s, %s, %s, %s)',
                           (data1['r_id'], item, description, price))
            mysql.connection.commit()
            cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
            data2 = cursor.fetchone()
            cursor.execute('SELECT * FROM menus WHERE r_id = %s', (data1['r_id'],))
            menu = cursor.fetchall()
            return render_template('rest_menu.html', name=session['u_name'], data1=data1, data2=data2, menu=menu)
    return redirect('login')


@app.route('/rest_menu_delete/<string:id_data>', methods=['GET'])
def deleteMenu(id_data):
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM menus WHERE menu_id = %s', (id_data,))
        mysql.connection.commit()
        flash("Item has been deleted", "success")
        return redirect(url_for('restMenu'))
    return redirect(url_for('login'))


@app.route('/rest_menu_update/<string:id_data>', methods=['GET', 'POST'])
def menuUpdate(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'restaurant':
        try:
            cursor = mysql.connection.cursor()
            rest = request.form['rest1']
            item = request.form['item1']
            description = request.form['des1']
            price = request.form['price1']
            cursor.execute(
                'UPDATE menus SET r_id = %s, item_name = %s, description = %s, price = %s WHERE menu_id = %s',
                (rest, item, description, price, id_data))
            mysql.connection.commit()  # Commit the changes to the database
            flash('Data updated successfully!!', 'success')
        except Exception as e:
            # Log the error
            print("An error occurred:", e)
            flash('An error occurred while updating data!', 'error')
        finally:
            # Close the cursor
            cursor.close()

        # Redirect based on the success of the update operation
        return redirect(url_for('restMenu'))
    return redirect(url_for('login'))


@app.route('/restreview')
def restReview():
    if 'logged_in' in session and session['u_role'] == 'restaurant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
        data1 = cursor.fetchone()
        cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
        data2 = cursor.fetchone()
        cursor.execute('''
                    SELECT users.u_id, users.u_name, reviews.rating, reviews.comment, reviews.review_date FROM
                    users JOIN reviews ON users.u_id = reviews.u_id WHERE reviews.r_id = %s''', (data1['r_id'],))
        data = cursor.fetchall()
        cursor.execute('SELECT rating FROM reviews WHERE r_id = %s', (data1['r_id'],))
        r = cursor.fetchall()
        if r:
            total_rating = sum(rating['rating'] for rating in r)
            avg = total_rating / len(r)
        else:
            avg = None
        return render_template('rest_review.html', name=session['u_name'], data=data, data2= data2, rating=avg)
    return redirect(url_for('login'))


# Restaurant Managare Part Ends Here ---------------------------------------------------------------------------------------------------->

# Customer Part Starts Here ------------------------------------------------------------------------------------------------------------->
@app.route('/cust')
def custDashboard():
    if 'logged_in' in session and session['u_role'] == 'customer':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurants WHERE r_status = %s', ('approved',))
        data = cursor.fetchall()
        return render_template('customer_dashboard.html', name=session['u_name'], data=data)
    return redirect(url_for('login'))


@app.route('/custrest/<string:id_data>')
def custRestaurant(id_data):
    if 'logged_in' in session and session['u_role'] == 'customer':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM menus WHERE r_id = %s', (id_data,))
        data1 = cursor.fetchall()
        cursor.execute('SELECT * FROM tables WHERE r_id = %s AND availability = %s', (id_data, 1))
        data2 = cursor.fetchall()
        cursor.execute('SELECT r_id, r_name FROM restaurants WHERE r_id = %s', (id_data,))
        rest_name = cursor.fetchone()
        return render_template('cust_rest.html', name=session['u_name'], data1=data1, data2=data2, rest=rest_name,
                               user_id=session['u_id'])
    return redirect(url_for('login'))


@app.route('/custreview/<string:id_data>', methods=['GET', 'POST'])
def custReview(id_data):
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'customer':
        user = request.form['user']
        rest = request.form['resta']
        rating = request.form['rate']
        comment = request.form['cmt']
        today = date.today()
        formatted_date = today.strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO reviews (u_id, r_id, rating, comment, review_date) VALUES (%s, %s, %s, %s, %s)',
            (user, rest, rating, comment, formatted_date))
        mysql.connection.commit()
        cursor.execute('SELECT rating FROM reviews WHERE r_id = %s', (rest,))
        r = cursor.fetchall()
        if r:
            total_rating = sum(rating['rating'] for rating in r)
            avg = total_rating / len(r)
        else:
            avg = None
        cursor.execute('UPDATE restaurants SET rating = %s WHERE r_id = %s', (avg, rest))
        mysql.connection.commit()
        return redirect(url_for('custRestaurant', id_data=id_data))
    return redirect(url_for('login'))


@app.route('/custbook/<string:id_data1>/<string:id_data2>', methods=['GET', 'POST'])
def custBook(id_data1, id_data2):
    st = 'Pending'
    if request.method == 'POST' and 'logged_in' in session and session['u_role'] == 'customer':
        user = request.form['user1']
        date = request.form['date_input']
        reserve_time = request.form['time_input']
        size = request.form['size']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO reservations (u_id, r_id, table_id, reservation_date, reservation_time, party_size, status) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (user, id_data1, id_data2, date, reserve_time, size, st))
            mysql.connection.commit()

            cursor.execute('UPDATE tables SET availability = %s WHERE table_id = %s', (0, id_data2))
            mysql.connection.commit()
            flash("Reservation Successful!", "success")  # Add flash message
            return redirect(url_for('custReserve'))
        except Exception as e:
            # Handle database exceptions here (e.g., log the error)
            flash(f"Reservation failed: {str(e)}", "danger")  # Flash error message
            return redirect(
                url_for('custBook', id_data1=id_data1, id_data2=id_data2))  # Redirect with original data for re-attempt
    return redirect(url_for('login'))


@app.route('/custreserve')
def custReserve():
    if 'logged_in' in session and session['u_role'] == 'customer':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
                    SELECT users.u_name, restaurants.r_name, tables.table_num, reservations.reservation_date, reservations.reservation_time, reservations.status
                    FROM users JOIN reservations ON users.u_id = reservations.u_id
                    JOIN tables ON reservations.table_id = tables.table_id 
                    JOIN restaurants ON tables.r_id = restaurants.r_id 
                    WHERE users.u_id = %s
                    ORDER BY 
                        CASE 
                            WHEN reservations.status = 'Pending' THEN 1 
                            ELSE 2 
                        END, 
                        reservations.reservation_date DESC, 
                        reservations.reservation_time DESC
                    ''', (session['u_id'],))
        data = cursor.fetchall()
        return render_template('cust_reserve.html', name=session['u_name'], data=data)
    return redirect(url_for('login'))


# Customer Part Ends Here --------------------------------------------------------------------------------------------------------------->
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE u_email = %s AND u_pass = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['u_id'] = user['u_id']
            session['u_name'] = user['u_name']
            session['u_email'] = user['u_email']
            session['u_phone'] = user['u_phone']
            session['u_role'] = user['u_role']
            flash('Logged in successfully!!', 'success')
            if session['u_role'] == 'admin':
                return render_template('admin_dashboard.html', name=session['u_name'])
            elif session['u_role'] == 'customer':
                cursor.execute('SELECT * FROM restaurants')
                data = cursor.fetchall()
                return render_template('customer_dashboard.html', name=session['u_name'], data=data)
            elif session['u_role'] == 'restaurant':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT r_id FROM restaurant_managers WHERE u_id = %s', (session['u_id'],))
                data1 = cursor.fetchone()
                cursor.execute('SELECT r_name FROM restaurants WHERE r_id = %s', (data1['r_id'],))
                data2 = cursor.fetchone()
                cursor.execute('SELECT * FROM reservations WHERE r_id = %s', (data1['r_id'],))
                data = cursor.fetchall()
                return render_template('restaurant_dashboard.html', name=session['u_name'], data1=data1, data2=data2,
                                       data=data)
        else:
            flash('Please enter correct email or password', 'error')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('u_id', None)
    session.pop('u_name', None)
    session.pop('u_email', None)
    session.pop('u_phone', None)
    session.pop('u_role', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def userSignup():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE u_email = %s AND u_pass = %s', (email, password))
        account = cursor.fetchone()
        if account:
            flash('Account already exists !', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address', 'error')
        else:
            cursor.execute('INSERT INTO users (u_name, u_email, u_phone, u_pass, u_role) VALUES (%s, %s, %s, %s, %s)',
                           (name, email, phone, password, role))
            mysql.connection.commit()
            session['logged_in'] = True
            session['u_name'] = name
            session['u_email'] = email
            session['u_phone'] = phone
            session['u_role'] = role
            flash('You have successfully signed up', 'success')
            if role == 'customer':
                return render_template('customer_dashboard.html', name=session['u_name'])
            elif role == 'restaurant':
                return render_template('restaurant_dashboard.html', name=session['u_name'])
    return redirect(url_for('userRegister'))


@app.route('/registerrestaurant', methods=['GET', 'POST'])
def restaurantSignup():
    if request.method == 'POST' and 'email' in request.form:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cuisine = request.form['cuisine']
        description = request.form['des']
        address = request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurants WHERE r_name = %s AND r_email = %s', (name, email))
        account = cursor.fetchone()
        if account:
            flash('Restaurant already exists !', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address', 'error')
        else:
            cursor.execute(
                'INSERT INTO restaurants (r_name, r_email, r_phone, cuisine, description, address, r_status) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (name, email, phone, cuisine, description, address, 'pending'))
            mysql.connection.commit()
            flash('Your request is on pending', 'success')
            return render_template('index.html')

    return redirect(url_for('restaurantRegister'))


if __name__ == '__main__':
    app.run(debug=True)
