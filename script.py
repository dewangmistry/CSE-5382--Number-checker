#!/usr/bin/python3
import sys
import re
import api
from tabulate import tabulate
import logging
import os

logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s', level=logging.DEBUG, filename="audit_logs.log")

""" Function to validate name using regular expressions
    Arguments:
        name (str): Name to be validated
"""
def validateName(name):
    return_dict = {}
    return_dict['status_code'] = 1
    return_dict['first_name'] = ""
    return_dict['middle_name'] = ""
    return_dict['last_name'] = ""
    return_dict['msg'] = ""
    try:
        # <first>
        if re.compile(r"^[a-z]+$", re.IGNORECASE).fullmatch(name):
            return_dict['first_name'] = name
            return_dict['status_code'] = 0
        # <first middle last>, <first last>, <first MI last>
        elif re.compile(r"^([a-z]+)( [a-z]+| [a-z]{1}.)?( [a-z]+('?[a-z]+-?[a-z]+|-?[a-z]+'?)[a-z]+)$", re.IGNORECASE).fullmatch(name):
            name = name.split(" ")
            return_dict['first_name'] = name[0]
            if len(name) == 3:
                return_dict['middle_name'] = name[1]
                return_dict['last_name'] = name[2]
            else:
                return_dict['last_name'] = name[1]
            return_dict['status_code'] = 0
        # <last, first MI>, <last, first>, <last, first middle>
        elif re.compile(r"^([a-z]+('?[a-z]+-?|-?[a-z]+'?)[a-z]+)(, [a-z]+( [a-z]+| [a-z]{1}.)?)$", re.IGNORECASE).fullmatch(name):
            return_dict['last_name'], first_name = name.split(",")
            initial_name = first_name.lstrip().split(" ")
            if len(initial_name) == 2:
                return_dict['first_name'], return_dict['middle_name'] = initial_name[0], initial_name[1]
            else:
                return_dict['first_name'] = initial_name[0]
            return_dict['status_code'] = 0
        else:
            return_dict['msg'] = "Invalid name format"
    except:
        return_dict['msg'] = "Error occured"
    finally:
        return return_dict

""" Function to validate phone number using regular expressions
    Arguments:
        phone_number: Phone number to validate
"""
def validateNumber(phone_number):
    return_dict = {}
    return_dict['status_code'] = 1
    return_dict['phone_number'] = phone_number
    return_dict['msg'] = ""
    try:
        # 123-4567, (670)123-4567, 670-123-4567, 1-670-123-4567, 1(670)123-4567
        if re.compile(r"^([+]?(1|1[ ]?))?([(]\d{3}[)]|-\d{3}-|\d{3}-?)?(\d{3}-\d{4})$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # 1 670 123 4567, 670 123 4567
        elif re.compile(r"^([+]?(1|1[ ]?))?\d{3}[ ]\d{3}[ ]\d{4}$").fullmatch(phone_number):    
            return_dict['status_code'] = 0
        # 670.123.4567, 1.670.123.4567
        elif re.compile(r"^([+]?(1|1.?))?\d{3}[.]\d{3}[.]\d{4}$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # 12345
        elif re.compile(r"^[0-9]{5}$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # 011 701 111 1234, 011 1 703 111 1234
        elif re.compile(r"^((011|00)[ ])(1[ ])?\d{3}[ ]\d{3}[ ]\d{4}$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # 12345.12345, 12345 12345
        elif re.compile(r"^[0-9]{5}[.| ][0-9]{5}$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # Danish phone numbers in groups of 2: +45 11 22 33 44, +45 11.22.33.44
        elif re.compile(r"^([+]?45)?[ ]?(\d{2}[.]\d{2}[.]\d{2}[.]\d{2}|\d{2}[ ]\d{2}[ ]\d{2}[ ]\d{2})$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # Danish phone numbers in groups of 4: +45 1122 3344, +45 1122.3344
        elif re.compile(r"^([+]?45)?[ ]?(\d{4}[.| ]\d{4})$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        # +32 (21) 212-2324
        elif re.compile(r"^[+]?[2-9]{1}\d?\d?[ ]?([(]\d{2}\d?[)]|\d{2}\d?)[ ]?\d{3}-\d{4}$").fullmatch(phone_number):
            return_dict['status_code'] = 0
        else:
            return_dict['msg'] = "Invalid phone number format"
    except Exception as e:
        return_dict['msg'] = "Error occured"
    finally:
        return return_dict

""" Main function. Execution starts from here
"""
if __name__ == "__main__":
    d = api.DBApi()                         # API object
    args_len = len(sys.argv)
    if args_len < 2:
        print("Enter valid choice from ADD, DEL, LIST")
        print("ADD “<Person>” “<Telephone #>” - Add a new person to the database")
        print("DEL “<Person>”       - Remove someone from the database by name")
        print("DEL “<Telephone #>”  - Remove someone by telephone #")
        print("LIST")
    else:
        if sys.argv[1] != '':
            if sys.argv[1] == 'ADD':
                if args_len == 4:
                    name = sys.argv[2]
                    phone_number = sys.argv[3]
                    name_status = validateName(name)
                    number_status = validateNumber(phone_number)
                    
                    if name_status['status_code'] == 0 and number_status['status_code'] == 0:
                        return_code = d.insert_user(name, phone_number)
                        logging.debug(str(os.getuid()) + " ADD: " + name + " " + str(phone_number))
                        print(0)
                    elif name_status['status_code'] == 0 and number_status['status_code'] == 1:
                        print(1)
                        print(number_status['msg'])
                    elif name_status['status_code'] == 1 and number_status['status_code'] == 0:
                        print(1)
                        print(name_status['msg'])
                    else:
                        print(1)
                        print(name_status['msg'])
                        print(number_status['msg'])
                else:
                    print("Help Section")
                    print("ADD “<Person>” “<Telephone #>” - Add a new person to the database")
            elif sys.argv[1] == 'DEL':
                if args_len == 3:
                    param = sys.argv[2]
                    if re.compile(r"^[a-z]", re.IGNORECASE).findall(sys.argv[2]):
                        status = validateName(sys.argv[2])
                        if status['status_code'] == 0:
                            return_code = d.delete_by_name(sys.argv[2])
                            if return_code == True:
                                logging.debug(str(os.getuid()) + " DEL: " + sys.argv[2])
                                print(0)
                            else:
                                print(1)
                                print("No user found")
                        else:
                            print(1)
                            print("Invalid Name format")
                    else:
                        status = validateNumber(sys.argv[2])
                        if status['status_code'] == 0:
                            return_code = d.delete_by_number(sys.argv[2])
                            if return_code == True:
                                logging.debug(str(os.getuid()) + " DEL: " + sys.argv[2])
                                print(0)
                            else:
                                print(1)
                                print("No user found")
                        else:
                            print("Invalid Number format")
                else:
                    print("Help Section")
                    print("DEL “<Person>”       - Remove someone from the database by name")
                    print("DEL “<Telephone #>”  - Remove someone by telephone #")
            elif sys.argv[1] == 'LIST':
                data = d.get_users()
                if data:
                    logging.debug(str(os.getuid()) + " LIST")
                    print(tabulate(data, headers=['Name', 'Phone Number']))
            else:
                print("Invalid choice")
        else:
            print("Enter an option to perform")