import os
import torch
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "Salesforce/codet5-base")
DEVICE = torch.device("cpu")

print(f"[model] Loading mock model (lightweight mode) ...")
print(f"[model] Mock model ready.")


def generate_code(prompt: str, max_new_tokens: int = 256) -> str:
    p = prompt.lower()

    # ── HELLO WORLD ───────────────────────────────────────────
    if "hello" in p and "world" in p:
        if "c++" in p or "cpp" in p:
            return """#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}"""
        elif "java" in p:
            return """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}"""
        elif "c" in p:
            return """#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}"""
        else:
            return """print("Hello, World!")"""

    # ── EVEN OR ODD ───────────────────────────────────────────
    if ("even" in p and "odd" in p) or "even or odd" in p or "odd or even" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter a number: ";
    cin >> n;
    if (n % 2 == 0)
        cout << n << " is Even" << endl;
    else
        cout << n << " is Odd" << endl;
    return 0;
}"""
        elif "java" in p:
            return """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n % 2 == 0 ? "Even" : "Odd");
    }
}"""
        else:
            return """n = int(input("Enter a number: "))
if n % 2 == 0:
    print(f"{n} is Even")
else:
    print(f"{n} is Odd")"""

    # ── SWAP ──────────────────────────────────────────────────
    if "swap" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int main() {
    int a = 5, b = 10;
    cout << "Before swap: a=" << a << " b=" << b << endl;
    swap(a, b);
    cout << "After swap: a=" << a << " b=" << b << endl;
    return 0;
}"""
        elif "java" in p:
            return """public class Main {
    public static void main(String[] args) {
        int a = 5, b = 10;
        System.out.println("Before: a=" + a + " b=" + b);
        int temp = a; a = b; b = temp;
        System.out.println("After: a=" + a + " b=" + b);
    }
}"""
        else:
            return """a = 5
b = 10
print(f"Before: a={a}, b={b}")
a, b = b, a
print(f"After: a={a}, b={b}")"""

    # ── REVERSE ───────────────────────────────────────────────
    if "reverse" in p and "array" in p:
        if "c++" in p or "cpp" in p:
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {1, 2, 3, 4, 5};
    reverse(arr.begin(), arr.end());
    for (int x : arr) cout << x << " ";
    return 0;
}"""
        elif "java" in p:
            return """import java.util.Arrays;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        Integer[] arr = {1, 2, 3, 4, 5};
        Collections.reverse(Arrays.asList(arr));
        System.out.println(Arrays.toString(arr));
    }
}"""
        else:
            return """def reverse_array(arr):
    return arr[::-1]

result = reverse_array([1, 2, 3, 4, 5])
print(result)"""

    if "reverse" in p and ("string" in p or "str" in p):
        if "c++" in p:
            return """#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    string s = "hello";
    reverse(s.begin(), s.end());
    cout << s << endl;
    return 0;
}"""
        else:
            return """def reverse_string(s):
    return s[::-1]

print(reverse_string("hello"))"""

    if "reverse" in p and ("number" in p or "num" in p or "integer" in p):
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int reverseNumber(int n) {
    int rev = 0;
    while (n > 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return rev;
}

int main() {
    cout << reverseNumber(12345) << endl;
    return 0;
}"""
        else:
            return """def reverse_number(n):
    return int(str(n)[::-1])

print(reverse_number(12345))"""

    # ── SUM OF ARRAY ──────────────────────────────────────────
    if "sum" in p and ("array" in p or "list" in p):
        if "c++" in p:
            return """#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int x : arr) sum += x;
    cout << "Sum: " << sum << endl;
    return 0;
}"""
        else:
            return """arr = [1, 2, 3, 4, 5]
print(f"Sum: {sum(arr)}")"""

    # ── MAX / MIN ─────────────────────────────────────────────
    if ("maximum" in p or "max" in p or "largest" in p) and ("array" in p or "list" in p):
        if "c++" in p:
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Max: " << *max_element(arr.begin(), arr.end()) << endl;
    return 0;
}"""
        else:
            return """arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Max: {max(arr)}")"""

    if ("minimum" in p or "min" in p or "smallest" in p) and ("array" in p or "list" in p):
        if "c++" in p:
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Min: " << *min_element(arr.begin(), arr.end()) << endl;
    return 0;
}"""
        else:
            return """arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Min: {min(arr)}")"""

    # ── CREATE / INITIALIZE ARRAY ─────────────────────────────
    if ("create" in p or "initialize" in p or "declare" in p) and ("array" in p or "list" in p):
        if "c++" in p:
            return """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    vector<int> v = {10, 20, 30, 40, 50};
    for (int x : v) cout << x << " ";
    return 0;
}"""
        elif "java" in p:
            return """public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        for (int x : arr)
            System.out.print(x + " ");
    }
}"""
        else:
            return """arr = [1, 2, 3, 4, 5]
arr2 = list(range(1, 6))
print(arr)
print(arr2)"""

    # ── PRINT ARRAY ───────────────────────────────────────────
    if ("print" in p or "display" in p) and ("array" in p or "list" in p):
        if "c++" in p:
            return """#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {1, 2, 3, 4, 5};
    for (int x : arr) cout << x << " ";
    cout << endl;
    return 0;
}"""
        else:
            return """arr = [1, 2, 3, 4, 5]
for item in arr:
    print(item, end=" ")"""

    # ── FIBONACCI ─────────────────────────────────────────────
    if "fibonacci" in p or "fib" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    for (int i = 0; i < 10; i++)
        cout << fibonacci(i) << " ";
    return 0;
}"""
        elif "java" in p:
            return """public class Fibonacci {
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n-1) + fibonacci(n-2);
    }
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++)
            System.out.print(fibonacci(i) + " ");
    }
}"""
        else:
            return """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i), end=" ")"""

    # ── FACTORIAL ─────────────────────────────────────────────
    if "factorial" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n-1);
}

int main() {
    cout << factorial(5) << endl;
    return 0;
}"""
        elif "java" in p:
            return """public class Main {
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n-1);
    }
    public static void main(String[] args) {
        System.out.println(factorial(5));
    }
}"""
        else:
            return """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))"""

    # ── PRIME ─────────────────────────────────────────────────
    if "prime" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}

int main() {
    for (int i = 2; i <= 20; i++)
        if (isPrime(i)) cout << i << " ";
    return 0;
}"""
        else:
            return """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

primes = [x for x in range(2, 21) if is_prime(x)]
print(primes)"""

    # ── PALINDROME ────────────────────────────────────────────
    if "palindrome" in p:
        if "c++" in p:
            return """#include <iostream>
#include <algorithm>
using namespace std;

bool isPalindrome(string s) {
    string rev = s;
    reverse(rev.begin(), rev.end());
    return s == rev;
}

int main() {
    cout << isPalindrome("racecar") << endl;
    return 0;
}"""
        else:
            return """def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("racecar"))
print(is_palindrome("hello"))"""

    # ── ARMSTRONG ─────────────────────────────────────────────
    if "armstrong" in p:
        if "c++" in p:
            return """#include <iostream>
#include <cmath>
using namespace std;

bool isArmstrong(int n) {
    int temp = n, sum = 0, digits = to_string(n).length();
    while (temp > 0) {
        sum += pow(temp % 10, digits);
        temp /= 10;
    }
    return sum == n;
}

int main() {
    cout << isArmstrong(153) << endl;
    cout << isArmstrong(123) << endl;
    return 0;
}"""
        else:
            return """def is_armstrong(n):
    digits = len(str(n))
    return sum(int(d)**digits for d in str(n)) == n

print(is_armstrong(153))  # True
print(is_armstrong(123))  # False"""

    # ── GCD / HCF ─────────────────────────────────────────────
    if "gcd" in p or "hcf" in p or "greatest common" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

int main() {
    cout << "GCD: " << gcd(48, 18) << endl;
    return 0;
}"""
        else:
            return """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(f"GCD: {gcd(48, 18)}")"""

    # ── POWER ─────────────────────────────────────────────────
    if "power" in p or "exponent" in p:
        if "c++" in p:
            return """#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int base = 2, exp = 10;
    cout << base << "^" << exp << " = " << pow(base, exp) << endl;
    return 0;
}"""
        else:
            return """def power(base, exp):
    return base ** exp

print(power(2, 10))  # 1024"""

    # ── COUNT VOWELS ──────────────────────────────────────────
    if "vowel" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int countVowels(string s) {
    int count = 0;
    for (char c : s)
        if (c=='a'||c=='e'||c=='i'||c=='o'||c=='u'||
            c=='A'||c=='E'||c=='I'||c=='O'||c=='U')
            count++;
    return count;
}

int main() {
    cout << countVowels("Hello World") << endl;
    return 0;
}"""
        else:
            return """def count_vowels(s):
    return sum(1 for c in s.lower() if c in 'aeiou')

print(count_vowels("Hello World"))  # 3"""

    # ── STRING LENGTH ─────────────────────────────────────────
    if ("length" in p or "size" in p) and ("string" in p or "str" in p):
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int stringLength(string s) {
    int len = 0;
    while (s[len] != '\\0') len++;
    return len;
}

int main() {
    cout << stringLength("hello") << endl;
    return 0;
}"""
        else:
            return """def string_length(s):
    count = 0
    for _ in s:
        count += 1
    return count

print(string_length("hello"))  # 5"""

    # ── MATRIX MULTIPLICATION ─────────────────────────────────
    if "matrix" in p and ("multipl" in p or "product" in p):
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int main() {
    int a[2][2] = {{1,2},{3,4}};
    int b[2][2] = {{5,6},{7,8}};
    int c[2][2] = {{0,0},{0,0}};
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            for (int k = 0; k < 2; k++)
                c[i][j] += a[i][k] * b[k][j];
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++)
            cout << c[i][j] << " ";
        cout << endl;
    }
    return 0;
}"""
        else:
            return """def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    cols_B = len(B[0])
    C = [[0]*cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
print(matrix_multiply(A, B))"""

    # ── LINEAR SEARCH ─────────────────────────────────────────
    if "linear search" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int linearSearch(int arr[], int n, int target) {
    for (int i = 0; i < n; i++)
        if (arr[i] == target) return i;
    return -1;
}

int main() {
    int arr[] = {2, 4, 6, 8, 10};
    cout << linearSearch(arr, 5, 6) << endl;
    return 0;
}"""
        else:
            return """def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

print(linear_search([2, 4, 6, 8, 10], 6))  # 2"""

    # ── BINARY SEARCH ─────────────────────────────────────────
    if "binary search" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int main() {
    int arr[] = {1, 3, 5, 7, 9};
    cout << binarySearch(arr, 5, 7) << endl;
    return 0;
}"""
        else:
            return """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9], 7))"""

    # ── BUBBLE SORT ───────────────────────────────────────────
    if "bubble sort" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++)
        for (int j = 0; j < n-i-1; j++)
            if (arr[j] > arr[j+1])
                swap(arr[j], arr[j+1]);
}

int main() {
    int arr[] = {64, 34, 25, 12, 22};
    bubbleSort(arr, 5);
    for (int i = 0; i < 5; i++) cout << arr[i] << " ";
    return 0;
}"""
        else:
            return """def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22]))"""

    # ── SELECTION SORT ────────────────────────────────────────
    if "selection sort" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

void selectionSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        int minIdx = i;
        for (int j = i+1; j < n; j++)
            if (arr[j] < arr[minIdx]) minIdx = j;
        swap(arr[i], arr[minIdx]);
    }
}

int main() {
    int arr[] = {64, 25, 12, 22, 11};
    selectionSort(arr, 5);
    for (int i = 0; i < 5; i++) cout << arr[i] << " ";
    return 0;
}"""
        else:
            return """def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print(selection_sort([64, 25, 12, 22, 11]))"""

    # ── INSERTION SORT ────────────────────────────────────────
    if "insertion sort" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i], j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = key;
    }
}

int main() {
    int arr[] = {12, 11, 13, 5, 6};
    insertionSort(arr, 5);
    for (int i = 0; i < 5; i++) cout << arr[i] << " ";
    return 0;
}"""
        else:
            return """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

print(insertion_sort([12, 11, 13, 5, 6]))"""

    # ── MERGE SORT ────────────────────────────────────────────
    if "merge sort" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

void merge(int arr[], int l, int m, int r) {
    int n1 = m-l+1, n2 = r-m;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++) L[i] = arr[l+i];
    for (int i = 0; i < n2; i++) R[i] = arr[m+1+i];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2)
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r-l)/2;
        mergeSort(arr, l, m);
        mergeSort(arr, m+1, r);
        merge(arr, l, m, r);
    }
}

int main() {
    int arr[] = {12, 11, 13, 5, 6, 7};
    mergeSort(arr, 0, 5);
    for (int i = 0; i < 6; i++) cout << arr[i] << " ";
    return 0;
}"""
        else:
            return """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge_sort([12, 11, 13, 5, 6, 7]))"""

    # ── QUICK SORT ────────────────────────────────────────────
    if "quick sort" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int partition(int arr[], int low, int high) {
    int pivot = arr[high], i = low - 1;
    for (int j = low; j < high; j++)
        if (arr[j] <= pivot) swap(arr[++i], arr[j]);
    swap(arr[i+1], arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi-1);
        quickSort(arr, pi+1, high);
    }
}

int main() {
    int arr[] = {10, 7, 8, 9, 1, 5};
    quickSort(arr, 0, 5);
    for (int i = 0; i < 6; i++) cout << arr[i] << " ";
    return 0;
}"""
        else:
            return """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([10, 7, 8, 9, 1, 5]))"""

    # ── GENERAL SORT ──────────────────────────────────────────
    if "sort" in p:
        if "c++" in p:
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {5, 3, 1, 4, 2};
    sort(arr.begin(), arr.end());
    for (int x : arr) cout << x << " ";
    return 0;
}"""
        else:
            return """arr = [5, 3, 1, 4, 2]
arr.sort()
print(arr)"""

    # ── QUEUE ─────────────────────────────────────────────────
    if "queue" in p:
        if "c++" in p:
            return """#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    return 0;
}"""
        else:
            return """from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)

while queue:
    print(queue.popleft(), end=" ")"""

    # ── STACK ─────────────────────────────────────────────────
    if "stack" in p:
        if "c++" in p:
            return """#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> st;
    st.push(1);
    st.push(2);
    st.push(3);
    while (!st.empty()) {
        cout << st.top() << " ";
        st.pop();
    }
    return 0;
}"""
        else:
            return """stack = []
stack.append(1)
stack.append(2)
stack.append(3)

while stack:
    print(stack.pop(), end=" ")"""

    # ── LINKED LIST ───────────────────────────────────────────
    if "linked list" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

void printList(Node* head) {
    while (head) {
        cout << head->data << " ";
        head = head->next;
    }
}

int main() {
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(3);
    printList(head);
    return 0;
}"""
        else:
            return """class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" ")
            curr = curr.next

ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.print_list()"""

    # ── STAR PATTERN ──────────────────────────────────────────
    if "pattern" in p or ("star" in p and ("print" in p or "display" in p)):
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int main() {
    int n = 5;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++)
            cout << "* ";
        cout << endl;
    }
    return 0;
}"""
        else:
            return """n = 5
for i in range(1, n+1):
    print("* " * i)"""

    # ── CALCULATOR ────────────────────────────────────────────
    if "calculator" in p:
        if "c++" in p:
            return """#include <iostream>
using namespace std;

int main() {
    double a, b;
    char op;
    cout << "Enter: num op num: ";
    cin >> a >> op >> b;
    if (op == '+') cout << a + b;
    else if (op == '-') cout << a - b;
    else if (op == '*') cout << a * b;
    else if (op == '/' && b != 0) cout << a / b;
    else cout << "Invalid";
    return 0;
}"""
        else:
            return """def calculator(a, op, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/' and b != 0: return a / b
    return "Invalid"

print(calculator(10, '+', 5))
print(calculator(10, '/', 2))"""

    # ── PRINT / DISPLAY (generic) ─────────────────────────────
    if "print" in p or "display" in p or "show" in p:
        text = prompt.replace("print", "").replace("display", "").replace("show", "").strip()
        if "c++" in p:
            return f"""#include <iostream>
using namespace std;

int main() {{
    cout << "{text}" << endl;
    return 0;
}}"""
        elif "java" in p:
            return f"""public class Main {{
    public static void main(String[] args) {{
        System.out.println("{text}");
    }}
}}"""
        else:
            return f'print("{text}")'

    # ── DEFAULT FALLBACK ──────────────────────────────────────
    if "c++" in p or "cpp" in p:
        return f"""#include <iostream>
using namespace std;

// Program to: {prompt}
int main() {{
    // TODO: Implement - {prompt}
    cout << "Running: {prompt}" << endl;
    return 0;
}}"""
    elif "java" in p:
        return f"""public class Main {{
    // Program to: {prompt}
    public static void main(String[] args) {{
        // TODO: Implement - {prompt}
        System.out.println("Running: {prompt}");
    }}
}}"""
    else:
        return f"""# Program to: {prompt}
def main():
    # TODO: Implement - {prompt}
    print("Running: {prompt}")

main()"""