import csv
import math
import random


BENFORD_EXPECTED_PERCENTAGES = {
        "1": 0.301, 
        "2": 0.176, 
        "3": 0.125, 
        "4": 0.097, 
        "5": 0.079, 
        "6": 0.067, 
        "7": 0.058, 
        "8": 0.051, 
        "9": 0.046
}


def readfile(filename):
    def conversion_to_list(file):
        return [row[0] for row in reader if row[0].isdigit()]
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)

        return conversion_to_list(reader)


def calculate_benford_values(data):
    output = []

    def first_digit_frequency(digits_list):
        digits_count = {}
        total_count = 0
        for digit in digits_list:
            if digit == "0":
                continue
            else:
                if digit in digits_count.keys():
                    digits_count[digit] += 1
                else:
                    digits_count[digit] = 1
                total_count += 1
        
        return digits_count, total_count
    
    list_of_first_digit = sorted(list(map(lambda n: str(n)[0], data)))
    frequencies_of_first_digit, total_count = first_digit_frequency(list_of_first_digit)

    def calculate_percentage(count, total):
        return count/total
    
    def calculate_expected_values(digit, total_count):
        return BENFORD_EXPECTED_PERCENTAGES[str(digit)], BENFORD_EXPECTED_PERCENTAGES[str(digit)] * total_count
    

    for num in range(1, 10):
        observed_frequency = frequencies_of_first_digit[str(num)]
        observed_percentage = calculate_percentage(observed_frequency, total_count)

        expected_percentage, expected_frequency = calculate_expected_values(num, total_count)
        
        output.append({
            "digit": num,
            "expected_frequency": expected_frequency,
            "expected_percentage": expected_percentage,
            "observed_frequency": observed_frequency,
            "observed_percentage": observed_percentage
        })

    return output

def test_benford(distribution):
    chi_square_stat = 0
    for digit in distribution:
        chi_square = math.pow((digit["observed_frequency"] - digit["expected_frequency"]), 2)
        chi_square_stat += chi_square

    return chi_square < 15.51

def check_benford(file, random_dist=False):
    if random_dist:
        data_list = [random.randint(1, 1000) for i in range(10000)]
    else:
        data_list = readfile(file)
    
    output = calculate_benford_values(data_list)

    if test_benford(output):
        return test_benford(output), output
    return test_benford(output), None