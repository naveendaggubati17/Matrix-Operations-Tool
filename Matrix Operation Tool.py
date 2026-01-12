import numpy as np

def input_matrix():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    print(f"Enter {rows} rows of {cols} space-separated numbers:")
    matrix = []
    for i in range(rows):
        row = list(map(float, input().split()))
        if len(row) != cols:
            raise ValueError("Invalid row length")
        matrix.append(row)
    return np.array(matrix)

def display_matrix(name, mat):
    np.set_printoptions(precision=2, suppress=True, linewidth=100)
    print(f"\n{name}:")
    print(mat)

def main():
    print("Matrix Operations Tool")
    print("1. Addition\n2. Subtraction\n3. Multiplication\n4. Transpose\n5. Determinant")
    choice = input("Choose operation (1-5): ")
    
    if choice in ['1', '2', '3']:
        print("Enter Matrix A:")
        A = input_matrix()
        print("Enter Matrix B:")
        B = input_matrix()
        
        if choice == '1':
            if A.shape != B.shape:
                print("Error: Matrices must have same dimensions for addition")
                return
            result = A + B
            display_matrix("A + B", result)
        elif choice == '2':
            if A.shape != B.shape:
                print("Error: Matrices must have same dimensions for subtraction")
                return
            result = A - B
            display_matrix("A - B", result)
        else:  # Multiplication
            if A.shape[1] != B.shape[0]:
                print("Error: Invalid dimensions for multiplication")
                return
            result = np.dot(A, B)
            display_matrix("A x B", result)
    
    elif choice == '4':
        print("Enter Matrix:")
        mat = input_matrix()
        result = np.transpose(mat)
        display_matrix("Transpose", result)
    
    elif choice == '5':
        print("Enter square Matrix:")
        mat = input_matrix()
        if mat.shape[0] != mat.shape[1]:
            print("Error: Matrix must be square for determinant")
            return
        result = np.linalg.det(mat)
        print(f"Determinant: {result:.2f}")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    while True:
        main()
        if input("\nAnother operation? (y/n): ").lower() != 'y':
            break
    np.set_printoptions()  # Reset
