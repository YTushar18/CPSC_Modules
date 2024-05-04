#write a program that sorts phonebook

def stripFormatiing(number):
    """Remove formaatiing charachter from a phone number """
    return ''.join(filter(str.isdigit,number))

def padWithZeros(number, length):
    """PAd the umber with leading zeroes to match the specified length"""
    return number.zfill(length)

def findMaxLength(numbers):
    """Find the max number of leght in the list"""
    return max(len(number) for number in numbers)

def countingSortByDigit(numbers, digitPosition, radix=10):
    """Sort the numbers based on the digits at the specified position"""
    output = [0] * len(numbers)
    count = [0] * radix

    # we can count the occurances of each difit at DigitPosition
    for number in numbers:
        index = int(number[digitPosition]) if digitPosition < len(number) else 0
        count[index] += 1

    #counted values accumulation
    for i in range(1,radix):
        count[i] += count[i-1]
    
    # build the output array
    for number in reversed(numbers):
        index = int(number[digitPosition]) if digitPosition < len(number) else 0
        output[count[index] -1] = number
        count[index] -= 1

    return output

def radixSort(numbers):
    """Sort the numbers using Radix Sort"""

    maxLength = findMaxLength(numbers)

    for digitPosition in range(maxLength -1,-1,-1):
        numbers = countingSortByDigit(numbers, digitPosition)
    return numbers

def preProcessPhoneNumbers(phoneNumbers):
    """Pre processing list of phone numbers by standardizing their formats"""
    stadardizedNumbers = [stripFormatiing(number) for number in phoneNumbers]
    maxLength = findMaxLength(stadardizedNumbers)
    return [padWithZeros(number, maxLength) for number in stadardizedNumbers]


def main():
    n = int(input("Enter the number of phone numbers:"))
    rawPhoneNumbers = [input(f"Enter phone number {i+1}: ") for i in range(n)]

    #Preprocessing on raw numbers
    stadardizedNumbers = preProcessPhoneNumbers(rawPhoneNumbers)

    #sorting of the raw numbers (pre processed)

    sortedNumbers = radixSort(stadardizedNumbers)

    # display sorted numbers
    print("\n Sorted Phone Numbers")
    for number in sortedNumbers:
        print(number)

if __name__ == "__main__":
    main()

