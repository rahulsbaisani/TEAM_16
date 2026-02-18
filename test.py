numbers = []

# Take 5 numbers from user
for i in range(5):
    num = int(input("Enter a number: "))
    numbers.append(num)

# Find the largest number
largest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num

# Print result
print("The numbers are:", numbers)
print("The largest number is:", largest)
