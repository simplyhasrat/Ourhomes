
# CLASS 12 PROJECT
# By Arshiya Malhotra, Anubhav Rawat and Dakshita Yadav

import mysql.connector

cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',)
cur=cn.cursor()
cur.execute("Create database Ourhomes")
cur.execute("use Ourhomes")
cur.execute("create table Residents (House_no varchar(10) Primary Key,Owner_name varchar(50) NOT NULL,Contact_no char(10) NOT NULL,Two_wheeler_1 varchar(15),Two_wheeler_2 varchar (15),Four_wheeler_1 integer,Four_wheeler_2 integer)")
cur.execute("create table Help (Help_id varchar(6) Primary Key,Help_Name varchar(50),Contact_no char(10),Service varchar(15),Date_of_registration date)")
cur.execute("create table records(House_no varchar(10),Vehicle_no varchar(15),Name varchar(50) Not NULL,Contact_no char(10) Not NULL,Entry_date date,Entry_time time,Exit_date date,Exit_time time,Help_id varchar(6))")
cur.execute('insert into residents(house_no,owner_name,contact_no) values("1001","Vidhi Sharma","9810010021")')
cur.execute('insert into residents(house_no,owner_name,contact_no) values("1002","Subhash Yadav","9700010034")')
cur.execute('insert into residents(house_no,owner_name,contact_no,Two_wheeler_1) values("1003","Dheeraj","9000880009","HR 26 DQ 6001")')
cur.execute("insert into Help (Help_id ,Help_Name,Contact_no ,Service ,Date_of_registration) values('102','Akshit Rana','9989888998','maid','2003-05-05')")
cur.execute("insert into Help (Help_id ,Help_Name,Contact_no ,Service ,Date_of_registration) values('101','Vasu Yadav','8293748489','maid','2005-07-05')")
cur.execute("insert into Help (Help_id ,Help_Name,Contact_no ,Service ,Date_of_registration) values('103','Sivani Verma','9836201897','maid','2023-01-09')")
cn.commit()
cn.close()

def record_entry():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    print("""------------------
1. Helper entry
2. Outsider entry
------------------""")
    try:
        choice= int(input("Enter visitor type : "))
        if choice==1:
            help_id=input("Enter id : ")
            h=(help_id,)
            q="select Help_Name,Contact_no,Help_id from Help where Help_id=%s"
            cur.execute(q,h)
            rec=cur.fetchone()
            if rec==None:
                print("SECURITY ALERT! : Id not found")
            else:
                q2="select name from records where Help_id=%s and Exit_date is NULL"
                cur.execute(q2,h)
                rec2=cur.fetchone()
                if rec2==None:
                    q3="insert into records(Name,Contact_no,Help_id,Entry_date,Entry_time) values(%s,%s,%s,date(now()),time(now()))"
                    cur.execute(q3,rec)
                    cn.commit()
                    print("Entry Recorded")
                else:
                    print("SECURITY ALERT! : Visitor still inside/Last entry not recorded")
        elif choice==2:
            house_no=input("Enter the house no. you wish to visit : ")
            h=(house_no,)
            q="select * from Residents where House_no=%s"
            cur.execute(q,h)
            rec=cur.fetchone()
            if rec==None:
                print("SECURITY ALERT! : Entered house no. does not exist")
            else:
                name=input("Enter name : ")
                contact_no=input("Enter contact no : ")
                choice2=input("Vehicle? (Y/N) ")
                if choice2 in 'Yy':
                    vehicle_no=input("Enter vehicle no : ")
                    q2="insert into records(House_no,Vehicle_no,Name,Contact_no,Entry_date,Entry_time) values(%s,%s,%s,%s,date(now()),time(now()))"
                    data=(house_no,vehicle_no,name,contact_no)
                    cur.execute(q2,data)
                    cn.commit()
                    print("Record Entered")
                else:
                    q2="insert into records(House_no,Name,Contact_no,Entry_date,Entry_time) values(%s,%s,%s,date(now()),time(now()))"
                    data=(house_no,name,contact_no)
                    cur.execute(q2,data)
                    cn.commit()
                    print("Record Entered")
        else:
            print("Invalid Input")
    except:
        print("Error occured")



def record_exit():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    print("""------------------
1. Help 
2. Outsider visit
------------------""")
    try:
        choice= int(input("Enter visitor type : "))
        if choice==1:
            help_id=input("Enter id : ")
            h=(help_id,)
            q="select Help_Name from Help where Help_id=%s"
            cur.execute(q,h)
            rec=cur.fetchone()
            if rec==None:
                print("SECURITY ALERT! : Id not found")
            else:
                q2="select name from records where Help_id=%s and Exit_date is NULL"
                cur.execute(q2,h)
                rec2=cur.fetchone()
                if rec2==None:
                    print("SECURITY ALERT! : Entry not recorded for id = ",help_id,"; name = ",rec[0])
                else :
                    q2="update records set Exit_date=date(now()),Exit_time=time(now()) where Help_id=%s and Exit_date is NULL"
                    cur.execute(q2,h)
                    cn.commit()
                    print("Exit Recorded")
        elif choice==2:
            contact_no=input("Enter contact no : ")
            c=(contact_no,)
            q="select name,house_no from records where contact_no=%s"
            cur.execute(q,c)
            rec=cur.fetchone()
            if rec==None:
                print("Entry record for ",contact_no,"does not exist")
                choice2=input("Try by House no. instead? (Y/N) : ")
                if choice2 in 'Yy':
                    house_no=input("Enter house no. : ")
                    h=(house_no,)
                    q2="select name,entry_date,entry_time from records where house_no=%s and Exit_date is NULL"
                    cur.execute(q2,h)
                    rec2=cur.fetchall()
                    if rec2==None:
                        print("No Record found")
                    else:
                        for i in rec2:
                            print("Record -",i[0]," - ",i[1]," - ",i[2])
                            choice3=input("Press Y if this is your record : ")
                            if choice3 in "Yy":
                                q2="update records set Exit_date=date(now()),Exit_time=time(now()) where name=%s and entry_date=%s and entry_time=%s and Exit_date is NULL"
                                cur.execute(q2,i)
                                cn.commit()
                                print("Exit Recorded")
                                break
                        else:
                            print("No more Records")
            else:
                print("Record by the name",rec[0],"for house no.",rec[1])
                choice2=input("Continue? (Y/N) : ")
                if choice2 in "yY":
                    q2="update records set Exit_date=date(now()),Exit_time=time(now()) where contact_no=%s and Exit_date is NULL"
                    cur.execute(q2,c)
                    cn.commit()
                    print("Exit Recorded")
        else:
            print("Invaid Input")
    except:
        print("Error occured")
        


def show_visitors_inside():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        cur.execute("select house_no,name,contact_no,entry_date,entry_time,vehicle_no from records where help_id is NULL and exit_date is NULL")
        rec=cur.fetchall()
        if rec==None or rec==[]:
            print("No outsider inside")
        else:
            print("Outsiders inside:-")
            for i in rec:
                for j in range(5):
                    print(i[j],end=" | ")
                print("Vehicle -",i[5])
                print()
        cur.execute("select help_id,name,contact_no,entry_date,entry_time from records where help_id is not NULL and exit_date is NULL")
        rec2=cur.fetchall()
        if rec2==None or rec2==[]:
            print("No help inside")
        else:
            print("Help inside :-")
            for a in rec2:
                for b in a:
                    print(b,end=" | ")
                print()
    except:
        print("An error occured")

def show_visitors_today():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    q="select * from records where entry_date=date(now())"
    cur.execute(q)
    rec=cur.fetchall()
    cn.commit()
    print("House_no | Vehicle_no | Name | Contact_no | Entry_date | Entry_time | Exit_date | Exit_time | Help_id")
    for i in rec:
        for j in i:
          print(j,end=" | ")
        print()

def show_visitors_foradate():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        d=input("Enter date (yyyy-mm-dd) : ")
        da=(d,d)
        q="select * from records where entry_date=%s or exit_date=%s"
        cur.execute(q,da)
        rec=cur.fetchall()
        cn.commit()
        print("House_no | Vehicle_no | Name | Contact_no | Entry_date | Entry_time | Exit_date | Exit_time | Help_id")
        for i in rec:
            for j in i:
                print(j,end=" | ")
            print()
    except:
        print("An errorr occured")
        
def print_residents():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    house_no=input("Enter the house no. of the record you want to print : ")
    h=(house_no,)
    q="select * from Residents where House_no=%s"
    cur.execute(q,h)
    rec=cur.fetchone()
    if rec==None:
        print("SECURITY ALERT : Entered house no. does not exist")
    else:
        print("House_no | Owner_name | Contact_no  | Two_wheeler_1 | Two_wheeler_2 | Four_wheeler_1 | Four_wheeler_2")
        for i in rec:
          print(i,end=" | ")




def insert_resident_record():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    try:
        cur=cn.cursor()
        house_no=input("Enter house no. : ")
        owner_name=input("Enter name of ownwer : ")
        contact_no=input("Enter contact no. : ")
        nt=int(input("Enter no. of two wheelers(0-2) : "))
        nf=int(input("Enter no. of four wheelers(0-2) : "))     
        if nt==0:
            if nf==0:
                s="insert into residents(house_no,owner_name,contact_no) values(%s,%s,%s)"
                v=(house_no,owner_name,contact_no)
                cur.execute(s,v)
                cn.commit()
            elif nf==1:
                fw1=input("Enter the car no. : ")
                s="insert into residents (house_no,owner_name,contact_no,Four_wheeler_1) values(%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1)
                cur.execute(s,v)
                cn.commit()
            elif nf==2:
                fw1=input("Enter 1st car no. : ")
                fw2=input("Enter 2nd car no. : ")
                s="insert into residents(house_no,owner_name,contact_no,Four_wheeler_1,Four_wheeler_2) values(%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1,fw2)
                cur.execute(s,v)
                cn.commit()                  
            else:
                print("Error : Only 0-2 four wheelers allowed ")
        elif nt==1:
            tw1=input("Enter vehicle no. of the two wheeler : ")
            if nf==0:
                s="insert into residents(house_no,owner_name,contact_no,Two_wheeler_1) values(%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,tw1)
                cur.execute(s,v)
                cn.commit()
            elif nf==1:
                fw1=input("Enter the car no. : ")
                s="insert into residents(house_no,owner_name,contact_no,Four_wheeler_1,Two_wheeler_1) values(%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1,tw1)
                cur.execute(s,v)
                cn.commit()
            elif nf==2:
                fw1=input("Enter 1st car no. : ")
                fw2=input("Enter 2nd car no. : ")
                s="insert into residents(house_no,owner_name,contact_no,Four_wheeler_1,Four_wheeler_2,Two_wheeler_1) values(%s,%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1,fw2,tw1)
                cur.execute(s,v)
                cn.commit()
            else:
                print("Error : Only 0-2 four wheelers allowed ")
        elif nt==2:
            tw1=input("Enter vehicle no. of 1st two wheeler : ")
            tw2=input("Enter vehicle no. of 2nd two wheeler : ")
            if nf==0:
                s="insert into residents(house_no,owner_name,contact_no,Two_wheeler_1,Two_wheeler_2) values(%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,tw1,tw2)
                cur.execute(s,v)
                cn.commit()
            elif nf==1:
                fw1=input("Enter the car no. : ")
                s="insert into residents(house_no,owner_name,contact_no,Four_wheeler_1,Two_wheeler_1,Two_wheeler_2) values(%s,%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1,tw1,tw2)
                cur.execute(s,v)
                cn.commit()
            elif nf==2:
                fw1=input("Enter 1st car no. : ")
                fw2=input("Enter 2nd car no. : ")
                s="insert into residents(house_no,owner_name,contact_no,Four_wheeler_1,Four_wheeler_2,Two_wheeler_1,Two_wheeler_2) values(%s,%s,%s,%s,%s,%s,%s)"
                v=(house_no,owner_name,contact_no,fw1,fw2,tw1,tw2)
                cur.execute(s,v)
                cn.commit()                 
            else:
                print("Error : Only 0-2 four wheelers allowed")
        else:
            print("Error : Only 0-2 two wheelers allowed")
    except:
        print("Error occured")
    cn.close()


def delete_residents():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        house_no=input("Enter the house no. for which record is to be deleted : ")
        h=(house_no,)
        q="select * from Residents where House_no=%s"
        cur.execute(q,h)
        rec=cur.fetchone()
        if rec==None:
            print("ALERT! : Entered house no. does not exist")
        else:
            h=(house_no,)  
            q="delete from Residents where House_no=%s"
            cur.execute(q,h)
            cn.commit()
            print("Record Deleted")
    except:
        print("Error occured")
    cn.close()

    
def update_residents():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        house_no=input("Enter the house no. of the record you want to update : ")
        h=(house_no,)
        q="select * from Residents where House_no=%s"
        cur.execute(q,h)
        rec=cur.fetchone()
        field=("Owner_name","Contact_no","Two_wheeler_1","Two_wheeler_2","Four_wheeler_1","Four_wheeler_2")
        rec2=rec[1::]
        print("Owner_name | Contact_no | Two_wheeler_1 | Two_wheeler_2 | Four_wheeler_1 | Four_wheeler_2")
        for i in rec:
          print(i,end=" | ")
        print()
        if rec2==None:
            print("SECURITY ALERT! : Entered house no. does not exist")
        else:
            for i in range(len(rec2)):
                print(field[i],":",rec2[i])
                choice=input("Update? (Y/N) ")
                if choice in "Yy":
                    val=input("Enter value : ")
                    q2="update residents set "+field[i]+"=%s where house_no=%s"
                    values=(val,house_no)
                    cur.execute(q2,values)
                    cn.commit()
                    print("Record Updated")
            print("-End of this record-")
    except:
        print("Error Occured !!!")
    cn.close()

def print_all_residents():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    q="select * from Residents"
    cur.execute(q)
    rec=cur.fetchall()
    print(("House_no | Owner_name | Contact_no  | Two_wheeler_1 | Two_wheeler_2 | Four_wheeler_1 | Four_wheeler_2"))
    for i in rec:
        for j in i:
          print(j,end=" | ")
        print()
    cn.close()


def insert_help_record():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    try:
        cur=cn.cursor()
        help_id=input("Enter id : ")
        help_name=input("Enter name : ")
        contact_no=input("Enter contact no. : ")
        print("""--------------
1. Driver
2. Maid
3. Laundry
4. Car wash
5. Gardening
6. others
--------------""")
        choice=int(input("Enter choice : "))
        if choice==1:
            service="Driver"
        elif choice==2:
            service="Maid"
        elif choice==3:
            service="Laundry"
        elif choice==4:
            service="Car wash"
        elif choice==5:
            service="Gardening"
        elif choice==6:
            service="Others"
        else:
            print("Invaid Input")
        s="insert into Help values(%s,%s,%s,%s,date(now()))"
        v=(help_id,help_name,contact_no,service)
        cur.execute(s,v)
        cn.commit()
        cn.close()
        print("Record Entered")
    except:
        print("Error occured")
    cn.close()




def show_help_record():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    for a in range(1):
        help_id=input("Enter id : ")
        h=(help_id,)
        q="select Help_Name,Contact_no from Help where Help_id=%s"
        cur.execute(q,h)
        rec=cur.fetchone()
        if rec==None:
            print("SECURITY ALERT : Id not found")
        else:
            q2="select help_id,name,contact_no,entry_date,entry_time,exit_date,exit_time from records where help_id=%s"
            cur.execute(q2,h)
            rec2=cur.fetchall()
            if rec2==[]:
                print("No record found")
            else:
                print("help_id | name | contact_no | entry_date | entry_time | exit_date | exit_time")
                for i in rec2:
                    for j in i:
                        print(j,end=" | ")
                    print()
    cn.close()

def search_help_record():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        help_id=input("Enter id : ")
        h=(help_id,)
        q="select * from Help where Help_id=%s"
        cur.execute(q,h)
        rec=cur.fetchone()
        if rec==None:
            print("Security Alert! : Id not found")
        else:
            print("Help id | Name | Contact no | Service | Date of registration ")
            for i in rec:
                print(i,end=" | ")
            print()
    except:
        print("Error occured")
    cn.close()
            


def print_all_help():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        q="select * from help"
        cur.execute(q)
        rec=cur.fetchall()
        print("Help id | Name | Contact no | Service | Date of registration ")
        for i in rec:
            print(i,end=" | ")
        print()
    except:
        print("Error occured")
    cn.close()
        

def delete_help():
    cn=mysql.connector.connect(host='localhost',
                               user='root',
                               password='root',
                               database='Ourhomes')
    cur=cn.cursor()
    try:
        help_id=input("Enter id : ")
        h=(help_id,)
        q="select * from Help where Help_id=%s"
        cur.execute(q,h)
        rec=cur.fetchone()
        if rec==None:
            print("SECURITY ALERT : Id not found")
        else:
            q="delete from Help where help_id=%s"
            cur.execute(q,h)
            cn.commit()
    except:
        print("Error occured")
    cn.close()
    
def menu2():
    while(1):
        print("1. Show a resident's record ")
        print("2. Add a resident's record ")
        print("3. Delete a resident's record")
        print("4. Update a resident's record")
        print("5. Show All Resident's Records ")
        print("Any other key to exit.")
        x=input("Your choice? : ")
        if x=="1" :
            print_residents()
        elif x=="2":
            insert_resident_record()
        elif x=="3":
            delete_residents()
        elif x=="4":
            update_residents()
        elif x=="5":
            print_all_residents()
        else:
            print("---------------------------------------------------------------------------------------------------------------")
            break
        print()

def menu3():
    while(1):
        print("1. Search for a helper's details")
        print("2. Add a helper's record")
        print("3. Delete a helper's record")
        print("4. Show All helper's Records")
        print("Any other key to exit.")
        x=input("Your choice? : ")
        if x=="1" :
            search_help_record()
        elif x=="2":
            insert_help_record()
        elif x=="3":
            delete_help()
        elif x=="4":
            print_all_help()
        else:
            print("---------------------------------------------------------------------------------------------------------------")
            break
        print()

def menu1():
    while(1):
        print("1. Record Entry ")
        print("2. Record Exit ")
        print("3. Show all Visitors inside")
        print("4. Show today's records")
        print("5. Search record for a particular date")
        print("6. Record of a particular helper ")
        print("Any other key to exit.")
        x=input("Your choice? : ")
        if x=="1" :
            record_entry()
        elif x=="2":
            record_exit()
        elif x=="3":
            show_visitors_inside()
        elif x=="4":
            show_visitors_today()
        elif x=="5":
            show_visitors_foradate()
        elif x=="6":
            show_help_record()
        else:
            print("---------------------------------------------------------------------------------------------------------------")
            break
        print()

def main():
    print()
    print("                             OURHOMES SOCIETY                             ")
    print("WELCOME!")
    print()
    while True:
        print("1. Visitor's records")
        print("2. Resident's data")
        print("3. Domestic Help's data")
        print("Any other key to exit.")
        x=input("Your choice? : ")
        print()
        if x=="1" :
            menu1()
        elif x=="2":
            menu2()
        elif x=="3":
            menu3()
        else:
            print()
            print('THANKS FOR VISITING!')
            print()
            break
        print()

main()



