class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = 0
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        # Transcation list  
        self.transaction_list = []
        

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            self.balance = self.balance + float(amount)
        except ValueError:
            return ("'{}' is not a float!".format(amount))
        self.transaction_list.append(("Deposit",amount))
        
        

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            self.balance = self.balance - float(amount)
        except ValueError:
            return ("'{}' is not a float!".format(amount))
        try:
            assert amount>self.balance
        except AssertionError:
            return ("You don't have enough balance in your account! Your balance is "+self.balance)
        self.transaction_list.append(("Withdrawal",amount))
        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        testStr=''
        for i in range(len(self.transaction_list)):
            testStr=testStr+(self.transaction_list[i][0]+str(self.transaction_list[i][1])+"\n")
        return testStr

    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        info=open(str(self.account_number)+".txt",'w')
        info.write(str(self.account_number)+"\n"+str(self.pin_number)+"\n"+str(self.balance)+"\n"+str(self.interest_rate)+"\n")
        info.close()
        inf=open(str(self.account_number)+".txt",'a')
        inf.write(self.get_transaction_string())
        inf.close()
