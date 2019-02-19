# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
win.geometry('440x640')# Set window size here to '440x640' pixels
win.title('FedUni Banking')# Set window title here to 'FedUni Banking'

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, textvariable=pin_number_var, state='normal')
account_pin_entry.config(show="*") #modified for *

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    global pin_number_var
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    if event.widget.cget("text")=='Cancel/Clear':
        pin_number_var.set('')

def handle_pin_button(event):
    global pin_number_var
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''    
    # Limit to 4 chars in length

    if len(str(pin_number_var.get()))==4:
        return
    
    # Set the new pin number on the pin_number_var
    if event.widget.cget("text")=='0':

        pin_number_var.set(pin_number_var.get()+'0')

    elif event.widget.cget("text")=='1':

        pin_number_var.set(pin_number_var.get()+'1')

    elif event.widget.cget("text")=='2':

        pin_number_var.set(pin_number_var.get()+'2')

    elif event.widget.cget("text")=='3':

        pin_number_var.set(pin_number_var.get()+'3')

    elif event.widget.cget("text")=='4':

        pin_number_var.set(pin_number_var.get()+'4')

    elif event.widget.cget("text")=='5':

        pin_number_var.set(pin_number_var.get()+'5')

    elif event.widget.cget("text")=='6':

        pin_number_var.set(pin_number_var.get()+'6')

    elif event.widget.cget("text")=='7':

        pin_number_var.set(pin_number_var.get()+'7')

    elif event.widget.cget("text")=='8':

        pin_number_var.set(pin_number_var.get()+'8')

    elif event.widget.cget("text")=='9':

        pin_number_var.set(pin_number_var.get()+'9')

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_number_var
    # Create the filename from the entered account number with '.txt' on the end
    filename=str(account_number_var.get())+'.txt'

    # Try to open the account file for reading
    
    try:
        # Open the account file for reading
        fopen = open(filename,'r')

        # First line is account number
        
        account.account_number = int(fopen.readline())

        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read 
        
        account.pin_number = int(fopen.readline())
        
        assert int(pin_number_var.get())==account.pin_number

        # Read third and fourth lines (balance and interest rate) 
        
        account.balance = float(fopen.readline())
        account.interest_rate = float(fopen.readline())
        
        
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        while True:
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list
            transac_list=[]
            check=fopen.readline()
            if check=='':
                break
            transac_list.append(check)
            transac_list.append(float(fopen.readline()))
            account.transaction_list.append(tuple(transac_list))

        # Close the file now we're finished with it
        fopen.close()
     
         # Catch exception if we couldn't open the file or PIN entered did not match account PIN    
    except FileNotFoundError:
    
        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror("Error","Invalid account number - please try again!")
        
        account = BankAccount() # account  balance wiil call here

        #  ...also clear PIN entry and change focus to account number entry
        
        pin_number_var.set('')
        account_number_var.set('')
        
        return
    except AssertionError:
        messagebox.showerror("Error","Wrong PIN entered!")
        account = BankAccount()
        pin_number_var.set('')
        account_number_var.set('')
        return

    except ValueError:
        messagebox.showerror("Error","Enter some pin!")
        account = BankAccount()
        pin_number_var.set('')
        account_number_var.set('')
        return
        # return the value here

    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    
    remove_all_widgets()
    create_account_screen()
    

# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    
    account.save_to_file()
    
    # Reset the bank acount object
    
    account=BankAccount()

    # Reset the account number and pin to blank
    
    
    pin_number_var.set('')
    account_number_var.set('')

    # Remove all widgets and display the login screen again
    
    remove_all_widgets()
    create_login_screen()
    

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var
    # Try to increase the account balance and append the deposit to the account file    
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        amountDep = float(amount_entry.get())
    
            # Deposit funds
        account.balance = account.balance + amountDep
            
            # Update the transaction widget with the new transaction by calling account.get_transaction_string()
            # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
            #       contents, and finally configure back to state='disabled' so it cannot be user edited.
            
        account.transaction_list.append(("Deposit\n",float(amount_entry.get())))
        transaction_text_widget.configure(state='normal')
        transaction_text_widget.delete('1.0', 'end')
        transaction_text_widget.insert('insert',account.get_transaction_string())
        transaction_text_widget.configure(state='disabled')
    
            # Change the balance label to reflect the new balance
            
        balance_var.set("Balance: $"+str(account.balance))
    
            # Clear the amount entry
            
        amount_entry.delete(0, 'end')
    
            # Update the interest graph with our new balance
        
        plot_interest_graph()

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except ValueError as err:
        messagebox.showerror("Transaction Error!",err)
        
          
def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account    
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method
        
        amountWdrw = float(amount_entry.get())
        
        # Withdraw funds 
        
        assert account.balance > amountWdrw
        
        account.balance = account.balance - amountWdrw       

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        
        account.transaction_list.append(("Withdrawal\n",float(amount_entry.get())))
        transaction_text_widget.configure(state='normal')
        transaction_text_widget.delete('1.0', 'end')
        transaction_text_widget.insert('insert',account.get_transaction_string())
        transaction_text_widget.configure(state='disabled')

        # Change the balance label to reflect the new balance
        
        balance_var.set("Balance: $"+str(account.balance))        
        
        # Clear the amount entry
        amount_entry.delete(0, 'end')

        # Update the interest graph with our new balance
        
        plot_interest_graph()

    # Catch and display any returned exception as a messagebox 'showerror'
    except ValueError as err:
        messagebox.showerror("Transaction Error!",err)
    except AssertionError:
        messagebox.showerror("Error","The bank does not allow overdraft!")
        amount_entry.delete(0, 'end')

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    global account
    '''Function to plot the cumulative interest for the next 12 months here.'''
    x=[]
    y=[]
    # YOUR CODE to generate the x and y lists here which will be plotted
    
    
    interest=1+((account.interest_rate)/12)
    
    for i in range(1,13):
        x.append(i)
    
    y.append(account.balance)
    
    for j in range(1,12):
        y.append(y[j-1]*interest)
    
    
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=90)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='n')


# ---------- UI Screen Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    
    # ----- Row 0 -----

    # 'FedUni Banking' label here. Font size is 32.
    
    banklabel = tk.Label(win,text="FedUni Banking",font=('Ariel','32'),anchor='ne')
    banklabel.grid(row=0,column=0,columnspan=3,padx=63,pady=10)

    # ----- Row 1 -----

    # Acount Number / Pin label here
    accLabel = tk.Label(win,text="Account Number/PIN:")
    accLabel.grid(row=1,column=0,padx=10,pady=10)

    # Account number entry here

    account_number_entry.grid(row=1,column=1,sticky="N"+"S"+"E"+"W")
    
    # Account pin entry here
    
    account_pin_entry.grid(row=1,column=2,sticky="N"+"S"+"E"+"W")

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b1 = tk.Button(win, text ="1")
    b1.grid(row=2,column=0,sticky="N"+"S"+"E"+"W")
    b1.bind("<Button-1>",handle_pin_button)
    b2 = tk.Button(win, text ="2")
    b2.grid(row=2,column=1,sticky="N"+"S"+"E"+"W")
    b2.bind("<Button-1>",handle_pin_button)
    b3 = tk.Button(win, text ="3")
    b3.grid(row=2,column=2,sticky="N"+"S"+"E"+"W")
    b3.bind("<Button-1>",handle_pin_button)
    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    
    b4 = tk.Button(win, text ="4")
    b4.grid(row=3,column=0,sticky="N"+"S"+"E"+"W")
    b4.bind("<Button-1>",handle_pin_button)
    b5 = tk.Button(win, text ="5")
    b5.grid(row=3,column=1,sticky="N"+"S"+"E"+"W")
    b5.bind("<Button-1>",handle_pin_button)
    b6 = tk.Button(win, text ="6")
    b6.grid(row=3,column=2,sticky="N"+"S"+"E"+"W")
    b6.bind("<Button-1>",handle_pin_button)

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    b7 = tk.Button(win, text ="7")
    b7.grid(row=4,column=0,sticky="N"+"S"+"E"+"W")
    b7.bind("<Button-1>",handle_pin_button)
    b8 = tk.Button(win, text ="8")
    b8.grid(row=4,column=1,sticky="N"+"S"+"E"+"W")
    b8.bind("<Button-1>",handle_pin_button)
    b9 = tk.Button(win, text ="9")
    b9.grid(row=4,column=2,sticky="N"+"S"+"E"+"W")
    b9.bind("<Button-1>",handle_pin_button)
    

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    
    bclear = tk.Button(win, text ="Cancel/Clear",bg='red',activebackground='red')
    bclear.grid(row=5,column=0,sticky="N"+"S"+"E"+"W")
    bclear.bind("<Button-1>",clear_pin_entry)
    
    # Button 0 here
    
    b0 = tk.Button(win, text ="0")
    b0.grid(row=5,column=1,sticky="N"+"S"+"E"+"W")   
    b0.bind("<Button-1>",handle_pin_button)
    
    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    
    blogin = tk.Button(win, text ="Login",bg='green',activebackground='green')
    blogin.grid(row=5,column=2,sticky="N"+"S"+"E"+"W")
    blogin.bind("<Button-1>",log_in)

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(2,weight=1)
    win.rowconfigure(3,weight=1)
    win.rowconfigure(4,weight=1)
    win.rowconfigure(5,weight=1)

def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    global account
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    banklabel = tk.Label(win,text="FedUni Banking",font=('Ariel','24'),anchor='ne')
    banklabel.grid(row=0,column=0,columnspan=4,padx=105,pady=10)
    

    # ----- Row 1 -----

    # Account number label here
    
    accNum = ("Account Number: " + str(account.account_number))
    accLabel = tk.Label(win,text=accNum)
    accLabel.grid(row=1,column=0,padx=10,pady=10)

    # Balance label here
    
    balance_var.set("Balance: $" + str(account.balance))
    balance_label.grid(row=1,column=1,padx=10,pady=10)

    # Log out button here
    
    blogout = tk.Button(win, text ="Logout", command = save_and_log_out)
    blogout.grid(row=1,column=2,sticky="N"+"S"+"E"+"W",columnspan=2)
    #blogin.bind("<Button-1>",log_in)

    # ----- Row 2 -----

    # Amount label here

    amount_label = tk.Label(win,text="Amount ($)")
    amount_label.grid(row=2,column=0,padx=10)

    # Amount entry here
    
    amount_entry.grid(row=2,column=1,sticky="N"+"S"+"E"+"W")

    # Deposit button here
    
    bdeposit = tk.Button(win, text ="Deposit",command=perform_deposit)
    bdeposit.grid(row=2,column=2,sticky="N"+"S"+"E"+"W")

    # Withdraw button here
    
    bwdraw = tk.Button(win, text ="Withdraw",command=perform_withdrawal)
    bwdraw.grid(row=2,column=3,sticky="N"+"S"+"E"+"W")
    
    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    
    text_scrollbar = tk.Scrollbar(win)
    
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    
    transaction_text_widget.grid(row=3,column=0,columnspan=4,sticky="N"+"S"+"E"+"W")
    transaction_text_widget.configure(wrap='word', yscrollcommand=text_scrollbar.set, state='disabled')
    
    
    transaction_text_widget.insert('insert',account.get_transaction_string())
    
    transaction_text_widget.configure(state='disabled')
    
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited

    # Now add the scrollbar and set it to change with the yview of the text widget
    text_scrollbar.grid(row=3,column=3,sticky="S"+"N"+"E")
    text_scrollbar.config(command=transaction_text_widget.yview)


    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()
    

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    
    win.rowconfigure(3,weight=1)
    
    

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
#create_account_screen()
win.mainloop()
