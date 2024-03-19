import psycopg


print("---Begin Testing---\n\n\n\n\n") ## just to make it easier to read in console

host_ip = 'localhost' #self (localhost) - ip adress used for getting db info 
db_port = 5432 #DB port

database = 'pythonTest' ## the name of the database (not your username to access it!)
db_username = 'postgres'
db_password = 'student2024'

try:
    conn = psycopg.connect(
            f"dbname={database} user={db_username} password={db_password} host={host_ip} port={db_port}")
except psycopg.OperationalError as e:
    print(f"Error: {e}")
    exit(1)

##Initialize and execute instructions
def init():
    initData() ##<-- Delete this if you want to use pre-existing table
    getAllStudents()
    #Testing functions
    print('-------------')
    addStudent("Jornio", "Joseph", "jornio.joseph@example.com", "2023-10-03")
    getAllStudents()
    print('-------------')
    updateStudentEmail(4, "JoJo@gmail.com")
    getAllStudents()
    print('-------------')
    deleteStudent(4)
    getAllStudents()

##Initialize the table and the data inside it
##(used more as a convinience, to not need to setup the table and data inside of postgreSQL)
def initData():
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS students")
        temp_table = """ CREATE TABLE IF NOT EXISTS students(
                        student_id SERIAL,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        enrollment_date DATE,
                        PRIMARY KEY (student_id)
                    );
        """
        cursor.execute(temp_table)

        #practice using a list to insert
        temp_insert = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s,%s,%s,%s)"
        temp_insert_vals = [('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
                            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
                            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
                            ]
        for val in temp_insert_vals:
            conn.execute(temp_insert, val)

##Displays all table info
def getAllStudents():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

##Add a student into the students table
def addStudent(first_name, last_name, email, enrollment_date):
    with conn.cursor() as cursor:
        insert_str = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s,%s,%s,%s);"
        insert_vals = (first_name, last_name, email, enrollment_date)
        
        conn.execute(insert_str, insert_vals)

##Update a students email using the id, in the students table
def updateStudentEmail(student_id, new_email):
    with conn.cursor() as cursor:
        update_str = """UPDATE students
                        SET email = %s
                        WHERE student_id = %s;
        """
        update_vals = (new_email, student_id)
        conn.execute(update_str, update_vals)

##Delete a student using the id, from the students table
def deleteStudent(student_id):
    with conn.cursor() as cursor:
        delete_str = f"DELETE FROM students WHERE student_id = {student_id};"
        conn.execute(delete_str)

##Start program execution
init()

conn.commit() ## YOU NEED TO COMMIT.
conn.close() ## since I am not using a with block, I must close it myself (I think)