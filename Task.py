from functools import wraps

from collections import UserDict
from datetime import datetime, date, timedelta
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено









class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, name):
        super().__init__(name)
        #  self.name = name
    def __str__(self):
        return str(self.value)
		



class NumberTooShortError(Exception):
    def __init__(self, message="Number is too short"):
        self.message = message
        super().__init__(self.message)

class NumberStartsFromLowError(Exception):
    def __init__(self, message="Number is too long"):
        self.message = message
        super().__init__(self.message)



class Phone(Field):
    # реалізація класу
   def __init__(self, number) : 
     super().__init__(number) 
     if len(number) < 10:
        raise NumberTooShortError
     elif len(number) > 10:
        raise NumberStartsFromLowError
     else:
        self.number = number
   def __str__(self):
        return str(self.value)
   def __repr__(self):
        return str(self)
		
class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        try:
            self.birthday=datetime.strptime(birthday,"%d.%m.%Y")
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self):
        return str(self.value)    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    # реалізація класу
    def add_phone(self,number: str):
        self.phones.append(Phone(number))

    def remove_phone(self,phone_number:str):
       
         self.phone = [phone for phone in self.phones if self.phone != phone_number]
             


    def edit_phone(self, number:str,new_number:str): 
       for phone in self.phones:
           if phone.value == number:
               self.phones.remove(phone)
               break
       new_phone = Phone(new_number)
       self.phones.append(new_phone)
       

    def find_phone(self,number):
        for phone in self.phones:
           if phone.value == number:
               return phone 


    def add_birthday(self,birthday:str):
        self.birthday=Birthday(birthday)




    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    def __repr__(self):
        return str(self) 
    

class AddressBook(UserDict):
     def __init__(self):
        self.data = dict()

     def add_record(self,record):
       self.data[record.name.value] = record

     def find(self,name):
       record = self.data.get(name)
       return record
       
     def delete(self,name):
       del self.data[name]
  

     def get_upcoming_birthdays(self):
        birthdays = dict()
        for name, user in self.data.items():
         birthday=datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
         today = datetime.today().date()
         birthday_this_year=birthday.replace(year=today.year)
         birthdays.update({name:birthday})
        if birthday_this_year<today:
         birthdays[name]=birthday_this_year+timedelta(days=365)
        elif birthday.weekday()==5:
         birthdays[name]=birthday_this_year+timedelta(days=2)
        elif birthday.weekday()==6:
         birthdays[name]=birthday_this_year+timedelta(days=1)
        else:
         birthdays[name]=birthday_this_year
    
        return birthdays
     











































def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner



def phone_error(func):
    @wraps(func)
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name of contact please."

    return inner


def change_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Please input right contact."

    return inner

def birthday_error(func):
    @wraps(func)
    def inner(args, book:AddressBook):
       try:
         name, birthday= args
         birthday = datetime.strptime(birthday,"%d.%m.%Y")
         return func(args, book)
         
       except ValueError:
            return ValueError("Invalid date format. Use DD.MM.YYYY")

    return inner


@birthday_error
def add2_birthday(args, book: AddressBook):
       # self.birthday=Birthday(birthday)
    #    name, birthday, *_ = args
    #    book.update({name : birthday})
    #    return Birthday(birthday)
       name, birthday = args
       record = book.find(name)
       message = "Contact updated."
       if record is None:
          record = Record(name)
          book.add_record(record)
          message = "Birthday added."
       if birthday:
        record.add_birthday(birthday)
       return message

# @input_errora
# def add_contact(args, contacts):
#     name, phone = args
#     contacts.update({name : phone})
   
#     return "Contact added."


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message




@change_error
def change_contact(args, book:AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record:
        record = Record(name)
        record.add_phone(phone)
        book.update({name : record})
    # book.update({Record(name) : phone})
    return "Contact updated."

@phone_error
def show_phone(args,book:AddressBook): 
     #name, = args
    name=args[0]
    res = book.get(name)
    return res.phones
    

def show_birthday(args,book:AddressBook):
     #name, = args
    name=args[0]
    res = book.get(name)
    return res.birthday



def show_all(book:AddressBook):
    return book



def birthdays2(book:AddressBook):
     
     birthdays = dict()
     for name, user in book.items():
      birthday=datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
      today = datetime.today().date()
      birthday_this_year=birthday.replace(year=today.year)
      birthdays.update({name:birthday})
     if birthday_this_year<today:
      birthdays[name]=birthday_this_year+timedelta(days=365)
     elif birthday.weekday()==5:
      birthdays[name]=birthday_this_year+timedelta(days=2)
     elif birthday.weekday()==6:
      birthdays[name]=birthday_this_year+timedelta(days=1)
     else:
      birthdays[name]=birthday_this_year
     return birthdays







def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
                print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "add-birthday":
            print(add2_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book)) 
        elif command == "birthdays":
            print(birthdays2(book))       
        elif command == "all":
            print(show_all(book))    
        else:
            print("Invalid command.")
    save_data(book)           

if __name__ == "__main__":
    main()



