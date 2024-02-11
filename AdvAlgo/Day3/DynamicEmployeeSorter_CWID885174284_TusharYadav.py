
# Employee Class
class Employee:
    def __init__(self, id, name, salary) -> None:
        self.id = id
        self.name = name
        self.salary = salary
    
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.salary})"
    
def insertion_sort( arr, key=lambda x:x):
    for i in range(1, len(arr)):
        key_value = arr[i]
        j = i-1
        while j>=0 and key(arr[j]) > key(key_value):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key_value
    
def merge_sort( arr, key=lambda x:x):
    if len(arr) > 1:
        mid = len(arr)//2
        L,R = arr[:mid], arr[mid:]

        merge_sort(L,key)
        merge_sort(R,key)

        i = j = k = 0
        while i < len(L) and j<len(R):
            if key(L[i]) < key(R[j]):
                arr[k] = L[i]
                i += 1
            
            else:
                arr[k] = R[j]
                j +=1
            k +=1

            while i <len(L):
                arr[k]=L[i]
                i +=1
                k+=1
            
            while j<len(R):
                arr[k] = R[j]
                j += 1
                k+=1
    
def quick_sort(arr, key=lambda x: x):
    if len(arr) <=1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if key(x) <= key(pivot)]
        greater = [x for x in arr[1:] if key(x) > key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

def create_employee_list():
    employee_list = []
    n = int(input("Enter Number of Employees: "))
    for _ in range(n):
        id = input("Enter Employee ID: ")
        name = input("Enter Employee Name: ")
        salary = float(input("Enter Employee Salary: "))
        employee_list.append(Employee(id,name,salary))
    
    return employee_list

def sort_and_display_empoyees(employee_list):
    while True:
        print("\n Choose Sorting Algorithm: \n 1.Insertion Sort \n 2. Merge Sort \n 3. Quick Sort \n 4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            sorting_algorithm = insertion_sort
        elif choice == '2':
            sorting_algorithm = merge_sort
        elif choice == '3':
            def quick_sort_wrapper(arr, key=lambda x: x):
                sorted_arr = quick_sort(arr, key)
            
            sorting_algorithm = quick_sort_wrapper
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid Entry, Please select a valid option!")
            continue

        key_func = lambda employee:employee.salary
        sorting_algorithm(employee_list, key = key_func)

        print("Sorted Employee:")
        for employee in employee_list:
            print(employee)
        
def main():
    employee_list = create_employee_list()
    sort_and_display_empoyees(employee_list)

if __name__ == "__main__":
    main()
        
            
                   

