#-----------------------------------checks--------------------------------------#

def check_binary(num):
    try:
        if int(num) < 0: #if they enter - sign
            raise ValueError
        
        if num[0] == '-': #if they enter -0
            raise ValueError
        
    except ValueError:
        print("- Use SM or 2's Complement to enter negative binary")
        return False
    
    is_binary = True
    for char in num:
        if int(char) not in [0, 1]:
            is_binary = False
    if not is_binary:
        print('- Binary only consists of 0s and 1s')
    return is_binary

def check_denary(num):
    try:
        int(num)
        return True
        
    except ValueError:
        return False
    
def get_denary_sign(num): #checks if denary num neagtive
    if int(num) < 0:
        return True
    else:
        return False
    
def check_hex(num):
    is_hex = True 
    for char in num:
        try:
            int(char)
        except ValueError:
            if char.lower() not in ['a', 'b', 'c', 'd', 'e', 'f']:
                is_hex = False
    if not is_hex:
        print('- Hex only consists of the integer numbers and letters A-F')        
            
    return is_hex

def check_octal(num):
    is_octal = True
    for char in num:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7']:
            is_octal = False
    if not is_octal:
        print('- Octal only consists of numbers 0-7')        
        
    return is_octal        

def check_bcd(num):
    try:
        if int(num) < 0 or num[0] == '-': #if they enter - sign
            print('Program does not support input of negative BCD')
            raise ValueError
        
    except ValueError:
        print('- BCD only consists of 0s and 1s')
        return False
    
    for char in num:
        if int(char) not in [0, 1]:
            print('- BCD only consists of 0s and 1s')
            return False
        
    is_bcd = True
    #check each byte is valid (no greater than denary 9)
    binary_list = list(num)
    binary_list.reverse()
    while len(binary_list) %4 != 0: #then add 0s until makes number a byte long
        binary_list.append('0')
    binary_list.reverse()
    
    bytes_list = []
    temp = ''
    for i, value in enumerate(binary_list, start=1):
        temp += value
        if i %4 == 0:
            bytes_list.append(temp)
            temp = ''
    
    for item in bytes_list:
            if item in ['1010', '1011', '1100', '1101', '1110', '1111']:
                is_bcd = False
    if not is_bcd:
        print('- BCD only consists bytes of max 1001 (= 9 in Denary)')
    return is_bcd
        
#---------------------------------converters-------------------------------#        

def binary2denary(args):
    num, mode = args[0], args[1]
    binary_list = list(num)    
    
    print('[---------------- Working Out ---------------]')
    
    sm_negative = False
    if mode == '1': #SM
        sm_negative = int(binary_list.pop(0)) #removes left most digit and uses it to deccide if its +ve/-ve
        show_binary_working('# Remove sign bit from list and store it', binary_list) #showing working
    
    negative_bit = None
    if mode == '2': #if using 2's complement
        if binary_list[0] == '1': #if MSB is 1 (so its negative)
            negative_bit = len(binary_list) -1 #gets index of whats currently LSB but will be MSB after reverse
        
    binary_list.reverse() #as binary's powers of 2 increase from right to left
    show_binary_working("# Reverse it as binary's powers of 2 increase from right to left", binary_list) #showing working
    
    twos = 1
    display_twos = ''
    denary_num = 0
    #for each value in the iterable give it the value i and run the code in the loop reassigning i & v each time
    print("\n----- Adding each digits value in denary -----\n") #showing working
    for i, value in enumerate(binary_list): #optional arg 'start' changes what i starts as, default = 0
        if int(value): #if the current num is not 0
            if i == negative_bit:
                twos = -1
                display_twos = '*-1'
            num2add = (2**i)* twos
            denary_num += num2add
            display_sign = '+'
            if num2add < 0:
                display_sign = '-'
            print(f"> + (2^ {i}) {display_twos} = {display_sign}{abs(num2add)} ") #showing working
    
    if sm_negative:
        print(f"> = {denary_num} *-1 #as sign bit for SM num was 1") #showing working
        denary_num *= -1

    return denary_num


def denary2binary(args):
    num, mode, negative = args[0], args[1], args[2]
    print('[---------------- Working Out ---------------]')
    if negative:
        num = num[1:] #remove negative sign
        print(num, '> remove negative sign')
        
    binary_list = []
    result, new_result = int(num), int(num) #sets these variable and changes from str --> int
    i = 0 #this is for if they input 1, to make sure it goes through the loop at least once
    #as otherwise int(1/2) = 0 so it never enters loop, resulting in empty list + no working
    while result > 1 or i == 0: #until the number we are dividing < 1
        i += 1
        result = new_result #defines current result for remainder to be found from
        new_result = int(result/2) #half num and round down
        remainder = int(result %2)
        binary_list.append(remainder) #add remainder of this to list
        
        print(f"> {result}/2 = {new_result} r = {remainder} ")
    #here has been converted to positive binary, but is in list and still wrong way round

    #------adding 0s------
    if mode: #if using SM/ 2's (theres other functions dont)
        show_binary_working("#converted to positive binary", binary_list, start_msg='\n>', reversed=True)
        #if MSB (last in list as not reversed yet) number in list is 1
        if binary_list[len(binary_list)-1] == 1: 
        #add a 0 to end of list (binary) so that when u 1 + 2s complement it the MSB is not lost
            binary_list.append(0)
            show_binary_working("#added 0 to end of list so MSB isnt lost during 1's complement", binary_list, reversed=True)
    
    zeros = 0 #a counter for how many 0s added for displaying working
    while len(binary_list) %4 != 0: #then add 0s until makes number a byte long
        binary_list.append(0)
        zeros += 1
    if zeros: #sort flippings; -131
        show_binary_working(f"#added {zeros} zero(s) to make up a byte", binary_list, reversed=True)
        
    if negative:
        if mode == '1': #changes the sign bit if using SM
            binary_list[len(binary_list)-1] = 1
            show_binary_working("#input was -ve, and using SM so changed sign bit to 1", binary_list, reversed=True)
        #converting from pos binary to 2's
        if mode == '2':
            
    #for each value in iterable give it value i & run code in loop along with assigning i & v each time
            for index, item in enumerate(binary_list):
                binary_list[index] = 1-item #inverts 0s and 1s
            
            show_binary_working("#1's complement of the positive binary number", binary_list, reversed=True)
            carry = True #if ones: then do like carry = False
            for index, item in enumerate(binary_list): 
                if carry: #always first loop through as set to True above 
                    #inverts num to 0/1 effectively having added 1 to it but without carrying yet
                    binary_list[index] = 1 -binary_list[index] 
                    if binary_list[index]: #repeat until carry gets added so num would be 1
                        carry = False
            
    binary_list.reverse() #flips it the right way round
    binary_num = list2string(binary_list)
    
    return binary_num

def hex2denary(args):
    num = args[0]
    denary_num = 0
    print('\n[---------------- Working Out ---------------]')
    hex_list = list(num)
    hex_list.reverse() #as hex's powers of 16 increase from right to left

    #for each value in the iterable give it the value i and run the code in the loop reassigning i & v each time
    for i, value in enumerate(hex_list): #optional arg 'start' changes what i starts as, default = 0
        try:
            hex_val = int(value)
        
        except ValueError:
            hex_val = ord(str(value.lower())) -87 #getting ascii value of letter and converting to numerical equivalent
            print(f">   {value} --> {hex_val} ")
        
        num2add = int(hex_val)* (16**i)
        denary_num += num2add
        print(f"> + {hex_val}* (16^ {i}) = +{num2add} ")
    
    return denary_num

def denary2hex(args):
    num = args[0]
    hex_list = []
    print('\n[---------------- Working Out ---------------]')
    new_result = int(num) #sets this variable and changes from str --> int

    while new_result != 0: #until the number we are dividing < 16
        remainder_string = ''
        result = new_result #defines current result for remainder to be found from
        new_result = int(result/16) #num/16 and round down
        remainder = int(result %16) #must add remainder of the division thats just been done
        denary_remainder = remainder
        if remainder > 9:
            remainder = (chr(remainder + 87)).upper() #converts numerical remainder to hex letter
            remainder_string = f"---> {remainder} "
            
        hex_list.append(remainder) 
        
        print(f"> {result}/16 = {new_result} r = {denary_remainder} {remainder_string}")

    hex_list.reverse()
    hex_num = list2string(hex_list)
    return hex_num

def octal2denary(args):
    num = args[0]
    print('\n[---------------- Working Out ---------------]')
    octal_list = list(num)
    octal_list.reverse() #as octals's powers of 2 increase from right to left
    denary_num = 0
    
    #for each value in the iterable give it the value i and run the code in the loop reassigning i & v each time
    for i, value in enumerate(octal_list): #optional arg 'start' changes what i starts as, default = 0
        num2add = int(value)* (8**i)
        denary_num += num2add
        print(f"> + {value}* (8^ {i}) = +{num2add} ")
        
    return denary_num

def denary2octal(args):
    num = args[0]
    print('\n[---------------- Working Out ---------------]')
    octal_list = []
    new_result = int(num) #sets this variable and changes from str --> int

    while new_result != 0: #until the number we are dividing < 8
        result = new_result #defines current result for remainder to be found from
        new_result = int(result/8) #num/8 and round down
        remainder = int(result %8) #must add remainder of the division thats just been done

        octal_list.append(remainder) 
        print(f"> {result}/8 = {new_result} r = {remainder} ")

    octal_list.reverse()
    octal_num = list2string(octal_list)
    return octal_num

def denary2bcd(args):
    num = args[0]
    bcd_list = []
    for i, char in enumerate(num):
        print(f'\n[Digit {i+1}] ', end = '')
        bcd_list.append(denary2binary([int(char), False, None]))
    
    bcd_num = list2string(bcd_list)
    return bcd_num

def bcd2denary_list(num):
    binary_list = list(num)
    binary_list.reverse()
    zeros = 0 #a counter for how many 0s added for displaying working
    while len(binary_list) %4 != 0: #then add 0s until makes number a byte long
        binary_list.append('0')
        zeros += 1
    binary_list.reverse()
    if zeros:
        show_binary_working(f"#added {zeros} zero(s) to make up a byte", binary_list)
    
    denary_list = []
    temp = ''
    #separates into bytes, sends each to function to be converted to denary and adds denary nums to list
    for i, value in enumerate(binary_list, start=1):
        temp += value
        if i %4 == 0:
            print(f'\n[Byte {int(i/4)}] ', end = '')
            denary_list.append(binary2denary([temp, None]))
            temp = ''
    
    return denary_list

def bcd2denary(args):
    num = args[0]
    bcd_list = bcd2denary_list(num)
    denary_num = list2string(bcd_list)
    
    return denary_num
            
    
#---------------------------other functions---------------------------#

def show_binary_working(message, data, old_data = None, start_msg='>', reversed = False):
    if data != old_data:
        display_list = make_bytes(data, reversed)
        print(start_msg, list2string( display_list), message)


#seperates binary digits into bytes with spaces 
def make_bytes(binary_list, reversed=False): #takes and returns list
    new_binary_list = binary_list[:]
    if not reversed:
        new_binary_list.reverse()
    num_spaces = 0
    for i in range(len(new_binary_list)): #loop through whole list
        if i %4 == 0 and i!= 0: #at every 4th digit, but not i = 0
#adding in spaces as we go changes index of later elements
#insert a space at this val of i + num of previous spaces added
            new_binary_list.insert(i + num_spaces, ' ') 
            num_spaces += 1 #increment var
    new_binary_list.reverse()
    return new_binary_list

def list2string(items):
    num = ''.join([str(item) for item in items]) #converts list to string
    return num
    
def remove_space(num):
    array2edit = list(num)
    new_array = []
    for i, item in enumerate(array2edit):
        if item != ' ':
            new_array.append(item)
    num = "".join(new_array)
    return num

def which_binary_mode():
    mode = None
    print('''\nWould you like to use:
1. Sign Magnitude
2. 2's Complement''')
    while mode not in ['1','2']:
        mode = input('\nEnter 1 or 2\n > ')
    
    return mode

def get_mode_msg(mode):
    mode_msg = "[2's]" #defines string to write as message with ans to remind user which type
    if mode == '1':
        mode_msg = "[SM]"
    return mode_msg

def print_results(result, mode, display_base, conversion=None, negative_string=''):
    mode_msg = ''
    if conversion == 'denary2binary':
        mode_msg = get_mode_msg(mode)

    print('\n...')
    print('Result [' + conversions[display_base-1] + ']'+ mode_msg + ' = '+ negative_string + str(result))


def convert_loop(input_base, output_base, mode, conv_str, num2convert):
    args = [num2convert]
    result = None
    
    if input_base == 1: #binary
        args.append(mode)
    
    elif output_base == 1:
        negative = None
        if conv_str == 'denary2binary':
            negative = get_denary_sign(num2convert)
        args.append(mode)
        args.append(negative)
        
    if input_base == 2 or output_base == 2: #if converting to or from denary
        result = eval(conv_str + '(args)')
    
    else: #if not converting directly to or from denary (has 2 steps)
        denary_num = eval(conversions[input_base-1].lower() + '2denary' + '(args)') #gets other base 2denary conversion 
        args[0] = str(denary_num) #changes the num2convert argument to the intermediate denary num
        print(f"\n[{conversions[input_base-1]} {num2convert}] ---> [Denary] {denary_num}]\n")
        result = eval('denary2' + conversions[output_base-1].lower() + '(args)')
        
    if output_base == 1 or output_base == 5:
        result_list = make_bytes(list(result))
        result = list2string(result_list)
    
    return result

#-------------------------------------------MAIN PROGRAM---------------------------------------------------#
# list of menu text
conversions = ['Binary', 'Denary', 'Hex', 'Octal', 'BCD']

#          (choice2,    choice3,                  choice4):
def convert(input_base, output_base, num2convert, mode=None):
    print('\n\n\n\n\n')
    num2convert = remove_space(num2convert) #removes spaces in input
    #checking if input was valid, calling right check function based on input using eval()
    valid = eval('check_' + conversions[input_base-1].lower() + '(num2convert)')
    if not valid:
        return False, False, False
            
    #getting string of conversion chosen e.g binary2denary 
    conversion = conversions[input_base-1].lower() + '2' + conversions[output_base-1].lower()
    result = convert_loop(input_base, output_base, mode, conversion, num2convert)
    print(result)
    print_results(result, mode, output_base, conversion)    
    return True, result, ''

    #-----------------------adding/ subtracting loop-------------------------#
#       choice1, choice2,                          choice4
def add(choice, input_base, first_num, second_num, mode=None):
    print('\n\n\n\n\n')
    first_num = remove_space(first_num) #removes spaces in input
    valid1 = eval('check_' + conversions[input_base-1].lower() + '(first_num)')
    second_num = remove_space(second_num) #removes spaces in input
    valid2 = eval('check_' + conversions[input_base-1].lower() + '(second_num)')
    if not valid1 or not valid2:
        return False, False, False
    
    if input_base != 2: #if not just working in denary do conversions
        conversion = conversions[input_base-1].lower() + '2denary'
        
        first_num = convert_loop(input_base, 2, mode, conversion, first_num)
        second_num = convert_loop(input_base, 2, mode, conversion, second_num)
    
    print('\n1st num [Denary] =', str(first_num))
    print('2nd num [Denary] =', str(second_num))
    
    if choice == 2:  #add/ sub the 2 nums
        denary_result = int(first_num) + int(second_num)
    elif choice == 3:
        denary_result = int(first_num) - int(second_num)

    negative_string = ''
    
    #defining string of conversion from denary answer to base in use e.g denary2hex
    conversion = 'denary2' + conversions[input_base-1].lower() 
    if input_base != 2:
        print('\nResult  [Denary] =', str(denary_result))
        if denary_result < 0 and conversion != 'denary2binary':
            denary_result *= -1
            negative_string = ' [Negative] '
        result = convert_loop(2, input_base, mode, conversion, str(denary_result))
    
    else:
        result = denary_result
    print(negative_string)
    print_results(result, mode, input_base, negative_string= negative_string)
    return True, result, negative_string