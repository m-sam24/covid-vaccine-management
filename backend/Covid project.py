#TODO: dose name is not yet stored in register_vaccine
import mysql.connector
from db import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
db=mysql.connector.connect(host=DB_HOST,port=DB_PORT,user=DB_USER,passwd=DB_PASSWORD)
cursor=db.cursor()
cursor.execute("create database if not exists vaccine_management")
cursor.execute("use vaccine_management")
cursor.execute("""Create table if not exists dose_details(did int,hid int,dose_name varchar(15),price int,dose_date date,
                slot1 int,slot2 int,slot3 int,slot4 int,
                slot1_used int default 1,slot2_used int default 0,slot3_used int default 0,slot4_used int default 0)""")
cursor.execute("""create table if not exists register_vaccine(regid int,adharno int,
                    DOA1 date,DOA2 date default null,ndose int default 0,h_id1 int,amt1 int,h_id2 int,amt2 int default 0
                    ,marker1 varchar(2) default 'n',marker2 varchar(2) default 'n')""")
cursor.execute("""create table if not exists user_register(adharno int,
                    name varchar(25),age int,phone varchar(11))""")
cursor.execute("""create table if not exists hospital(h_id int,hospital_name varchar(30),
                    address varchar(50),pincode int,phone int,dr_name varchar(20))""")
def display_user_by_phone():
    phone=int(input("Enter phone number ~"))
    sql='select * from user_register where phone=%s'
    values=(phone,)
    cursor.execute(sql,values)
    user=cursor.fetchone()
    print("Aadhaar No.   |            Name            | Age | Phone |")
    print("{0:<14}{1:<27}{2:<5}{3:<3}".format(user[0],user[1],user[2],user[3]))
def display_dose_details(): # display all dose details
    print("Dose details ~")
    sql="select * from dose_details"
    cursor.execute(sql)
    doses=cursor.fetchall()
    print("_____________________________________________________________________________________________________________")
    print("| Dose ID | Hospital ID  |        Dose Name        | Price  |  Dose Date | Slot 1 | Slot 2 | Slot 3 | Slot 4|")
    for dose in doses:
        print("|{0:^9}|{1:^14}|{2:^25}|{3:<8}|{4:<12}|{5:^8}|{6:^8}|{7:^8}|{8:^7}|".format(dose[0],dose[1],dose[2],dose[3],str(dose[4]),dose[5],dose[6],dose[7],dose[8]))
    print("-------------------------------------------------------------------------------------------------------------")
    admin_menu()

def display_hospitals(): # display all hospitals
    print("Hospital details ~")
    sql="select * from hospital"
    cursor.execute(sql)
    print("___________________________________________________________________________________________________")
    hospitals=cursor.fetchall()
    print('| ID |   Hospital Name   |       Hospital Address       |Pincode |Phone Number |    Doctor Name   |')
    for hospital in hospitals:
        print("|{0:<4}|{1:<19}|{2:<30}|{3:<8}|{4:<13}|{5:<18}|".format(hospital[0],hospital[1],hospital[2],hospital[3],hospital[4],hospital[5]))
    print("---------------------------------------------------------------------------------------------------")
    admin_menu()

def display_registered_users():
    print("Registered users ~")
    sql="select * from user_register"
    cursor.execute(sql)
    users=cursor.fetchall()
    print("_______________________________________________________________")
    print("| Aadhaar No.  |          Name           | Age |    Phone     |")
    for user in users:
        print("|{0:^14}|{1:^25}|{2:^5}|{3:^14}|".format(user[0],user[1],user[2],user[3]))
    print("---------------------------------------------------------------")
    admin_menu()

def insert_dummy_hospitals(): # sample hospital records
    cursor.execute("insert into hospital values(1,'aiims','basni industrial area',342005,029156894,'Dr. Abz')")
    cursor.execute("insert into hospital values(2,'MdM','sector-H Shastri nagar,jodhpur',342003,029195618,'Dr. mvn')")
    cursor.execute("insert into hospital values(3,'MGM','jalori gate,jodhpur',342001,029156481,'Dr. ytu')")
    cursor.execute("insert into hospital values(4,'choupasni satt','choupasni jodhpur',342003,029189451,'Dr. erp')")
    cursor.execute("insert into hospital values(5,'pratap nagar SH-2','pratap nagar jodhpur',342003,029189417,'Dr. opt')")
    db.commit()
    print("                      >>> Dummy records inserted <<<")
    admin_menu()


def add_hospital(): # add a new hospital
    print("~ Add New Hospital ~")
    sql='select max(h_id) from hospital'
    cursor.execute(sql)
    result=cursor.fetchone()
    if result[0]==None:
        hospital_id=1
    else:
        hospital_id=result[0]+1
    hospital_name=input("Enter hospital name ~")
    address=input("Enter address ~")
    pincode=int(input("Enter pincode ~"))
    phone=int(input("Enter phone number ~"))
    doctor_name=input("Enter doctor name ~")
    sql='insert into hospital values(%s,%s,%s,%s,%s,%s)'
    values=(hospital_id,hospital_name,address,pincode,phone,doctor_name)
    cursor.execute(sql,values)
    db.commit()
    admin_menu()
    print("                      >>> New hospital added <<<")
def add_dose(): # admin adds a new dose
    print("~ Add New Dose Details ~")
    sql='select max(did) from dose_details'
    cursor.execute(sql)
    result=cursor.fetchone()
    if result[0]==None:
        dose_id=1
    else:
        dose_id=result[0]+1
    sql='select max(hid) from dose_details'
    cursor.execute(sql)
    result=cursor.fetchone()
    if result[0]==None:
        hospital_id=1
    else:
        hospital_id=result[0]+1
    dose_name=input("Enter dose name ~")
    price=int(input("Enter price ~"))
    dose_date=input("Enter date (yyyy/mm/dd) ~")
    slot1=int(input("Enter capacity for slot 1 ~"))
    slot2=int(input("Enter capacity for slot 2 ~"))
    slot3=int(input("Enter capacity for slot 3 ~"))
    slot4=int(input("Enter capacity for slot 4 ~"))
    sql='''insert into dose_details (did,hid,dose_name,price,dose_date,slot1,slot2,slot3,slot4)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    values=(dose_id,hospital_id,dose_name,price,dose_date,slot1,slot2,slot3,slot4)
    cursor.execute(sql,values)
    db.commit()
    print("                      >>> Dose added <<<")
    admin_menu()
def mark_vaccinated(): # admin marks a dose as given, enabling the certificate
    print("~ Mark Dose as Given ~")
    aadhaar_no=int(input("Enter Aadhaar number ~"))
    sql='select marker1,marker2 from register_vaccine where adharno=%s'
    values=(aadhaar_no,)
    cursor.execute(sql,values)
    markers=cursor.fetchone()
    vaccinated='y'
    if markers[0]=='n':
        sql='update register_vaccine set marker1=%s where adharno=%s'
        print("                      >>> Vaccinated successfully with dose 1 <<<")
    else:
        sql='update register_vaccine set marker2=%s where adharno=%s'
        print("                      >>> Vaccinated successfully with dose 2 <<<")
    values=(vaccinated,aadhaar_no)
    cursor.execute(sql,values)
    db.commit()
def update_registered_user(): # update user details
    print("~ Update User Information ~")
    aadhaar_no=int(input("Enter Aadhaar number ~"))
    sql='select * from user_register where adharno=%s'
    values=(aadhaar_no,)
    cursor.execute(sql,values)
    user=cursor.fetchone()
    name=input("Enter name [o to keep current] ~")
    if name=='o':
        name=user[1]
    age=int(input("Enter age [0 to keep current] ~"))
    if age==0:
        age=user[2]
    phone=int(input("Enter phone number [0 to keep current] ~"))
    if phone==0:
        phone=user[3]
    sql='update user_register set name=%s,age=%s,phone=%s where adharno=%s'
    values=(name,age,phone,aadhaar_no)
    cursor.execute(sql,values)
    db.commit()

def update_hospital(): # update hospital details
    print("~ Update Hospital Phone Number & Doctor Name ~")
    hospital_id=int(input("Enter hospital ID ~"))
    sql='select * from hospital where h_id=%s'
    values=(hospital_id,)
    cursor.execute(sql,values)
    hospital=cursor.fetchone()
    print(hospital)
    choice=int(input("""
            ********************************************
            * 1. Update phone number                   *
            * 2. Update doctor name                    *
            * 3. Update phone number and doctor name   *
            ********************************************
            Enter your choice >>>"""))

    if choice==1:
        phone=int(input("Enter new phone number ~"))
        sql="update hospital set phone=%s where h_id=%s"
        values=(phone,hospital_id)
        cursor.execute(sql,values)
        db.commit()
        print("                      >>> Phone number updated <<<")
    elif choice==2:
        doctor_name=input("Enter new doctor name ~")
        sql="update hospital set dr_name=%s where h_id=%s"
        values=(doctor_name,hospital_id)
        cursor.execute(sql,values)
        db.commit()
        print("                      >>> Doctor name updated <<<")
    elif choice==3:
        phone=int(input("Enter new phone number ~"))
        doctor_name=input("Enter new doctor name ~")
        sql="update hospital set phone=%s,dr_name=%s where h_id=%s"
        values=(phone,doctor_name,hospital_id)
        cursor.execute(sql,values)
        db.commit()
        print("                      >>> Phone number and doctor name updated <<<")
    admin_menu()

def delete_registered_user(): # delete a registered user
    print("~ Delete Registered User ~")
    aadhaar_no=int(input("Enter Aadhaar number ~"))
    sql='delete from user_register where adharno=%s'
    values=(aadhaar_no,)
    cursor.execute(sql,values)
    db.commit()
    print("                      >>> User deleted <<<")


def admin_login(): # admin login
    #username=input("Enter username")
    #password=input("Enter password")
    #if username=='admin' and password=='admin':
        #print("You have logged in successfully")
    admin_menu()

def admin_menu():
    choice=int(input("""
                *******************************************************
                * 1. Add new hospital                                 *
                * 2. Add daily dose                                   *
                * 3. Register new user                                *
                * 4. Display all hospitals                            *
                * 5. Display daily dose details                       *
                * 6. Display all registered users                     *
                * 7. Display all slots (not working)                  *
                * 8. Update hospital (phone number and doctor name)   *
                * 9. Delete registered user                           *
                * 10. Mark dose as given (for certificate)            *
                * 0. Log out                                          *
                * 98. Go to main menu                                 *
                * 99. Insert dummy hospital records                   *
                *******************************************************
                Enter your choice >>>"""))

    if choice==1:
        add_hospital()
    elif choice==2:
        add_dose()
    elif choice==3:
        register_user()
        admin_menu()
    elif choice==4:
        display_hospitals()
    elif choice==5:
        display_dose_details()
    elif choice==6:
        display_registered_users()
    elif choice==8:
        update_hospital()
    elif choice==7:
        display_dose_details()
    elif choice==0:
        print("You have logged out")
        exit()
    elif choice==9:
        delete_registered_user()
        admin_menu()
    elif choice==10:
        mark_vaccinated()
    elif choice==98:
        main_menu()
    elif choice==99:
        insert_dummy_hospitals()
    else:
        print("Enter a valid choice")
def print_certificate():
    aadhaar_no=int(input("Enter Aadhaar number ~"))
    sql='select marker1 from register_vaccine where adharno=%s and marker1="y"'
    values=(aadhaar_no,)
    cursor.execute(sql,values)
    result=cursor.fetchone()
    print(result)
    if result==None:
        print("You are not vaccinated")
    else:
        choice=int(input("""
            1. Print certificate for dose 1
            2. Print certificate for dose 2
            Enter your choice >>>"""))

        if choice==1:


            sql="""select regid,DOA1,ndose,h_id1,amt1, ur.* from user_register ur, register_vaccine rv
                    where ur.adharno=%s and marker1="y" and ur.adharno=rv.adharno"""
            values=(aadhaar_no,)
            cursor.execute(sql,values)
            record=cursor.fetchone()
            print('Aadhaar No. ~',aadhaar_no)
            print('Name ~',record[6])
            print('Age ~',record[7])
            print('Phone Number ~',record[8])
            print('Registration ID ~',record[0])
            print('Date of Dose 1 ~',record[1])
            print('No. of Doses ~',record[2])
            print('Hospital ID ~',record[3])
            print('Amount ~',record[4])
        elif choice==2:
            sql='select * from user_register where adharno=%s'
            values=(aadhaar_no,)
            cursor.execute(sql,values)
            user=cursor.fetchone()
            print('Aadhaar No. ~',user[0])
            print('Name ~',user[1])
            print('Age ~',user[2])
            print('Phone Number ~',user[3])
            sql='select regid,DOA1,DOA2,ndose,h_id1,amt1,h_id2,amt2 from register_vaccine where adharno=%s'
            values=(aadhaar_no,)
            cursor.execute(sql,values)
            booking=cursor.fetchone()
            print('Registration ID ~',booking[0])
            print('Date of Dose 1 ~',booking[1])
            print('Date of Dose 2 ~',booking[2])
            print('No. of Doses ~',booking[3])
            print('Hospital ID (Dose 1) ~',booking[4])
            print('Amount for Dose 1 ~',booking[5])
            print('Hospital ID (Dose 2) ~',booking[6])
            print('Amount for Dose 2 ~',booking[7])

def register_user(): # register for vaccination
    aadhaar_no=int(input("Enter your Aadhaar number ~"))
    name=input("Enter name ~")
    age=int(input("Enter age ~"))
    phone=input("Enter phone number ~")
    sql='insert into user_register values(%s,%s,%s,%s)'
    values=(aadhaar_no,name,age,phone)
    cursor.execute(sql,values)
    db.commit()
    print("Your registration is saved")
def book_vaccine(): # book a vaccine slot
    aadhaar_no=int(input("Enter Aadhaar number ~"))
    sql='select adharno from user_register where adharno=%s'
    values=(aadhaar_no,)
    cursor.execute(sql,values)
    result=cursor.fetchone()
    if result==None:
        print("New users must register first")
        choice=int(input("""
                        1. Go back
                        2. Register as a new user
                        Enter your choice >>>"""))
        if choice==1:
            main_menu()
        else:
            register_user()
    else:
            sql='select hid,slot1,slot2,slot3,slot4,slot1_used,slot2_used,slot3_used,slot4_used from dose_details'
            cursor.execute(sql)
            slots=cursor.fetchall()
            for slot in slots:
                print(slot[0],slot[1]-slot[5],slot[2]-slot[6],slot[3]-slot[7],slot[4]-slot[8])
            hospital_id=int(input("Enter hospital ID ~"))
            slot_no=int(input("Enter slot number (1, 2, 3 or 4) ~"))
            # reserve a seat in the chosen slot
            if slot_no==1:
                sql='select slot1_used from dose_details where hid=%s '
                values=(hospital_id,)
                cursor.execute(sql,values)
                result=cursor.fetchone()
                used=int(result[0])
                used+=1
                sql='update dose_details set slot1_used=%s where hid=%s'
                values=(used,hospital_id)
                cursor.execute(sql,values)
            elif slot_no==2:
                sql='select slot2_used from dose_details where hid=%s'
                values=(hospital_id,)
                cursor.execute(sql,values)
                result=cursor.fetchone()
                used=int(result[0])
                used+=1
                sql='update dose_details set slot2_used=%s where hid=%s'
                values=(used,hospital_id)
                cursor.execute(sql,values)
            elif slot_no==3:
                sql='select slot3_used from dose_details where hid=%s'
                values=(hospital_id,)
                cursor.execute(sql,values)
                result=cursor.fetchone()
                used=int(result[0])
                used+=1
                sql='update dose_details set slot3_used=%s where hid=%s'
                values=(used,hospital_id)
                cursor.execute(sql,values)
            elif slot_no==4:
                sql='select slot4_used from dose_details where hid=%s'
                values=(hospital_id,)
                cursor.execute(sql,values)
                result=cursor.fetchone()
                used=int(result[0])
                used+=1
                sql='update dose_details set slot4_used=%s where hid=%s'
                values=(used,hospital_id)
                cursor.execute(sql,values)
            db.commit()
            dose_date=input("Enter date (yyyy/mm/dd) ~")
            sql='select adharno from register_vaccine where adharno=%s' # check whether this is the user's first dose
            values=(aadhaar_no,)
            cursor.execute(sql,values)
            result=cursor.fetchone()
            if result==None:
                sql='select max(regid) from register_vaccine'
                cursor.execute(sql)
                result=cursor.fetchone()
                print(result)
                if result[0]==None:
                    registration_id=1
                else:
                    registration_id=int(result[0])+1

                dose_count=1
                sql='select price from dose_details where hid=%s and dose_date=%s'
                values=(hospital_id,dose_date)
                cursor.execute(sql,values)
                result=cursor.fetchone()
                amount=result[0]
                print(amount)
                sql='insert into register_vaccine(regid,adharno,DOA1,ndose,h_id1,amt1) values(%s,%s,%s,%s,%s,%s)'
                values=(registration_id,aadhaar_no,dose_date,dose_count,hospital_id,amount)
                cursor.execute(sql,values)
                db.commit()
                print("Dose 1 booked successfully")

            else:
                dose_count=2
                amount=int(input("Enter amount for dose 2 ~"))
                sql='update register_vaccine set DOA2=%s,ndose=%s,h_id2=%s,amt2=%s where adharno=%s'
                values=(dose_date,dose_count,hospital_id,amount,aadhaar_no)
                cursor.execute(sql,values)
                db.commit()
                print("Dose 2 booked successfully")
# entry point
def main_menu():
    while True:
        choice=int(input("""
                **********************
                *  1. Administrator  *
                *  2. General Public *
                *  3. Exit           *
                **********************
                Enter your choice >>>"""))
        if choice==1:
            admin_login()
        if choice==2:
            public_choice=int(input("""
                    **********************************
                    * 1. Register for vaccination    *
                    * 2. Book vaccine                *
                    * 3. Display your details        *
                    * 4. Update your details         *
                    * 5. Delete your registration    *
                    * 6. Print your certificate      *
                    **********************************
                    Enter your choice >>>"""))
            if public_choice==1:
                register_user()
            elif public_choice==2:
                book_vaccine()
            elif public_choice==3:
                display_user_by_phone()
            elif public_choice==4:
                update_registered_user()
            elif public_choice==5:
                delete_registered_user()
            elif public_choice==6:
                print_certificate()


main_menu()
