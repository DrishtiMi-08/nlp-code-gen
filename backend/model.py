import os
import torch
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "Salesforce/codet5-base")
DEVICE = torch.device("cpu")

print(f"[model] Loading mock model (lightweight mode) ...")
print(f"[model] Mock model ready.")


def detect_language(p: str) -> str:
    if "c++" in p or "cpp" in p: return "cpp"
    if "java" in p: return "java"
    if "c#" in p or "csharp" in p: return "csharp"
    if " c " in p or p.endswith(" c"): return "c"
    return "python"


def generate_code(prompt: str, max_new_tokens: int = 256) -> str:
    p = prompt.lower()
    lang = detect_language(p)

    # ── HELLO WORLD ───────────────────────────────────────────
    if "hello" in p and "world" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}"""
        if lang == "c":
            return """#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}"""
        if lang == "csharp":
            return """using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, World!");
    }
}"""
        return 'print("Hello, World!")'

    # ── PRINT PATTERNS (useful debugging/series cases) ────────

    if "print" in p and any(x in p for x in ["table", "multiplication table"]):
        # Extract number if given e.g. "print table of 5"
        import re
        match = re.search(r'\d+', p)
        n = match.group() if match else "n"
        if lang == "cpp":
            return f"""#include <iostream>
using namespace std;

void printTable(int n) {{
    for (int i = 1; i <= 10; i++)
        cout << n << " x " << i << " = " << n*i << endl;
}}

int main() {{
    printTable({n});
    return 0;
}}"""
        if lang == "java":
            return f"""public class Main {{
    static void printTable(int n) {{
        for (int i = 1; i <= 10; i++)
            System.out.println(n + " x " + i + " = " + (n*i));
    }}
    public static void main(String[] args) {{
        printTable({n});
    }}
}}"""
        return f"""def print_table(n):
    for i in range(1, 11):
        print(f"{{n}} x {{i}} = {{n*i}}")

print_table({n})"""

    if "print" in p and any(x in p for x in ["fibonacci", "fib"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void printFibonacci(int n) {
    int a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        cout << a << " ";
        int temp = a + b;
        a = b;
        b = temp;
    }
    cout << endl;
}

int main() {
    printFibonacci(10);
    return 0;
}"""
        return """def print_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

print_fibonacci(10)"""

    if "print" in p and "prime" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}

void printPrimes(int limit) {
    for (int i = 2; i <= limit; i++)
        if (isPrime(i)) cout << i << " ";
    cout << endl;
}

int main() {
    printPrimes(50);
    return 0;
}"""
        return """def print_primes(limit):
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    for i in range(2, limit+1):
        if is_prime(i): print(i, end=" ")

print_primes(50)"""

    if "print" in p and any(x in p for x in ["even numbers", "even number"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void printEven(int limit) {
    for (int i = 2; i <= limit; i += 2)
        cout << i << " ";
    cout << endl;
}

int main() {
    printEven(20);
    return 0;
}"""
        return """def print_even(limit):
    for i in range(2, limit+1, 2):
        print(i, end=" ")

print_even(20)"""

    if "print" in p and any(x in p for x in ["odd numbers", "odd number"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void printOdd(int limit) {
    for (int i = 1; i <= limit; i += 2)
        cout << i << " ";
    cout << endl;
}

int main() {
    printOdd(20);
    return 0;
}"""
        return """def print_odd(limit):
    for i in range(1, limit+1, 2):
        print(i, end=" ")

print_odd(20)"""

    if "print" in p and any(x in p for x in ["natural numbers", "natural number"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void printNatural(int n) {
    for (int i = 1; i <= n; i++)
        cout << i << " ";
    cout << endl;
}

int main() {
    printNatural(10);
    return 0;
}"""
        return """def print_natural(n):
    for i in range(1, n+1):
        print(i, end=" ")

print_natural(10)"""

    if "print" in p and "armstrong" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <cmath>
using namespace std;

void printArmstrong(int limit) {
    for (int n = 1; n <= limit; n++) {
        int temp = n, sum = 0, d = to_string(n).length();
        while (temp > 0) { sum += pow(temp%10, d); temp /= 10; }
        if (sum == n) cout << n << " ";
    }
    cout << endl;
}

int main() {
    printArmstrong(1000);
    return 0;
}"""
        return """def print_armstrong(limit):
    for n in range(1, limit+1):
        d = len(str(n))
        if sum(int(x)**d for x in str(n)) == n:
            print(n, end=" ")

print_armstrong(1000)"""

    if "print" in p and any(x in p for x in ["linked list", "linkedlist"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

void printList(Node* head) {
    while (head) {
        cout << head->data;
        if (head->next) cout << " -> ";
        head = head->next;
    }
    cout << endl;
}

int main() {
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(3);
    printList(head);
    return 0;
}"""
        return """class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def print_linked_list(head):
    curr = head
    while curr:
        print(curr.data, end=" -> " if curr.next else "\\n")
        curr = curr.next

head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
print_linked_list(head)"""

    if "print" in p and "matrix" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void printMatrix(int matrix[][3], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++)
            cout << matrix[i][j] << " ";
        cout << endl;
    }
}

int main() {
    int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    printMatrix(matrix, 3, 3);
    return 0;
}"""
        return """def print_matrix(matrix):
    for row in matrix:
        print(*row)

matrix = [[1,2,3],[4,5,6],[7,8,9]]
print_matrix(matrix)"""

    if "print" in p and any(x in p for x in ["binary tree", "tree inorder", "tree preorder", "tree postorder", "inorder", "preorder", "postorder"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(nullptr), right(nullptr) {}
};

void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->data << " ";
    inorder(root->right);
}

void preorder(Node* root) {
    if (!root) return;
    cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}

void postorder(Node* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->data << " ";
}

int main() {
    Node* root = new Node(1);
    root->left = new Node(2);
    root->right = new Node(3);
    cout << "Inorder: "; inorder(root); cout << endl;
    cout << "Preorder: "; preorder(root); cout << endl;
    cout << "Postorder: "; postorder(root); cout << endl;
    return 0;
}"""
        return """class Node:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

def preorder(root):
    if root:
        print(root.val, end=" ")
        preorder(root.left)
        preorder(root.right)

def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val, end=" ")

root = Node(1)
root.left = Node(2)
root.right = Node(3)
print("Inorder:"); inorder(root)
print("\\nPreorder:"); preorder(root)
print("\\nPostorder:"); postorder(root)"""

    if "print" in p and any(x in p for x in ["stack", "queue"]):
        if "queue" in p:
            if lang == "cpp":
                return """#include <iostream>
#include <queue>
using namespace std;

void printQueue(queue<int> q) {
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
}

int main() {
    queue<int> q;
    q.push(1); q.push(2); q.push(3);
    printQueue(q);
    return 0;
}"""
            return """from collections import deque

def print_queue(q):
    temp = list(q)
    print(*temp)

q = deque([1, 2, 3])
print_queue(q)"""
        if lang == "cpp":
            return """#include <iostream>
#include <stack>
using namespace std;

void printStack(stack<int> st) {
    while (!st.empty()) {
        cout << st.top() << " ";
        st.pop();
    }
    cout << endl;
}

int main() {
    stack<int> st;
    st.push(1); st.push(2); st.push(3);
    printStack(st);
    return 0;
}"""
        return """def print_stack(stack):
    print(*reversed(stack))

stack = [1, 2, 3]
print_stack(stack)"""

    if "print" in p and "variable" in p:
        import re
        # Try to extract variable name after "variable"
        match = re.search(r'variable\s+(\w+)', p)
        var = match.group(1) if match else "x"
        return f"""def print_variable(value, name="{var}"):
    print(f"{{name}} = {{value}}")

# Usage:
{var} = 42  # replace with your actual variable
print_variable({var}, "{var}")"""

    if "print" in p and any(x in p for x in ["array", "list", "elements"]):
        if lang == "cpp":
            return """#include <iostream>
#include <vector>
using namespace std;

void printArray(vector<int> arr) {
    for (int x : arr) cout << x << " ";
    cout << endl;
}

int main() {
    vector<int> arr = {1, 2, 3, 4, 5};
    printArray(arr);
    return 0;
}"""
        return """def print_array(arr):
    for item in arr:
        print(item, end=" ")
    print()

arr = [1, 2, 3, 4, 5]
print_array(arr)"""

    # ── EVEN OR ODD ───────────────────────────────────────────
    if any(x in p for x in ["even or odd", "odd or even"]) or ("even" in p and "odd" in p):
        if lang == "cpp":
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
        if lang == "java":
            return """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n % 2 == 0 ? "Even" : "Odd");
    }
}"""
        return """n = int(input("Enter a number: "))
if n % 2 == 0:
    print(f"{n} is Even")
else:
    print(f"{n} is Odd")"""

    # ── SWAP ──────────────────────────────────────────────────
    if "swap" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int a = 5, b = 10;
    cout << "Before swap: a=" << a << " b=" << b << endl;
    swap(a, b);
    cout << "After swap: a=" << a << " b=" << b << endl;
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    public static void main(String[] args) {
        int a = 5, b = 10;
        System.out.println("Before: a=" + a + " b=" + b);
        int temp = a; a = b; b = temp;
        System.out.println("After: a=" + a + " b=" + b);
    }
}"""
        return """a = 5
b = 10
print(f"Before: a={a}, b={b}")
a, b = b, a
print(f"After: a={a}, b={b}")"""

    # ── REVERSE ───────────────────────────────────────────────
    if "reverse" in p and "array" in p:
        if lang == "cpp":
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
        if lang == "java":
            return """import java.util.Arrays;
import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        Integer[] arr = {1, 2, 3, 4, 5};
        Collections.reverse(Arrays.asList(arr));
        System.out.println(Arrays.toString(arr));
    }
}"""
        return """def reverse_array(arr):
    return arr[::-1]

result = reverse_array([1, 2, 3, 4, 5])
print(result)"""

    if "reverse" in p and any(x in p for x in ["string", "str"]):
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    string s = "hello";
    reverse(s.begin(), s.end());
    cout << s << endl;
    return 0;
}"""
        return """def reverse_string(s):
    return s[::-1]

print(reverse_string("hello"))"""

    if "reverse" in p and any(x in p for x in ["number", "num", "integer", "digit"]):
        if lang == "cpp":
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
        return """def reverse_number(n):
    return int(str(n)[::-1])

print(reverse_number(12345))"""

    # ── SUM ───────────────────────────────────────────────────
    if "sum" in p and any(x in p for x in ["array", "list", "elements", "numbers"]):
        if lang == "cpp":
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
        return """arr = [1, 2, 3, 4, 5]
print(f"Sum: {sum(arr)}")"""

    if "sum" in p and any(x in p for x in ["digits", "digit"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int sumDigits(int n) {
    int sum = 0;
    while (n > 0) { sum += n % 10; n /= 10; }
    return sum;
}

int main() {
    cout << sumDigits(1234) << endl;
    return 0;
}"""
        return """def sum_digits(n):
    return sum(int(d) for d in str(n))

print(sum_digits(1234))"""

    # ── MAX / MIN ─────────────────────────────────────────────
    if any(x in p for x in ["maximum", "largest", "biggest"]) and any(x in p for x in ["array", "list", "elements"]):
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Max: " << *max_element(arr.begin(), arr.end()) << endl;
    return 0;
}"""
        return """arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Max: {max(arr)}")"""

    if any(x in p for x in ["minimum", "smallest"]) and any(x in p for x in ["array", "list", "elements"]):
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    cout << "Min: " << *min_element(arr.begin(), arr.end()) << endl;
    return 0;
}"""
        return """arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Min: {min(arr)}")"""

    # ── CREATE / PRINT ARRAY ──────────────────────────────────
    if any(x in p for x in ["create", "initialize", "declare"]) and any(x in p for x in ["array", "list"]):
        if lang == "cpp":
            return """#include <iostream>
#include <vector>
using namespace std;

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    vector<int> v = {10, 20, 30, 40, 50};
    for (int x : v) cout << x << " ";
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        for (int x : arr)
            System.out.print(x + " ");
    }
}"""
        return """arr = [1, 2, 3, 4, 5]
arr2 = list(range(1, 6))
print(arr)
print(arr2)"""

    # ── FIBONACCI ─────────────────────────────────────────────
    if any(x in p for x in ["fibonacci", "fib"]):
        if lang == "cpp":
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
        if lang == "java":
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
        return """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i), end=" ")"""

    # ── FACTORIAL ─────────────────────────────────────────────
    if "factorial" in p:
        if lang == "cpp":
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
        if lang == "java":
            return """public class Main {
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n-1);
    }
    public static void main(String[] args) {
        System.out.println(factorial(5));
    }
}"""
        return """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))"""

    # ── PRIME ─────────────────────────────────────────────────
    if "prime" in p:
        if lang == "cpp":
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
        if lang == "java":
            return """public class Main {
    static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i * i <= n; i++)
            if (n % i == 0) return false;
        return true;
    }
    public static void main(String[] args) {
        for (int i = 2; i <= 20; i++)
            if (isPrime(i)) System.out.print(i + " ");
    }
}"""
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
        if lang == "cpp":
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
    cout << isPalindrome("hello") << endl;
    return 0;
}"""
        return """def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False"""

    # ── ARMSTRONG ─────────────────────────────────────────────
    if "armstrong" in p:
        if lang == "cpp":
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
        return """def is_armstrong(n):
    digits = len(str(n))
    return sum(int(d)**digits for d in str(n)) == n

print(is_armstrong(153))  # True
print(is_armstrong(123))  # False"""

    # ── LCM ───────────────────────────────────────────────────
    if "lcm" in p or "least common" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
int lcm(int a, int b) { return a / gcd(a, b) * b; }

int main() {
    cout << "LCM: " << lcm(4, 6) << endl;
    return 0;
}"""
        return """import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

print(f"LCM: {lcm(4, 6)}")"""

    # ── GCD / HCF ─────────────────────────────────────────────
    if any(x in p for x in ["gcd", "hcf", "greatest common"]):
        if lang == "cpp":
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
        return """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(f"GCD: {gcd(48, 18)}")"""

    # ── SQUARE ROOT ───────────────────────────────────────────
    if "square root" in p or "sqrt" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <cmath>
using namespace std;

int main() {
    cout << sqrt(25) << endl;
    return 0;
}"""
        return """import math
print(math.sqrt(25))  # 5.0"""

    # ── POWER ─────────────────────────────────────────────────
    if "power" in p or "exponent" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <cmath>
using namespace std;

int main() {
    cout << pow(2, 10) << endl;
    return 0;
}"""
        return """def power(base, exp):
    return base ** exp

print(power(2, 10))  # 1024"""

    # ── COUNT VOWELS / CONSONANTS ─────────────────────────────
    if "consonant" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int countConsonants(string s) {
    int count = 0;
    string vowels = "aeiouAEIOU";
    for (char c : s)
        if (isalpha(c) && vowels.find(c) == string::npos) count++;
    return count;
}

int main() {
    cout << countConsonants("Hello World") << endl;
    return 0;
}"""
        return """def count_consonants(s):
    return sum(1 for c in s.lower() if c.isalpha() and c not in 'aeiou')

print(count_consonants("Hello World"))  # 7"""

    if "vowel" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int countVowels(string s) {
    int count = 0;
    for (char c : s)
        if (string("aeiouAEIOU").find(c) != string::npos) count++;
    return count;
}

int main() {
    cout << countVowels("Hello World") << endl;
    return 0;
}"""
        return """def count_vowels(s):
    return sum(1 for c in s.lower() if c in 'aeiou')

print(count_vowels("Hello World"))  # 3"""

    # ── STRING OPERATIONS ─────────────────────────────────────
    if "uppercase" in p or "upper case" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    string s = "hello world";
    transform(s.begin(), s.end(), s.begin(), ::toupper);
    cout << s << endl;
    return 0;
}"""
        return """s = "hello world"
print(s.upper())"""

    if "lowercase" in p or "lower case" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    string s = "HELLO WORLD";
    transform(s.begin(), s.end(), s.begin(), ::tolower);
    cout << s << endl;
    return 0;
}"""
        return """s = "HELLO WORLD"
print(s.lower())"""

    if "concatenat" in p or ("join" in p and "string" in p):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    string s1 = "Hello";
    string s2 = " World";
    cout << s1 + s2 << endl;
    return 0;
}"""
        return """s1 = "Hello"
s2 = " World"
print(s1 + s2)"""

    if any(x in p for x in ["length", "size"]) and any(x in p for x in ["string", "str", "word"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    string s = "hello";
    cout << "Length: " << s.length() << endl;
    return 0;
}"""
        return """def string_length(s):
    return len(s)

print(string_length("hello"))  # 5"""

    # ── ANAGRAM ───────────────────────────────────────────────
    if "anagram" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <algorithm>
using namespace std;

bool isAnagram(string s1, string s2) {
    sort(s1.begin(), s1.end());
    sort(s2.begin(), s2.end());
    return s1 == s2;
}

int main() {
    cout << isAnagram("listen", "silent") << endl;
    return 0;
}"""
        return """def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

print(is_anagram("listen", "silent"))  # True"""

    # ── MATRIX ────────────────────────────────────────────────
    if "matrix" in p and "transpose" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int a[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
    for (int i=0;i<3;i++) {
        for (int j=0;j<3;j++) cout << a[j][i] << " ";
        cout << endl;
    }
    return 0;
}"""
        return """matrix = [[1,2,3],[4,5,6],[7,8,9]]
transpose = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
for row in transpose:
    print(row)"""

    if "matrix" in p and any(x in p for x in ["multipl", "product"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int a[2][2] = {{1,2},{3,4}};
    int b[2][2] = {{5,6},{7,8}};
    int c[2][2] = {{0,0},{0,0}};
    for (int i=0;i<2;i++)
        for (int j=0;j<2;j++)
            for (int k=0;k<2;k++)
                c[i][j] += a[i][k]*b[k][j];
    for (int i=0;i<2;i++) {
        for (int j=0;j<2;j++) cout << c[i][j] << " ";
        cout << endl;
    }
    return 0;
}"""
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

    if "matrix" in p and any(x in p for x in ["add", "addition", "sum"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int a[2][2] = {{1,2},{3,4}};
    int b[2][2] = {{5,6},{7,8}};
    for (int i=0;i<2;i++) {
        for (int j=0;j<2;j++) cout << a[i][j]+b[i][j] << " ";
        cout << endl;
    }
    return 0;
}"""
        return """A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
result = [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]
for row in result:
    print(row)"""

    # ── SEARCH ────────────────────────────────────────────────
    if "linear search" in p:
        if lang == "cpp":
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
        return """def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

print(linear_search([2, 4, 6, 8, 10], 6))  # 2"""

    if "binary search" in p:
        if lang == "cpp":
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

    # ── SORTING ───────────────────────────────────────────────
    if "bubble sort" in p:
        if lang == "cpp":
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
        return """def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22]))"""

    if "selection sort" in p:
        if lang == "cpp":
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
        return """def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print(selection_sort([64, 25, 12, 22, 11]))"""

    if "insertion sort" in p:
        if lang == "cpp":
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

    if "merge sort" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void merge(int arr[], int l, int m, int r) {
    int n1=m-l+1, n2=r-m;
    int L[n1], R[n2];
    for(int i=0;i<n1;i++) L[i]=arr[l+i];
    for(int i=0;i<n2;i++) R[i]=arr[m+1+i];
    int i=0, j=0, k=l;
    while(i<n1 && j<n2) arr[k++]=(L[i]<=R[j])?L[i++]:R[j++];
    while(i<n1) arr[k++]=L[i++];
    while(j<n2) arr[k++]=R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if(l<r) {
        int m=l+(r-l)/2;
        mergeSort(arr,l,m);
        mergeSort(arr,m+1,r);
        merge(arr,l,m,r);
    }
}

int main() {
    int arr[]={12,11,13,5,6,7};
    mergeSort(arr,0,5);
    for(int i=0;i<6;i++) cout<<arr[i]<<" ";
    return 0;
}"""
        return """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
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

    if "quick sort" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int partition(int arr[], int low, int high) {
    int pivot=arr[high], i=low-1;
    for(int j=low;j<high;j++)
        if(arr[j]<=pivot) swap(arr[++i],arr[j]);
    swap(arr[i+1],arr[high]);
    return i+1;
}

void quickSort(int arr[], int low, int high) {
    if(low<high) {
        int pi=partition(arr,low,high);
        quickSort(arr,low,pi-1);
        quickSort(arr,pi+1,high);
    }
}

int main() {
    int arr[]={10,7,8,9,1,5};
    quickSort(arr,0,5);
    for(int i=0;i<6;i++) cout<<arr[i]<<" ";
    return 0;
}"""
        return """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([10, 7, 8, 9, 1, 5]))"""

    if "heap sort" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

void heapify(int arr[], int n, int i) {
    int largest=i, l=2*i+1, r=2*i+2;
    if(l<n && arr[l]>arr[largest]) largest=l;
    if(r<n && arr[r]>arr[largest]) largest=r;
    if(largest!=i) { swap(arr[i],arr[largest]); heapify(arr,n,largest); }
}

void heapSort(int arr[], int n) {
    for(int i=n/2-1;i>=0;i--) heapify(arr,n,i);
    for(int i=n-1;i>0;i--) { swap(arr[0],arr[i]); heapify(arr,i,0); }
}

int main() {
    int arr[]={12,11,13,5,6,7};
    heapSort(arr,6);
    for(int i=0;i<6;i++) cout<<arr[i]<<" ";
    return 0;
}"""
        return """def heapify(arr, n, i):
    largest = i
    l, r = 2*i+1, 2*i+2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n//2-1, -1, -1): heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr

print(heap_sort([12, 11, 13, 5, 6, 7]))"""

    if "sort" in p:
        if lang == "cpp":
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
        return """arr = [5, 3, 1, 4, 2]
arr.sort()
print(arr)"""

    # ── DATA STRUCTURES ───────────────────────────────────────
    if "queue" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(1); q.push(2); q.push(3);
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    return 0;
}"""
        return """from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)

while queue:
    print(queue.popleft(), end=" ")"""

    if "stack" in p:
        if lang == "cpp":
            return """#include <iostream>
#include <stack>
using namespace std;

int main() {
    stack<int> st;
    st.push(1); st.push(2); st.push(3);
    while (!st.empty()) {
        cout << st.top() << " ";
        st.pop();
    }
    return 0;
}"""
        return """stack = []
stack.append(1)
stack.append(2)
stack.append(3)

while stack:
    print(stack.pop(), end=" ")"""

    if "linked list" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

void printList(Node* head) {
    while (head) { cout << head->data << " "; head = head->next; }
}

int main() {
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(3);
    printList(head);
    return 0;
}"""
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
ll.append(1); ll.append(2); ll.append(3)
ll.print_list()"""

    if any(x in p for x in ["binary tree", "bst", "binary search tree"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node *left, *right;
    Node(int val) : data(val), left(nullptr), right(nullptr) {}
};

Node* insert(Node* root, int val) {
    if (!root) return new Node(val);
    if (val < root->data) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}

void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->data << " ";
    inorder(root->right);
}

int main() {
    Node* root = nullptr;
    for (int x : {5,3,7,1,4}) root = insert(root, x);
    inorder(root);
    return 0;
}"""
        return """class Node:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def insert(root, val):
    if not root: return Node(val)
    if val < root.val: root.left = insert(root.left, val)
    else: root.right = insert(root.right, val)
    return root

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

root = None
for x in [5,3,7,1,4]: root = insert(root, x)
inorder(root)"""

    if "hash" in p and any(x in p for x in ["map", "table"]):
        if lang == "cpp":
            return """#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<string, int> hashMap;
    hashMap["apple"] = 1;
    hashMap["banana"] = 2;
    hashMap["cherry"] = 3;
    for (auto& pair : hashMap)
        cout << pair.first << ": " << pair.second << endl;
    return 0;
}"""
        return """hash_map = {}
hash_map["apple"] = 1
hash_map["banana"] = 2
hash_map["cherry"] = 3

for key, value in hash_map.items():
    print(f"{key}: {value}")"""

    # ── PATTERNS ──────────────────────────────────────────────
    if "pattern" in p or ("star" in p and any(x in p for x in ["print", "display", "draw"])):
        if any(x in p for x in ["pyramid", "triangle"]):
            if lang == "cpp":
                return """#include <iostream>
using namespace std;

int main() {
    int n = 5;
    for (int i=1;i<=n;i++) {
        for (int j=1;j<=n-i;j++) cout << " ";
        for (int j=1;j<=2*i-1;j++) cout << "*";
        cout << endl;
    }
    return 0;
}"""
            return """n = 5
for i in range(1, n+1):
    print(" "*(n-i) + "*"*(2*i-1))"""
        if lang == "cpp":
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
        return """n = 5
for i in range(1, n+1):
    print("* " * i)"""

    if "number pattern" in p or ("number" in p and "pattern" in p):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int n = 5;
    for (int i=1;i<=n;i++) {
        for (int j=1;j<=i;j++) cout << j << " ";
        cout << endl;
    }
    return 0;
}"""
        return """n = 5
for i in range(1, n+1):
    print(*range(1, i+1))"""

    # ── CALCULATOR ────────────────────────────────────────────
    if "calculator" in p:
        if lang == "cpp":
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
        return """def calculator(a, op, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/' and b != 0: return a / b
    return "Invalid"

print(calculator(10, '+', 5))
print(calculator(10, '/', 2))"""

    # ── NUMBER CONVERSION ─────────────────────────────────────
    if "binary" in p and any(x in p for x in ["decimal", "convert"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int binaryToDecimal(string binary) {
    int decimal = 0, base = 1;
    for (int i = binary.length()-1; i >= 0; i--) {
        if (binary[i] == '1') decimal += base;
        base *= 2;
    }
    return decimal;
}

int main() {
    cout << binaryToDecimal("1010") << endl;
    return 0;
}"""
        return """def binary_to_decimal(binary):
    return int(binary, 2)

def decimal_to_binary(n):
    return bin(n)[2:]

print(binary_to_decimal("1010"))  # 10
print(decimal_to_binary(10))      # 1010"""

    # ── LOOPS ─────────────────────────────────────────────────
    if "for loop" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    for (int i = 0; i < 5; i++) {
        cout << "Iteration: " << i << endl;
    }
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 5; i++) {
            System.out.println("Iteration: " + i);
        }
    }
}"""
        return """for i in range(5):
    print(f"Iteration: {i}")"""

    if "while loop" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    int i = 0;
    while (i < 5) {
        cout << "i = " << i << endl;
        i++;
    }
    return 0;
}"""
        return """i = 0
while i < 5:
    print(f"i = {i}")
    i += 1"""

    # ── RECURSION ─────────────────────────────────────────────
    if any(x in p for x in ["recursion", "recursive"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int sum(int n) {
    if (n <= 0) return 0;
    return n + sum(n - 1);
}

int main() {
    cout << "Sum 1 to 10: " << sum(10) << endl;
    return 0;
}"""
        return """def sum_recursive(n):
    if n <= 0:
        return 0
    return n + sum_recursive(n - 1)

print(f"Sum 1 to 10: {sum_recursive(10)}")"""

    # ── OOP ───────────────────────────────────────────────────
    if "inheritance" in p:
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

class Animal {
public:
    void eat() { cout << "Animal eats" << endl; }
};

class Dog : public Animal {
public:
    void bark() { cout << "Dog barks" << endl; }
};

int main() {
    Dog d;
    d.eat();
    d.bark();
    return 0;
}"""
        if lang == "java":
            return """class Animal {
    void eat() { System.out.println("Animal eats"); }
}

class Dog extends Animal {
    void bark() { System.out.println("Dog barks"); }

    public static void main(String[] args) {
        Dog d = new Dog();
        d.eat();
        d.bark();
    }
}"""
        return """class Animal:
    def eat(self):
        print("Animal eats")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

d = Dog()
d.eat()
d.bark()"""

    if "class" in p and any(x in p for x in ["object", "oop", "create"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

class Animal {
public:
    string name;
    int age;

    Animal(string n, int a) : name(n), age(a) {}

    void speak() {
        cout << name << " says hello!" << endl;
    }
};

int main() {
    Animal dog("Rex", 3);
    dog.speak();
    cout << "Age: " << dog.age << endl;
    return 0;
}"""
        if lang == "java":
            return """public class Animal {
    String name;
    int age;

    Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    void speak() {
        System.out.println(name + " says hello!");
    }

    public static void main(String[] args) {
        Animal dog = new Animal("Rex", 3);
        dog.speak();
    }
}"""
        return """class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"{self.name} says hello!")

dog = Animal("Rex", 3)
dog.speak()
print(f"Age: {dog.age}")"""

    # ── FILE HANDLING ─────────────────────────────────────────
    if "file" in p and any(x in p for x in ["read", "write", "open"]):
        if "write" in p:
            if lang == "cpp":
                return """#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ofstream file("output.txt");
    file << "Hello, World!" << endl;
    file.close();
    cout << "File written successfully" << endl;
    return 0;
}"""
            return """with open("output.txt", "w") as f:
    f.write("Hello, World!\\n")
print("File written successfully")"""
        if lang == "cpp":
            return """#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream file("input.txt");
    string line;
    while (getline(file, line))
        cout << line << endl;
    file.close();
    return 0;
}"""
        return """with open("input.txt", "r") as f:
    content = f.read()
print(content)"""

    # ── EXCEPTION HANDLING ────────────────────────────────────
    if any(x in p for x in ["exception", "error handling", "try catch"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int divide(int a, int b) {
    if (b == 0) throw runtime_error("Division by zero!");
    return a / b;
}

int main() {
    try {
        cout << divide(10, 2) << endl;
        cout << divide(10, 0) << endl;
    } catch (exception& e) {
        cout << "Error: " << e.what() << endl;
    }
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    public static void main(String[] args) {
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("Done");
        }
    }
}"""
        return """try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Done")"""

    # ── FUNCTION ──────────────────────────────────────────────
    if any(x in p for x in ["function", "method"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

int main() {
    cout << add(5, 3) << endl;
    cout << multiply(5, 3) << endl;
    return 0;
}"""
        if lang == "java":
            return """public class Main {
    static int add(int a, int b) { return a + b; }
    static int multiply(int a, int b) { return a * b; }

    public static void main(String[] args) {
        System.out.println(add(5, 3));
        System.out.println(multiply(5, 3));
    }
}"""
        return """def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(add(5, 3))
print(multiply(5, 3))"""

    # ── PYTHON SPECIFIC ───────────────────────────────────────
    if "list comprehension" in p or "comprehension" in p:
        return """numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

print("Squares:", squares)
print("Evens:", evens)"""

    if "lambda" in p:
        return """square = lambda x: x ** 2
add = lambda a, b: a + b
filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))

print(square(5))
print(add(3, 4))
print(filter_evens([1,2,3,4,5,6]))"""

    if any(x in p for x in ["generator", "yield"]):
        return """def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

for num in count_up(5):
    print(num)"""

    if "dictionary" in p:
        return """student = {
    "name": "Alice",
    "age": 20,
    "grade": "A"
}

print(student["name"])
for key, value in student.items():
    print(f"{key}: {value}")"""

    if any(x in p for x in ["type conversion", "type casting", "casting"]):
        if lang == "cpp":
            return """#include <iostream>
using namespace std;

int main() {
    double d = 3.14;
    int i = (int)d;
    cout << "double: " << d << endl;
    cout << "int: " << i << endl;
    return 0;
}"""
        return """x = 3.14
print(int(x))    # 3
print(str(x))    # "3.14"
print(float("3.14"))  # 3.14
print(bool(0))   # False
print(bool(1))   # True"""

    # ── DEFAULT FALLBACK ──────────────────────────────────────
    if lang == "cpp":
        return f"""#include <iostream>
using namespace std;

// Program to: {prompt}
int main() {{
    // TODO: Implement - {prompt}
    cout << "Running: {prompt}" << endl;
    return 0;
}}"""
    if lang == "java":
        return f"""public class Main {{
    // Program to: {prompt}
    public static void main(String[] args) {{
        // TODO: Implement - {prompt}
        System.out.println("Running: {prompt}");
    }}
}}"""
    return f"""# Program to: {prompt}
def main():
    # TODO: Implement - {prompt}
    print("Running: {prompt}")

main()"""