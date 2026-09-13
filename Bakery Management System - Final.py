# ====== Final Douce Lune Bakery System ======

import random
import string
from datetime import date, datetime
import mysql.connector as mc

# Global flag
flag = True

# -------------------- CAPTCHA --------------------
def simple_captcha():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    print(f"\n🔒 Simple Verification — Enter this code exactly:\n[{code}]")
    user_input = input("Enter the code: ").strip()
    if user_input == code:
        print("✅ Verification passed!")
        return True
    else:
        print("\n❌ CAPTCHA failed. Try again.\n")
        return False

# -------------------- LOGIN --------------------
def login():
    global flag
    flag = True
    global cid
    cid = None
    while flag:
        identifier = input("Are you a customer or administrator? ")
        if identifier.lower() == 'customer':
            entry = input("\nDo you want to Login or Sign-Up? ")
            # Customer - Login
            if entry.lower() == 'login':
                while flag:
                    global username
                    username = input("Enter your Username: ")
                    cur.execute("SELECT USERNAME FROM CUSTOMER WHERE USERNAME=%s", (username.lower(),))
                    result = cur.fetchone()
                    if result:
                        passwd = input("Enter your password: ")
                        cur.execute("SELECT PASSWORD FROM CUSTOMER WHERE USERNAME=%s", (username,))
                        result1 = cur.fetchone()
                        if result1 and passwd == result1[0]:
                            if simple_captcha():
                                print("\n✅ Logged In Successfully!\n")
                                cur.execute("SELECT CID FROM CUSTOMER WHERE USERNAME=%s", (username,))
                                cid = cur.fetchone()[0]
                                flag = False
                        else:
                            print("\n❌ Invalid Password!\n")
                    else:
                        print(f"\n❌ Username {username} not found!\n")
                        ans = input("Try Re-Login (#) or Sign-Up (@)? ")
                        if ans == "#":
                            continue
                        elif ans == "@":
                            cur.execute("SELECT CID FROM CUSTOMER;")
                            data = cur.fetchall()
                            cust_id = data[-1][0]+1
                            name = input("\nEnter your name: ")
                            gen = input('Enter your gender: ')
                            while True:
                                cont = input('Enter your contact number: ')
                                if not(len(cont)>=10 and len(cont)<=13):
                                    print('\nEnter a valid contact\n')
                                else:
                                    break
                            add = input('Enter your address: ')
                            c_code = int(input('Enter your city code: '))
                            while True:
                                username = input('Enter a username (Gmail Id): ')
                                if '@' in username:
                                    break
                                else:
                                    print('\nEnter a valid username!\n')
                            passwd = input("Create password: ") 
                            cur.execute(f"INSERT INTO CUSTOMER VALUES ({cust_id},'{name}','{gen}', '{cont}', '{add}', {c_code}, '{username}', '{passwd}');")
                            db.commit()
                            print("\n✅ Sign-Up successful!\n")
                        else:
                            break
            # Customer - Sign-Up
            elif entry.lower() == 'sign-up':
                cur.execute("SELECT CID FROM CUSTOMER;")
                data = cur.fetchall()
                cust_id = data[-1][0]+1
                name = input("\nEnter your name: ")
                gen = input('Enter your gender: ')
                while True:
                    cont = input('Enter your contact number: ')
                    if not(len(cont)>=10 and len(cont)<=13):
                        print('\nEnter a valid contact\n')
                    else:
                        break
                add = input('Enter your address: ')
                c_code = int(input('Enter your city code: '))
                while True:
                    username = input('Enter a username (Gmail Id): ')
                    if '@' in username:
                        break
                    else:
                        print('\nEnter a valid username!\n')   
                passwd = input("Create password: ") 
                cur.execute(f"INSERT INTO CUSTOMER VALUES ({cust_id},'{name}','{gen}', '{cont}', '{add}', {c_code}, '{username}', '{passwd}');")
                db.commit()
                print("\n✅ Sign-Up successful!\n")
            else:
                print('\nEnter a valid choice\n')
        # Admin - Login
        elif identifier.lower() == 'administrator':
            try:
                aid = int(input("\nEnter Admin ID: "))
            except ValueError:
                print("Invalid Admin ID.")
                continue
            passwd = input("Enter Password: ")
            cur.execute("SELECT PASSWORD FROM ADMIN WHERE AdNo=%s", (aid,))
            result = cur.fetchone()
            if result and passwd == result[0]:
                if simple_captcha():
                    print("\n✅ Admin Logged In Successfully!\n")
                    flag = False
            else:
                print("\n❌ Invalid Admin credentials.\n")
        else:
            print("\nEnter either 'customer' or 'administrator'.\n")
    return identifier, flag

# -------------------- ADMIN --------------------
def Admin():
    while True:
        print("========== ADMIN MENU ==========")
        print("1. Add New Product\n2. Update Product Details\n3. Delete Product\n4. View All Customer Orders\n5. View Orders of a Customer\n6. Logout")
        choice = input("Choice: ")
        if choice=='1':
            try:
                PdNo=int(input("\nEnter the Product ID: "))
                PdName=input("Enter the Product Name: ")
                UtPr=float(input("Enter the Unit Price: "))
                Qty=int(input("Enter the Quantity available: "))
            except ValueError:
                print("\nInvalid input.\n")
                continue
            cur.execute("INSERT INTO PRODUCT (PdNo,PdName,UtPr,QTY) VALUES (%s,%s,%s,%s)", (PdNo,PdName,UtPr,Qty))
            db.commit()
            print("\n✅ Product added!\n")
        elif choice=='2':
            try:
                PdNo=int(input("\nEnter the Product ID to update: "))
            except ValueError:
                print("\nInvalid Product ID.\n")
                continue
            print("\nChoose the field that needs to be updated\n1. Name\n2. Price\n3. Quantity")
            u=input("Choice: ")
            if u=='1':
                cur.execute("UPDATE PRODUCT SET PdName=%s WHERE PdNo=%s",(input("New name: "),PdNo))
            elif u=='2': 
                try:
                    cur.execute("UPDATE PRODUCT SET UtPr=%s WHERE PdNo=%s",(float(input("New price: ")),PdNo))
                except:
                    print("\nInvalid price.\n")
                    continue
            elif u=='3':
                try:
                    cur.execute("UPDATE PRODUCT SET QTY=%s WHERE PdNo=%s",(int(input("New qty: ")),PdNo))
                except:
                    print("\nInvalid quantity.\n")
                    continue
            else:
                print("\nInvalid option.\n")
                continue
            db.commit()
            print("\n✅ Updated successfully!\n")
        elif choice=='3':
            try:
                PdNo=float(input("\nEnter the Product ID of the product to delete: "))
            except ValueError:
                print("\nInvalid ID.\n")
                continue
            cur.execute("DELETE FROM PRODUCT WHERE PdNo=%s",(PdNo,))
            db.commit()
            print("\n✅ Product deleted!\n")
        elif choice=='4':
            cur.execute("SELECT * FROM ORDERS")
            orders=cur.fetchall()
            if not orders:
                print("\nNo orders.\n")
                continue
            print()
            print('SNO\tOrder Number\tPdNo\tCID\tQTY\tRating\tDate')
            for row in orders:
                for j in range(len(row)):
                    if j == 6:
                        print(str(row[j]), end='\t')
                    else:
                        print(row[j], end= '\t')
                print()
            print()
        elif choice=='5':
            cname=input("\nEnter the Customer Name: ")
            contact=input("Enter the Contact No: ")
            cur.execute("SELECT CID FROM CUSTOMER WHERE CNAME=%s AND CONTACT=%s",(cname,contact))
            res=cur.fetchone()
            if res:
                cid=res[0]
                cur.execute("SELECT * FROM ORDERS WHERE CID=%s",(cid,))
                ords=cur.fetchall()
                if ords:
                    print('SNO\tOrder Number\tPdNo\tCID\tQTY\tRating\tDate')
                    for row in ords:
                        for i in range(len(row)):
                            if i==6:
                                print(row[i], end='\t')
                            else:
                                print(row[i], end='\t')
                        print()
                    print()
                else:
                    print("\nNo orders found.\n")
            else:
                print("\nCustomer not found.\n")
        elif choice=='6':
            print("\nLogged out.\n")
            break
        else:
            print("\nInvalid choice.\n")

# -------------------- CUSTOMER --------------------
def customer():
    while True:
        cur.execute(f"SELECT CNAME FROM CUSTOMER WHERE USERNAME = '{username}';")
        name = cur.fetchone()[0]
        print(f"HELLO {name}! What would you like to do Today?\n1. Place an Order\n2. View Past Orders\n3. Cancel an Order\n4. Rate an Order\n5. Logout")
        ch=input("Choice: ")
        if ch=='1':
            cur.execute("SELECT * FROM PRODUCT")
            products=cur.fetchall()
            print("\nMENU")
            [print(f"{p[0]} - {p[1]} ({p[2]})") for p in products]
            cart=[]
            total=0
            while True:
                p=input("\nEnter the Product No: ")
                p=int(p) if p.isdigit() else -1
                if p in [x[0] for x in products]:
                    pd=[x for x in products if x[0]==p][0]
                    qty=int(input("Enter the Quantity you require: "))
                    cart.append([pd[0],pd[1],qty,pd[2]])
                    total+=qty*pd[2]
                else:
                    print("\nInvalid product.\n")
                more=input("\nOrder more? (Y/N): ")
                if more.lower() != 'y':
                    break
            cur.execute("SELECT SNO FROM ORDERS ORDER BY SNO DESC LIMIT 1")
            last = cur.fetchone()
            sno = last[0]+1 if last else 1
            t_date=str(date.today())
            num_st = ''.join(t_date.split('-'))
            cur.execute(f"SELECT ORD_NUM FROM ORDERS WHERE ORD_NUM LIKE '{num_st}%';")
            ord_numbers = cur.fetchall()
            if ord_numbers:
                ord_c = int(ord_numbers[-1][0][-1])
            else:
                ord_c = 1
            for item in cart:

                if ord_c<10:
                    ord_num = num_st + '-0'+str(ord_c)
                else:
                    ord_num = num_st + '-'+str(ord_c)
                ord_c+=1
                cur.execute("INSERT INTO ORDERS (SNO,ORD_NUM,PdNo,CID,QTY,RATING,DATE) VALUES (%s,%s,%s,%s,%s,NULL,%s)", (sno,ord_num,item[0],cid,item[2],t_date))
                cur.execute("UPDATE PRODUCT SET QTY=QTY-%s WHERE PdNo=%s", (item[2],item[0]))
                sno += 1
                db.commit()
            print(f"\n✅ Order placed! Total = {total}\n")
            payment()
        elif ch=='2':
            cur.execute("SELECT PRODUCT.PdName,PRODUCT.UtPr,ORDERS.QTY FROM ORDERS JOIN PRODUCT ON ORDERS.PdNo=PRODUCT.PdNo WHERE ORDERS.CID=%s",(cid,))
            past=cur.fetchall()
            if not past:
                print("\nNo past orders.\n")
            else:
                print("\nProduct\t\tPrice\tQty")
                [print(f"{x[0]}\t{x[1]}\t{x[2]}") for x in past]
                print()
        elif ch=='3':
            onum=input("\nEnter the Order No: ")
            cur.execute("SELECT * FROM ORDERS WHERE CID=%s AND ORD_NUM=%s",(cid,onum))
            if not cur.fetchall():
                print("\nInvalid order number.\n")
                continue
            cur.execute("DELETE FROM ORDERS WHERE CID=%s AND ORD_NUM=%s",(cid,onum))
            db.commit()
            print("\n✅ Order cancelled!\n")
        elif ch=='4':
            onum=input("\nEnter the Order No: ")
            try:
                rate=int(input("\nRate 1-5: "))
            except:
                print("\nInvalid input.\n")
                continue
            cur.execute("UPDATE ORDERS SET RATING=%s WHERE CID=%s AND ORD_NUM=%s",(rate,cid,onum))
            db.commit()
            print("\n✅ Thank you for rating!\n")
        elif ch=='5':
            print("\nThank you for choosing Douce Lune Bakery!\n")
            break
        else:
            print("\nInvalid choice.\n")

# -------------------- PAYMENT --------------------
def payment():
    print("Choose payment method:\n1. Card\n2. UPI\n3. Cash")
    pay=input("Choice: ")
    t_date=str(date.today())
    time=datetime.now().strftime("%H:%M:%S")
    if pay=='1':
        try:
            card=int(input("\nCard No: "))
            cvv=int(input("CVV: "))
        except:
            print("Invalid data.")
            return
        name=input("Name on card: ")
        exp=input("Expiry: ")
        print(f"\n✅ Payment successful on {t_date} at {time}\n")
    elif pay=='2':
        while True:
            user=input("\nUPI ID: ")
            if '@ok' in user:
                break
            else:
                print('\nEnter a valid UPI ID!\n')
        try:
            pin=int(input("PIN: "))
        except:
            print("Invalid.")
            return
        print(f"\n✅ Payment successful on {t_date} at {time}\n")
    elif pay=='3':
        print("\n✅ Cash order confirmed, track your order!\n")
    else:
        print("\nEnter a valid choice!\n")

# -------------------- DATABASE CONNECTION --------------------
db = mc.connect(host='localhost', user='root', password='your_password')
cur = db.cursor()
cur.execute("USE BAKERY;")

# -------------------- MAIN LOOP --------------------
while True:
    print("Welcome to Douce Lune Bakery - Où chaque bouchée semble être un rêve!")
    iden, f = login()
    if iden.lower()=='customer' and f==False:
        customer()
        ch=input("Exit page? (Y/N): ")
        if ch.lower()=='y':
            break
    elif iden.lower()=='administrator' and f==False:
        Admin()
        ch=input("Exit page? (Y/N): ")
        if ch.lower()=='y':
            break

