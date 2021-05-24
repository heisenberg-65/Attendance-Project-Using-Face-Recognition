from database import Database

student_database = Database()
print("Choose your action\n")
c = input("Press\n1. For inserting a Student\n2. For checking attendance\nEnter option : ")
if c == '2':
    start_date = input("Enter Start Date (YYYY-MM-DD) : ")
    end_date = input("Enter End Date (YYYY-MM-DD) : ")

    choice = input("1. For one student\n2. For all students\nEnter option : ")

    if choice == '1':
        scholar = int(input("Enter Scholar ID : "))
        record = student_database.get_record(start_date, end_date, 0,scholar)
    else:
        record = student_database.get_record(start_date, end_date,1,int(0))
elif c == '1' :
    new_name = input("Enter the name of new student : ")
    student_database.insert_stu(new_name)
else :
    print("Invalid Choice")