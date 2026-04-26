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

    # ── REVERSE ──────────────────────────────────────────────
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
        if "c++" in p or "cpp" in p:
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

    # ── SORT ──────────────────────────────────────────────────
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
            return """def sort_array(arr):
    return sorted(arr)

print(sort_array([5, 3, 1, 4, 2]))"""

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

    # ── HELLO WORLD ───────────────────────────────────────────
    if "hello" in p and "world" in p:
        if "c++" in p:
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

    # ── DEFAULT FALLBACK ──────────────────────────────────────
    if "c++" in p or "cpp" in p:
        return f"""#include <iostream>
using namespace std;

// Program to: {prompt}
int main() {{
    // TODO: Implement logic for: {prompt}
    cout << "Program running" << endl;
    return 0;
}}"""
    elif "java" in p:
        return f"""public class Main {{
    // Program to: {prompt}
    public static void main(String[] args) {{
        // TODO: Implement logic for: {prompt}
        System.out.println("Program running");
    }}
}}"""
    else:
        return f"""# Program to: {prompt}
def main():
    # TODO: Implement logic for: {prompt}
    print("Program running")

main()"""