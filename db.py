import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


def connect_to_db():
    try:
        # MySQL bağlantısı oluştur
        connection = mysql.connector.connect(
            host='172.17.0.3',        # MySQL sunucu adresi
            user='root',    # MySQL kullanıcı adı
            password='1234',       # MySQL şifresi
            database='flask_db'  # Bağlanmak istediğin veritabanı
        )
        return connection
    except Error as e:
        print(f"Hata oluştu: {e}")


def get_user_info(username):

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    return result


def get_user_info_viaID(user_id):

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def is_valid_user(username):
    result = get_user_info(username)

    if result == None:
        print("geçersiz user")

    else:
        print("geçer")


def generate_hash(sifre):

    hash = generate_password_hash(sifre)
    return hash


def new_user_create(name, surname, username, email, password_hash):

    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name, surname,username, email, password_hash, role_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s)", (name, surname, username, email, password_hash, 2))

    connection.commit()
    cursor.close()
    connection.close()


def get_all_user_info():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT name, surname,username, email FROM users WHERE role_id=2 ")

    all_user_info = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_user_info


def login_user(username, password):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, password_hash, role_id  FROM users WHERE username=%s ", (username,))
    user = cursor.fetchone()
    if user is None:
        return (False, 0, 0)
    hash_db = user['password_hash']
    user_id = user['id']
    role = user['role_id']
    if check_password_hash(hash_db, password):
        return (True, role, user_id)
    else:
        return (False, 0, 0)


def new_admin_create(name, surname, username, email, password_hash):

    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name, surname,username, email, password_hash, role_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s)", (name, surname, username, email, password_hash, 1))

    connection.commit()
    cursor.close()
    connection.close()


def new_position_create(id, title, description, department, location, deadline):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO positions (admin_id, title,description, department, location, deadline) "
                   "VALUES (%s, %s, %s, %s, %s, %s)", (id, title, description, department, location, deadline))
    connection.commit()
    cursor.close()
    connection.close()


def get_all_position_info():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM positions")
    positions_info = cursor.fetchall()
    cursor.close()
    connection.close()
    return positions_info


def get_position_id(app_id):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT position_id FROM applications WHERE id = %s", (app_id,))
    position_id = cursor.fetchone()
    cursor.close()
    connection.close()
    return position_id


def get_position_info(position_id):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM positions WHERE id = %s ", (position_id,))
    positions_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return positions_info


def create_new_application(user_id, position_id, cv_name, cv_data, cover_letter):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO documents (title, cv_data)  "
                   "VALUES (%s, %s)", (cv_name, cv_data))

    document_id = cursor.lastrowid
    cursor.execute("INSERT INTO applications (user_id, position_id, document_id, cover_letter, status_id)"
                   "VALUES (%s, %s, %s, %s, %s)", (user_id, position_id, document_id, cover_letter, 1))
    connection.commit()
    cursor.close()
    connection.close()


# Bir kullanıcının bütün başvurularının bilgilerini çeker
def get_all_user_application_info(user_id):
    sql = """
        SELECT a.id, a.position_id, p.title, p.department,  p.location, p.is_active,
        p.created_at, s.status
        from applications a
        join positions p on a.position_id = p.id 
        join application_status s on a.status_id = s.id WHERE a.user_id = %s;
        """
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (user_id,))
    application_info = cursor.fetchall()
    cursor.close()
    connection.close()
    return application_info

# Bir pozisyona gelen bütün başvuranların başvuru bilgilerini bilgilerini çeker


def get_applications_for_position(position_id):
    sql = """
        SELECT app.id, p.is_active, app.status_id, u.name, u.surname, u.email, app.created_at, st.status, app.cover_letter
        FROM applications AS app
        JOIN users AS u ON app.user_id = u.id
        JOIN positions AS p ON app.position_id = p.id
        JOIN application_status AS st ON app.status_id = st.id
        WHERE app.position_id = %s;
        """

    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (position_id,))
    application_info = cursor.fetchall()
    cursor.close()
    connection.close()
    return application_info


def get_cvdata(application_id):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    sql = """
       SELECT u.name, u.surname, d.title, d.cv_data
        FROM applications AS app
        JOIN users AS u ON app.user_id = u.id
        JOIN documents AS d ON app.document_id = d.id
        WHERE app.id = %s;
        """
    cursor.execute(sql, (application_id,))
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data


def set_app_status(application_id, status_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = """
       UPDATE applications SET status_id = %s WHERE id = %s;
        """
    cursor.execute(sql, (status_id, application_id))
    connection.commit()
    cursor.close()
    connection.close()


def set_position_passive(position_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = """
       UPDATE positions SET is_active = FALSE WHERE id = %s;
        """
    cursor.execute(sql, (position_id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_cover_letter(app_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = """
       SELECT cover_letter from applications WHERE id = %s;
        """
    cursor.execute(sql, (app_id,))
    cover_letter = cursor.fetchone()
    cursor.close()
    connection.close()
    return cover_letter


print(type(get_cvdata(1)))
