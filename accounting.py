import json 

def register():
    print("Registration")
    user_username= input("Username: ")
    user_password= input("Password: ")
    
    user_dict = {user_username: user_password}
    
    write_into_files("accountlog.txt", user_dict)
    
    print("Registration successful!")
    ask = input("Do you want to login?(y/n) ").lower()
    if ask =='y':
        print("Type login ")
        main()
    
def login():        
    
    user_username = input("Username: ")
    user_password = input("Password: ")
    try:
        with open("accountlog.txt","r") as f:
            user_data = f.read()
            if not user_data:
                print("No registered users found!")
                
                ask = input("Do you want to register?(y/n) ").lower()
                if ask =='y':
                    register()
                # if not yes return garera program ends
                else:
                    return
    # argument ma pathako file chaina vane yo error fyalxa and return le end garxa            
    except FileNotFoundError:
        print("Error! File not found")   
        return
    # if false vo vane direct ya aauxa program data read garesi
    user_data_list= user_data.split("|")
    loginned = False
    
    for i in user_data_list:
        # checking to avoid empty i
        if i: 
            try:
                # Converts a JSON string back into a Python object(dictionary).
                user_dict_data = json.loads(i) 
                if user_username in user_dict_data and user_password == user_dict_data[user_username]:
                    print('Login Successfull')
                    loginned = True
                    return loginned, user_username
            except json.JSONDecodeError:
                continue
    print("Login failed! Invalid username or password. Try again")
    login()
    
def write_into_files(filename,write_dict):
    ##reading mode for list and comma because if data exists ->list  || else list vayeni initaialize garna suru mei comma add nahos vanera
    try:
        with open(filename, "r") as f:
            existing_data = f.read()
            # checks for data in the file and if exists converts it to list
            if existing_data:
                existing_data_list = existing_data.split("|")
            # list initialize gairakhne so that append part ma comma wala handle garxa as 0>0 false so no comma will be added
            else:
                existing_data_list = []
    #file vetena vane pani tala append mode ma create vaehalxa tei vara error nafyaleko               
    except FileNotFoundError:
        existing_data_list = []

    with open(filename, "a") as f:
        user_data_json = json.dumps(write_dict)
        #mathi read ma kholnu karan is this
        if len(existing_data_list) > 0:
            f.write("|")  
        f.write(user_data_json)       

    
def view_balance(user):
    
    with open("balance.txt") as f:
        content = f.read()
        
    content_list = content.split("|")
    #one by one element lai dictionary ma lageko to check user ko data cha ki nai
    for i in content_list:
        if i: 
            user_dict_data = json.loads(i) 
            if user_dict_data["name"] == user:
                print(f"Current balance : {user_dict_data["balance"]}")
        else:
            print(f"{user} doesn't have any data to view!")
        
def empty_balance_add(user,deposit):
    balance_dict= {"name":user,"balance":deposit}
    
    write_into_files("balance.txt", balance_dict)
    print(f"Rs{deposit} Balance deposited successfully!!")
    
def add_balance(user):
    try:
        with open("balance.txt") as f:
            content = f.read()
    #file exist garena vane pani write into files le create gari halxa 
    except FileNotFoundError:
        content = ""
        
    deposit = int(input("Enter the deposit amount: "))    
    if content == "":
    
        empty_balance_add(user,deposit)
        
    
    else:   
        content_list = content.split("|")
        user_found = False

        for idx, i in enumerate(content_list):
            if i: 
                user_dict_data = json.loads(i)
                
                # Check if the logged-in user matches
                if user_dict_data["name"] == user:
                    # Update the user's balance
                    user_dict_data["balance"] += deposit
                    user_found = True
                    print(f"Updated balance: Rs{user_dict_data['balance']}")

                    # Update the specific entry in the content list
                    content_list[idx] = json.dumps(user_dict_data)
                    break  # Exit after finding and updating the user

        if not user_found:
            empty_balance_add(user,deposit)
            return
            
            

        # Rebuild the content by joining the updated list
        updated_content = "|".join(content_list)

        # Write the updated content back to the balance file
        
        with open("balance.txt", "w") as f:
            f.write(updated_content)

        print(f"Rs{deposit} Balance deposited successfully!!")
        
def withdraw_balance(user):
    try:
        with open("balance.txt") as f:
            content = f.read()
    #file exist garena vane pani write into files le create gari halxa 
    except FileNotFoundError:
        print("Error!! File not found")
        return
        
    if content == "":
    
        print("There is no any data in the balance file.")
        return
    
    else:   
        withdraw = int(input("Enter the withdraw amount: "))    
        content_list = content.split("|")
        user_found = False

        for idx, i in enumerate(content_list):
            if i: 
                user_dict_data = json.loads(i)
                
                # Check if the logged-in user matches
                if user_dict_data["name"] == user:
                    user_found = True
                    if user_dict_data["balance"]>=withdraw:
                    # Update the user's balance
                        user_dict_data["balance"] -= withdraw
                        print(f"Updated balance: Rs{user_dict_data['balance']}")
                    else:
                        print("Insufficient balance!! Try again.")
                        return

                    # Update the specific entry in the content list
                    content_list[idx] = json.dumps(user_dict_data)
                    break  # Exit after finding and updating the user

        if not user_found:
            print(f"There is no data for user {user}")
            return
            
            

        # Rebuild the content by joining the updated list
        updated_content = "|".join(content_list)

        # Write the updated content back to the balance file
        
        with open("balance.txt", "w") as f:
            f.write(updated_content)

        print(f"Rs{withdraw} withdrawn successfully!!")
              
def main():   
    
    user_choice = input("Do you want to login or register ").lower()          
    if user_choice == "register":  
        register()
    elif user_choice == "login":
        logined, user= login()
        
    else:
        print("You can only login or register here.")

    if logined:
        while True:
            user_choice = input("1.View Balance\n2.Add Balance\n3.Withdraw Balance\n4.q to quit program\nChoose 1/2/3/q ")
            if user_choice == "1":
                view_balance(user)
                
            elif user_choice == "2":
                add_balance(user)
                
            elif user_choice == "3":
                withdraw_balance(user)
                
            elif user_choice == "q":
                break
                
        
            
            
main()