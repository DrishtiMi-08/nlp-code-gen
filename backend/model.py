import os
import re
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
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}'
        if lang == "c":
            return '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}'
        if lang == "csharp":
            return 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}'
        return 'print("Hello, World!")'

    # ── PRINT / DISPLAY / OUTPUT (generic — handles anything) ─
    if any(w in p for w in ["print", "display", "output", "show", "write"]):
        # Extract what to print — remove trigger words and language words
        text = p
        for w in ["print", "display", "output", "show", "write", "c++", "cpp", "java", "python", "in", "using", "to", "the", "a", "an"]:
            text = text.replace(w, "")
        text = text.strip().strip('"').strip("'").strip() or "Hello"

        if lang == "cpp":
            return f'#include <iostream>\nusing namespace std;\n\nint main() {{\n    cout << "{text}" << endl;\n    return 0;\n}}'
        if lang == "java":
            return f'public class Main {{\n    public static void main(String[] args) {{\n        System.out.println("{text}");\n    }}\n}}'
        if lang == "c":
            return f'#include <stdio.h>\n\nint main() {{\n    printf("{text}\\n");\n    return 0;\n}}'
        return f'print("{text}")'

    # ── INPUT FROM USER ───────────────────────────────────────
    if "input" in p or "read" in p or ("take" in p and "user" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    string name;\n    int age;\n    cout << "Enter name: ";\n    cin >> name;\n    cout << "Enter age: ";\n    cin >> age;\n    cout << "Name: " << name << ", Age: " << age << endl;\n    return 0;\n}'
        if lang == "java":
            return 'import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        System.out.print("Enter name: ");\n        String name = sc.nextLine();\n        System.out.println("Hello, " + name);\n    }\n}'
        return 'name = input("Enter your name: ")\nage = int(input("Enter your age: "))\nprint(f"Name: {name}, Age: {age}")'

    # ── EVEN OR ODD ───────────────────────────────────────────
    if ("even" in p and "odd" in p) or "even or odd" in p or "odd or even" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int n;\n    cin >> n;\n    cout << (n % 2 == 0 ? "Even" : "Odd") << endl;\n    return 0;\n}'
        if lang == "java":
            return 'import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        System.out.println(n % 2 == 0 ? "Even" : "Odd");\n    }\n}'
        return 'n = int(input("Enter a number: "))\nprint("Even" if n % 2 == 0 else "Odd")'

    # ── SWAP ──────────────────────────────────────────────────
    if "swap" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int a = 5, b = 10;\n    cout << "Before: a=" << a << " b=" << b << endl;\n    swap(a, b);\n    cout << "After: a=" << a << " b=" << b << endl;\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static void main(String[] args) {\n        int a = 5, b = 10;\n        int temp = a; a = b; b = temp;\n        System.out.println("a=" + a + " b=" + b);\n    }\n}'
        return 'a, b = 5, 10\nprint(f"Before: a={a}, b={b}")\na, b = b, a\nprint(f"After: a={a}, b={b}")'

    # ── REVERSE ───────────────────────────────────────────────
    if "reverse" in p and "array" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {1, 2, 3, 4, 5};\n    reverse(arr.begin(), arr.end());\n    for (int x : arr) cout << x << " ";\n    return 0;\n}'
        if lang == "java":
            return 'import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Integer[] arr = {1, 2, 3, 4, 5};\n        Collections.reverse(Arrays.asList(arr));\n        System.out.println(Arrays.toString(arr));\n    }\n}'
        return 'arr = [1, 2, 3, 4, 5]\nprint(arr[::-1])'

    if "reverse" in p and ("string" in p or "str" in p):
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s = "hello";\n    reverse(s.begin(), s.end());\n    cout << s << endl;\n    return 0;\n}'
        return 'def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string("hello"))'

    if "reverse" in p and ("number" in p or "num" in p or "integer" in p or "digit" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint reverseNumber(int n) {\n    int rev = 0;\n    while (n > 0) {\n        rev = rev * 10 + n % 10;\n        n /= 10;\n    }\n    return rev;\n}\n\nint main() {\n    cout << reverseNumber(12345) << endl;\n    return 0;\n}'
        return 'def reverse_number(n):\n    return int(str(n)[::-1])\n\nprint(reverse_number(12345))'

    # ── SUM ───────────────────────────────────────────────────
    if "sum" in p and ("array" in p or "list" in p or "elements" in p or "numbers" in p):
        if lang == "cpp":
            return '#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {1, 2, 3, 4, 5};\n    int sum = 0;\n    for (int x : arr) sum += x;\n    cout << "Sum: " << sum << endl;\n    return 0;\n}'
        return 'arr = [1, 2, 3, 4, 5]\nprint(f"Sum: {sum(arr)}")'

    if "sum" in p and ("digits" in p or "digit" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint sumDigits(int n) {\n    int sum = 0;\n    while (n > 0) { sum += n % 10; n /= 10; }\n    return sum;\n}\n\nint main() {\n    cout << sumDigits(1234) << endl;\n    return 0;\n}'
        return 'def sum_digits(n):\n    return sum(int(d) for d in str(n))\n\nprint(sum_digits(1234))'

    # ── MAX / MIN ─────────────────────────────────────────────
    if any(w in p for w in ["maximum", "max", "largest", "biggest"]) and any(w in p for w in ["array", "list", "elements"]):
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};\n    cout << "Max: " << *max_element(arr.begin(), arr.end()) << endl;\n    return 0;\n}'
        return 'arr = [3, 1, 4, 1, 5, 9, 2, 6]\nprint(f"Max: {max(arr)}")'

    if any(w in p for w in ["minimum", "min", "smallest"]) and any(w in p for w in ["array", "list", "elements"]):
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};\n    cout << "Min: " << *min_element(arr.begin(), arr.end()) << endl;\n    return 0;\n}'
        return 'arr = [3, 1, 4, 1, 5, 9, 2, 6]\nprint(f"Min: {min(arr)}")'

    # ── CREATE / PRINT ARRAY ──────────────────────────────────
    if any(w in p for w in ["create", "initialize", "declare", "make"]) and any(w in p for w in ["array", "list"]):
        if lang == "cpp":
            return '#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int arr[5] = {1, 2, 3, 4, 5};\n    vector<int> v = {10, 20, 30, 40, 50};\n    for (int x : v) cout << x << " ";\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static void main(String[] args) {\n        int[] arr = {1, 2, 3, 4, 5};\n        for (int x : arr) System.out.print(x + " ");\n    }\n}'
        return 'arr = [1, 2, 3, 4, 5]\narr2 = list(range(1, 6))\nprint(arr)'

    if any(w in p for w in ["print", "display"]) and any(w in p for w in ["array", "list"]):
        if lang == "cpp":
            return '#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {1, 2, 3, 4, 5};\n    for (int x : arr) cout << x << " ";\n    return 0;\n}'
        return 'arr = [1, 2, 3, 4, 5]\nfor item in arr:\n    print(item, end=" ")'

    # ── FIBONACCI ─────────────────────────────────────────────
    if "fibonacci" in p or "fib" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint fibonacci(int n) {\n    if (n <= 1) return n;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\n\nint main() {\n    for (int i = 0; i < 10; i++)\n        cout << fibonacci(i) << " ";\n    return 0;\n}'
        if lang == "java":
            return 'public class Fibonacci {\n    public static int fibonacci(int n) {\n        if (n <= 1) return n;\n        return fibonacci(n-1) + fibonacci(n-2);\n    }\n    public static void main(String[] args) {\n        for (int i = 0; i < 10; i++)\n            System.out.print(fibonacci(i) + " ");\n    }\n}'
        return 'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nfor i in range(10):\n    print(fibonacci(i), end=" ")'

    # ── FACTORIAL ─────────────────────────────────────────────
    if "factorial" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}\n\nint main() {\n    cout << factorial(5) << endl;\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static int factorial(int n) {\n        if (n <= 1) return 1;\n        return n * factorial(n-1);\n    }\n    public static void main(String[] args) {\n        System.out.println(factorial(5));\n    }\n}'
        return 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial(5))'

    # ── PRIME ─────────────────────────────────────────────────
    if "prime" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nbool isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i * i <= n; i++)\n        if (n % i == 0) return false;\n    return true;\n}\n\nint main() {\n    for (int i = 2; i <= 20; i++)\n        if (isPrime(i)) cout << i << " ";\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    static boolean isPrime(int n) {\n        if (n < 2) return false;\n        for (int i = 2; i * i <= n; i++)\n            if (n % i == 0) return false;\n        return true;\n    }\n    public static void main(String[] args) {\n        for (int i = 2; i <= 20; i++)\n            if (isPrime(i)) System.out.print(i + " ");\n    }\n}'
        return 'def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True\n\nprimes = [x for x in range(2, 21) if is_prime(x)]\nprint(primes)'

    # ── PALINDROME ────────────────────────────────────────────
    if "palindrome" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nbool isPalindrome(string s) {\n    string rev = s;\n    reverse(rev.begin(), rev.end());\n    return s == rev;\n}\n\nint main() {\n    cout << isPalindrome("racecar") << endl;\n    cout << isPalindrome("hello") << endl;\n    return 0;\n}'
        return 'def is_palindrome(s):\n    return s == s[::-1]\n\nprint(is_palindrome("racecar"))  # True\nprint(is_palindrome("hello"))    # False'

    # ── ARMSTRONG ─────────────────────────────────────────────
    if "armstrong" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <cmath>\nusing namespace std;\n\nbool isArmstrong(int n) {\n    int temp = n, sum = 0, d = to_string(n).length();\n    while (temp > 0) { sum += pow(temp % 10, d); temp /= 10; }\n    return sum == n;\n}\n\nint main() {\n    cout << isArmstrong(153) << endl;\n    return 0;\n}'
        return 'def is_armstrong(n):\n    d = len(str(n))\n    return sum(int(x)**d for x in str(n)) == n\n\nprint(is_armstrong(153))  # True\nprint(is_armstrong(123))  # False'

    # ── GCD / HCF / LCM ──────────────────────────────────────
    if "lcm" in p or "least common" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint gcd(int a, int b) { return b == 0 ? a : gcd(b, a%b); }\nint lcm(int a, int b) { return a / gcd(a, b) * b; }\n\nint main() {\n    cout << "LCM: " << lcm(4, 6) << endl;\n    return 0;\n}'
        return 'import math\n\ndef lcm(a, b):\n    return abs(a * b) // math.gcd(a, b)\n\nprint(f"LCM: {lcm(4, 6)}")'

    if "gcd" in p or "hcf" in p or "greatest common" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint gcd(int a, int b) {\n    return b == 0 ? a : gcd(b, a % b);\n}\n\nint main() {\n    cout << "GCD: " << gcd(48, 18) << endl;\n    return 0;\n}'
        return 'def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n\nprint(f"GCD: {gcd(48, 18)}")'

    # ── POWER ─────────────────────────────────────────────────
    if "power" in p or "exponent" in p or ("square" in p and "number" in p):
        if lang == "cpp":
            return '#include <iostream>\n#include <cmath>\nusing namespace std;\n\nint main() {\n    cout << pow(2, 10) << endl;\n    return 0;\n}'
        return 'def power(base, exp):\n    return base ** exp\n\nprint(power(2, 10))  # 1024'

    # ── SQUARE ROOT ───────────────────────────────────────────
    if "square root" in p or "sqrt" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <cmath>\nusing namespace std;\n\nint main() {\n    cout << sqrt(25) << endl;\n    return 0;\n}'
        return 'import math\nprint(math.sqrt(25))  # 5.0'

    # ── COUNT VOWELS ──────────────────────────────────────────
    if "vowel" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint countVowels(string s) {\n    int count = 0;\n    for (char c : s)\n        if (string("aeiouAEIOU").find(c) != string::npos) count++;\n    return count;\n}\n\nint main() {\n    cout << countVowels("Hello World") << endl;\n    return 0;\n}'
        return 'def count_vowels(s):\n    return sum(1 for c in s.lower() if c in "aeiou")\n\nprint(count_vowels("Hello World"))  # 3'

    # ── COUNT CONSONANTS ──────────────────────────────────────
    if "consonant" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint countConsonants(string s) {\n    int count = 0;\n    for (char c : s)\n        if (isalpha(c) && string("aeiouAEIOU").find(c) == string::npos) count++;\n    return count;\n}\n\nint main() {\n    cout << countConsonants("Hello World") << endl;\n    return 0;\n}'
        return 'def count_consonants(s):\n    return sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")\n\nprint(count_consonants("Hello World"))  # 7'

    # ── STRING LENGTH ─────────────────────────────────────────
    if ("length" in p or "size" in p or "count" in p) and ("string" in p or "str" in p or "word" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    string s = "hello";\n    cout << "Length: " << s.length() << endl;\n    return 0;\n}'
        return 'def string_length(s):\n    return len(s)\n\nprint(string_length("hello"))  # 5'

    # ── STRING UPPERCASE / LOWERCASE ─────────────────────────
    if "uppercase" in p or "upper case" in p or "to upper" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s = "hello world";\n    transform(s.begin(), s.end(), s.begin(), ::toupper);\n    cout << s << endl;\n    return 0;\n}'
        return 's = "hello world"\nprint(s.upper())'

    if "lowercase" in p or "lower case" in p or "to lower" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s = "HELLO WORLD";\n    transform(s.begin(), s.end(), s.begin(), ::tolower);\n    cout << s << endl;\n    return 0;\n}'
        return 's = "HELLO WORLD"\nprint(s.lower())'

    # ── STRING CONCATENATION ──────────────────────────────────
    if "concatenat" in p or ("join" in p and "string" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    string s1 = "Hello";\n    string s2 = " World";\n    string result = s1 + s2;\n    cout << result << endl;\n    return 0;\n}'
        return 's1 = "Hello"\ns2 = " World"\nresult = s1 + s2\nprint(result)'

    # ── CHECK ANAGRAM ─────────────────────────────────────────
    if "anagram" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\nusing namespace std;\n\nbool isAnagram(string s1, string s2) {\n    sort(s1.begin(), s1.end());\n    sort(s2.begin(), s2.end());\n    return s1 == s2;\n}\n\nint main() {\n    cout << isAnagram("listen", "silent") << endl;\n    return 0;\n}'
        return 'def is_anagram(s1, s2):\n    return sorted(s1.lower()) == sorted(s2.lower())\n\nprint(is_anagram("listen", "silent"))  # True'

    # ── MATRIX ────────────────────────────────────────────────
    if "matrix" in p and ("multipl" in p or "product" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int a[2][2] = {{1,2},{3,4}};\n    int b[2][2] = {{5,6},{7,8}};\n    int c[2][2] = {{0,0},{0,0}};\n    for (int i=0;i<2;i++)\n        for (int j=0;j<2;j++)\n            for (int k=0;k<2;k++)\n                c[i][j] += a[i][k]*b[k][j];\n    for (int i=0;i<2;i++) {\n        for (int j=0;j<2;j++) cout << c[i][j] << " ";\n        cout << endl;\n    }\n    return 0;\n}'
        return 'def matrix_multiply(A, B):\n    rows_A, cols_A = len(A), len(A[0])\n    cols_B = len(B[0])\n    C = [[0]*cols_B for _ in range(rows_A)]\n    for i in range(rows_A):\n        for j in range(cols_B):\n            for k in range(cols_A):\n                C[i][j] += A[i][k] * B[k][j]\n    return C\n\nA = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nprint(matrix_multiply(A, B))'

    if "matrix" in p and ("transpose" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int a[3][3] = {{1,2,3},{4,5,6},{7,8,9}};\n    for (int i=0;i<3;i++) {\n        for (int j=0;j<3;j++) cout << a[j][i] << " ";\n        cout << endl;\n    }\n    return 0;\n}'
        return 'matrix = [[1,2,3],[4,5,6],[7,8,9]]\ntranspose = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]\nfor row in transpose:\n    print(row)'

    if "matrix" in p and ("add" in p or "addition" in p or "sum" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int a[2][2] = {{1,2},{3,4}};\n    int b[2][2] = {{5,6},{7,8}};\n    for (int i=0;i<2;i++) {\n        for (int j=0;j<2;j++) cout << a[i][j]+b[i][j] << " ";\n        cout << endl;\n    }\n    return 0;\n}'
        return 'A = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nresult = [[A[i][j]+B[i][j] for j in range(2)] for i in range(2)]\nfor row in result:\n    print(row)'

    # ── SEARCH ────────────────────────────────────────────────
    if "linear search" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint linearSearch(int arr[], int n, int target) {\n    for (int i = 0; i < n; i++)\n        if (arr[i] == target) return i;\n    return -1;\n}\n\nint main() {\n    int arr[] = {2, 4, 6, 8, 10};\n    cout << linearSearch(arr, 5, 6) << endl;\n    return 0;\n}'
        return 'def linear_search(arr, target):\n    for i, val in enumerate(arr):\n        if val == target:\n            return i\n    return -1\n\nprint(linear_search([2, 4, 6, 8, 10], 6))  # 2'

    if "binary search" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint binarySearch(int arr[], int n, int target) {\n    int l=0, r=n-1;\n    while (l<=r) {\n        int mid = l+(r-l)/2;\n        if (arr[mid]==target) return mid;\n        if (arr[mid]<target) l=mid+1;\n        else r=mid-1;\n    }\n    return -1;\n}\n\nint main() {\n    int arr[] = {1,3,5,7,9};\n    cout << binarySearch(arr,5,7) << endl;\n    return 0;\n}'
        return 'def binary_search(arr, target):\n    left, right = 0, len(arr)-1\n    while left <= right:\n        mid = (left+right)//2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: left = mid+1\n        else: right = mid-1\n    return -1\n\nprint(binary_search([1,3,5,7,9], 7))'

    # ── SORTING ───────────────────────────────────────────────
    if "bubble sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nvoid bubbleSort(int arr[], int n) {\n    for (int i=0;i<n-1;i++)\n        for (int j=0;j<n-i-1;j++)\n            if (arr[j]>arr[j+1]) swap(arr[j],arr[j+1]);\n}\n\nint main() {\n    int arr[] = {64,34,25,12,22};\n    bubbleSort(arr,5);\n    for (int i=0;i<5;i++) cout << arr[i] << " ";\n    return 0;\n}'
        return 'def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n-1):\n        for j in range(n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j],arr[j+1] = arr[j+1],arr[j]\n    return arr\n\nprint(bubble_sort([64,34,25,12,22]))'

    if "selection sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nvoid selectionSort(int arr[], int n) {\n    for (int i=0;i<n-1;i++) {\n        int minIdx=i;\n        for (int j=i+1;j<n;j++)\n            if (arr[j]<arr[minIdx]) minIdx=j;\n        swap(arr[i],arr[minIdx]);\n    }\n}\n\nint main() {\n    int arr[] = {64,25,12,22,11};\n    selectionSort(arr,5);\n    for (int i=0;i<5;i++) cout << arr[i] << " ";\n    return 0;\n}'
        return 'def selection_sort(arr):\n    for i in range(len(arr)):\n        min_idx = i\n        for j in range(i+1, len(arr)):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr\n\nprint(selection_sort([64,25,12,22,11]))'

    if "insertion sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nvoid insertionSort(int arr[], int n) {\n    for (int i=1;i<n;i++) {\n        int key=arr[i], j=i-1;\n        while (j>=0 && arr[j]>key) { arr[j+1]=arr[j]; j--; }\n        arr[j+1]=key;\n    }\n}\n\nint main() {\n    int arr[] = {12,11,13,5,6};\n    insertionSort(arr,5);\n    for (int i=0;i<5;i++) cout << arr[i] << " ";\n    return 0;\n}'
        return 'def insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i-1\n        while j >= 0 and arr[j] > key:\n            arr[j+1] = arr[j]\n            j -= 1\n        arr[j+1] = key\n    return arr\n\nprint(insertion_sort([12,11,13,5,6]))'

    if "merge sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nvoid merge(int arr[],int l,int m,int r) {\n    int n1=m-l+1,n2=r-m;\n    int L[n1],R[n2];\n    for(int i=0;i<n1;i++) L[i]=arr[l+i];\n    for(int i=0;i<n2;i++) R[i]=arr[m+1+i];\n    int i=0,j=0,k=l;\n    while(i<n1&&j<n2) arr[k++]=(L[i]<=R[j])?L[i++]:R[j++];\n    while(i<n1) arr[k++]=L[i++];\n    while(j<n2) arr[k++]=R[j++];\n}\n\nvoid mergeSort(int arr[],int l,int r) {\n    if(l<r) { int m=l+(r-l)/2; mergeSort(arr,l,m); mergeSort(arr,m+1,r); merge(arr,l,m,r); }\n}\n\nint main() {\n    int arr[]={12,11,13,5,6,7};\n    mergeSort(arr,0,5);\n    for(int i=0;i<6;i++) cout<<arr[i]<<" ";\n    return 0;\n}'
        return 'def merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]: result.append(left[i]); i+=1\n        else: result.append(right[j]); j+=1\n    result.extend(left[i:]); result.extend(right[j:])\n    return result\n\nprint(merge_sort([12,11,13,5,6,7]))'

    if "quick sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint partition(int arr[],int low,int high) {\n    int pivot=arr[high],i=low-1;\n    for(int j=low;j<high;j++)\n        if(arr[j]<=pivot) swap(arr[++i],arr[j]);\n    swap(arr[i+1],arr[high]);\n    return i+1;\n}\n\nvoid quickSort(int arr[],int low,int high) {\n    if(low<high) { int pi=partition(arr,low,high); quickSort(arr,low,pi-1); quickSort(arr,pi+1,high); }\n}\n\nint main() {\n    int arr[]={10,7,8,9,1,5};\n    quickSort(arr,0,5);\n    for(int i=0;i<6;i++) cout<<arr[i]<<" ";\n    return 0;\n}'
        return 'def quick_sort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr)//2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n\nprint(quick_sort([10,7,8,9,1,5]))'

    if "heap sort" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nvoid heapify(int arr[], int n, int i) {\n    int largest=i, l=2*i+1, r=2*i+2;\n    if(l<n && arr[l]>arr[largest]) largest=l;\n    if(r<n && arr[r]>arr[largest]) largest=r;\n    if(largest!=i) { swap(arr[i],arr[largest]); heapify(arr,n,largest); }\n}\n\nvoid heapSort(int arr[], int n) {\n    for(int i=n/2-1;i>=0;i--) heapify(arr,n,i);\n    for(int i=n-1;i>0;i--) { swap(arr[0],arr[i]); heapify(arr,i,0); }\n}\n\nint main() {\n    int arr[]={12,11,13,5,6,7};\n    heapSort(arr,6);\n    for(int i=0;i<6;i++) cout<<arr[i]<<" ";\n    return 0;\n}'
        return 'def heapify(arr, n, i):\n    largest = i\n    l, r = 2*i+1, 2*i+2\n    if l < n and arr[l] > arr[largest]: largest = l\n    if r < n and arr[r] > arr[largest]: largest = r\n    if largest != i:\n        arr[i], arr[largest] = arr[largest], arr[i]\n        heapify(arr, n, largest)\n\ndef heap_sort(arr):\n    n = len(arr)\n    for i in range(n//2-1, -1, -1): heapify(arr, n, i)\n    for i in range(n-1, 0, -1):\n        arr[0], arr[i] = arr[i], arr[0]\n        heapify(arr, i, 0)\n    return arr\n\nprint(heap_sort([12,11,13,5,6,7]))'

    if "sort" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <algorithm>\n#include <vector>\nusing namespace std;\n\nint main() {\n    vector<int> arr = {5,3,1,4,2};\n    sort(arr.begin(), arr.end());\n    for (int x : arr) cout << x << " ";\n    return 0;\n}'
        return 'arr = [5,3,1,4,2]\narr.sort()\nprint(arr)'

    # ── DATA STRUCTURES ───────────────────────────────────────
    if "queue" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <queue>\nusing namespace std;\n\nint main() {\n    queue<int> q;\n    q.push(1); q.push(2); q.push(3);\n    while (!q.empty()) { cout << q.front() << " "; q.pop(); }\n    return 0;\n}'
        return 'from collections import deque\n\nqueue = deque()\nqueue.append(1)\nqueue.append(2)\nqueue.append(3)\n\nwhile queue:\n    print(queue.popleft(), end=" ")'

    if "stack" in p:
        if lang == "cpp":
            return '#include <iostream>\n#include <stack>\nusing namespace std;\n\nint main() {\n    stack<int> st;\n    st.push(1); st.push(2); st.push(3);\n    while (!st.empty()) { cout << st.top() << " "; st.pop(); }\n    return 0;\n}'
        return 'stack = []\nstack.append(1)\nstack.append(2)\nstack.append(3)\n\nwhile stack:\n    print(stack.pop(), end=" ")'

    if "linked list" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nstruct Node {\n    int data;\n    Node* next;\n    Node(int val) : data(val), next(nullptr) {}\n};\n\nvoid printList(Node* head) {\n    while (head) { cout << head->data << " "; head = head->next; }\n}\n\nint main() {\n    Node* head = new Node(1);\n    head->next = new Node(2);\n    head->next->next = new Node(3);\n    printList(head);\n    return 0;\n}'
        return 'class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self): self.head = None\n\n    def append(self, data):\n        new_node = Node(data)\n        if not self.head: self.head = new_node; return\n        curr = self.head\n        while curr.next: curr = curr.next\n        curr.next = new_node\n\n    def print_list(self):\n        curr = self.head\n        while curr: print(curr.data, end=" "); curr = curr.next\n\nll = LinkedList()\nll.append(1); ll.append(2); ll.append(3)\nll.print_list()'

    if "binary tree" in p or "bst" in p or "binary search tree" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nstruct Node {\n    int data;\n    Node *left, *right;\n    Node(int val) : data(val), left(nullptr), right(nullptr) {}\n};\n\nNode* insert(Node* root, int val) {\n    if (!root) return new Node(val);\n    if (val < root->data) root->left = insert(root->left, val);\n    else root->right = insert(root->right, val);\n    return root;\n}\n\nvoid inorder(Node* root) {\n    if (!root) return;\n    inorder(root->left);\n    cout << root->data << " ";\n    inorder(root->right);\n}\n\nint main() {\n    Node* root = nullptr;\n    for (int x : {5,3,7,1,4}) root = insert(root, x);\n    inorder(root);\n    return 0;\n}'
        return 'class Node:\n    def __init__(self, val):\n        self.val = val\n        self.left = self.right = None\n\ndef insert(root, val):\n    if not root: return Node(val)\n    if val < root.val: root.left = insert(root.left, val)\n    else: root.right = insert(root.right, val)\n    return root\n\ndef inorder(root):\n    if root:\n        inorder(root.left)\n        print(root.val, end=" ")\n        inorder(root.right)\n\nroot = None\nfor x in [5,3,7,1,4]: root = insert(root, x)\ninorder(root)'

    if "hash" in p and ("map" in p or "table" in p):
        if lang == "cpp":
            return '#include <iostream>\n#include <unordered_map>\nusing namespace std;\n\nint main() {\n    unordered_map<string, int> hashMap;\n    hashMap["apple"] = 1;\n    hashMap["banana"] = 2;\n    hashMap["cherry"] = 3;\n    for (auto& pair : hashMap)\n        cout << pair.first << ": " << pair.second << endl;\n    return 0;\n}'
        return 'hash_map = {}\nhash_map["apple"] = 1\nhash_map["banana"] = 2\nhash_map["cherry"] = 3\n\nfor key, value in hash_map.items():\n    print(f"{key}: {value}")'

    # ── PATTERNS ──────────────────────────────────────────────
    if "pattern" in p or ("star" in p and any(w in p for w in ["print", "display", "draw"])):
        if "pyramid" in p or "triangle" in p:
            if lang == "cpp":
                return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int n = 5;\n    for (int i=1;i<=n;i++) {\n        for (int j=1;j<=n-i;j++) cout << " ";\n        for (int j=1;j<=2*i-1;j++) cout << "*";\n        cout << endl;\n    }\n    return 0;\n}'
            return 'n = 5\nfor i in range(1, n+1):\n    print(" "*(n-i) + "*"*(2*i-1))'
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int n = 5;\n    for (int i=1;i<=n;i++) {\n        for (int j=1;j<=i;j++) cout << "* ";\n        cout << endl;\n    }\n    return 0;\n}'
        return 'n = 5\nfor i in range(1, n+1):\n    print("* " * i)'

    if "number pattern" in p or ("number" in p and "pattern" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int n = 5;\n    for (int i=1;i<=n;i++) {\n        for (int j=1;j<=i;j++) cout << j << " ";\n        cout << endl;\n    }\n    return 0;\n}'
        return 'n = 5\nfor i in range(1, n+1):\n    print(*range(1, i+1))'

    # ── CALCULATOR ────────────────────────────────────────────
    if "calculator" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    double a, b;\n    char op;\n    cin >> a >> op >> b;\n    if (op=="+") cout << a+b;\n    else if (op=="-") cout << a-b;\n    else if (op=="*") cout << a*b;\n    else if (op=="/" && b!=0) cout << a/b;\n    else cout << "Error";\n    return 0;\n}'
        return 'def calculator(a, op, b):\n    ops = {"+": a+b, "-": a-b, "*": a*b, "/": a/b if b!=0 else "Error"}\n    return ops.get(op, "Invalid operator")\n\nprint(calculator(10, "+", 5))\nprint(calculator(10, "/", 2))'

    # ── NUMBER CONVERSION ─────────────────────────────────────
    if "binary" in p and ("decimal" in p or "convert" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint binaryToDecimal(string binary) {\n    int decimal = 0, base = 1;\n    for (int i = binary.length()-1; i >= 0; i--) {\n        if (binary[i] == "1") decimal += base;\n        base *= 2;\n    }\n    return decimal;\n}\n\nint main() {\n    cout << binaryToDecimal("1010") << endl;\n    return 0;\n}'
        return 'def binary_to_decimal(binary):\n    return int(binary, 2)\n\ndef decimal_to_binary(n):\n    return bin(n)[2:]\n\nprint(binary_to_decimal("1010"))  # 10\nprint(decimal_to_binary(10))      # 1010'

    # ── LOOPS ─────────────────────────────────────────────────
    if "for loop" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    for (int i = 0; i < 5; i++) {\n        cout << "Iteration: " << i << endl;\n    }\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static void main(String[] args) {\n        for (int i = 0; i < 5; i++) {\n            System.out.println("Iteration: " + i);\n        }\n    }\n}'
        return 'for i in range(5):\n    print(f"Iteration: {i}")'

    if "while loop" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    int i = 0;\n    while (i < 5) {\n        cout << "i = " << i << endl;\n        i++;\n    }\n    return 0;\n}'
        return 'i = 0\nwhile i < 5:\n    print(f"i = {i}")\n    i += 1'

    # ── RECURSION ─────────────────────────────────────────────
    if "recursion" in p or "recursive" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint sum(int n) {\n    if (n <= 0) return 0;\n    return n + sum(n - 1);\n}\n\nint main() {\n    cout << "Sum 1 to 10: " << sum(10) << endl;\n    return 0;\n}'
        return 'def sum_recursive(n):\n    if n <= 0:\n        return 0\n    return n + sum_recursive(n - 1)\n\nprint(f"Sum 1 to 10: {sum_recursive(10)}")'

    # ── OOP ───────────────────────────────────────────────────
    if "class" in p and ("object" in p or "oop" in p or "create" in p):
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nclass Animal {\npublic:\n    string name;\n    int age;\n\n    Animal(string n, int a) : name(n), age(a) {}\n\n    void speak() {\n        cout << name << " says hello!" << endl;\n    }\n};\n\nint main() {\n    Animal dog("Rex", 3);\n    dog.speak();\n    cout << "Age: " << dog.age << endl;\n    return 0;\n}'
        if lang == "java":
            return 'public class Animal {\n    String name;\n    int age;\n\n    Animal(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n\n    void speak() {\n        System.out.println(name + " says hello!");\n    }\n\n    public static void main(String[] args) {\n        Animal dog = new Animal("Rex", 3);\n        dog.speak();\n    }\n}'
        return 'class Animal:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def speak(self):\n        print(f"{self.name} says hello!")\n\ndog = Animal("Rex", 3)\ndog.speak()\nprint(f"Age: {dog.age}")'

    if "inheritance" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nclass Animal {\npublic:\n    void eat() { cout << "Animal eats" << endl; }\n};\n\nclass Dog : public Animal {\npublic:\n    void bark() { cout << "Dog barks" << endl; }\n};\n\nint main() {\n    Dog d;\n    d.eat();\n    d.bark();\n    return 0;\n}'
        if lang == "java":
            return 'class Animal {\n    void eat() { System.out.println("Animal eats"); }\n}\n\nclass Dog extends Animal {\n    void bark() { System.out.println("Dog barks"); }\n\n    public static void main(String[] args) {\n        Dog d = new Dog();\n        d.eat();\n        d.bark();\n    }\n}'
        return 'class Animal:\n    def eat(self):\n        print("Animal eats")\n\nclass Dog(Animal):\n    def bark(self):\n        print("Dog barks")\n\nd = Dog()\nd.eat()\nd.bark()'

    # ── FILE HANDLING ─────────────────────────────────────────
    if "file" in p and ("read" in p or "write" in p or "open" in p):
        if "write" in p:
            if lang == "cpp":
                return '#include <iostream>\n#include <fstream>\nusing namespace std;\n\nint main() {\n    ofstream file("output.txt");\n    file << "Hello, World!" << endl;\n    file.close();\n    cout << "File written successfully" << endl;\n    return 0;\n}'
            return 'with open("output.txt", "w") as f:\n    f.write("Hello, World!\\n")\nprint("File written successfully")'
        if lang == "cpp":
            return '#include <iostream>\n#include <fstream>\n#include <string>\nusing namespace std;\n\nint main() {\n    ifstream file("input.txt");\n    string line;\n    while (getline(file, line))\n        cout << line << endl;\n    file.close();\n    return 0;\n}'
        return 'with open("input.txt", "r") as f:\n    content = f.read()\nprint(content)'

    # ── EXCEPTION HANDLING ────────────────────────────────────
    if "exception" in p or "try" in p or "catch" in p or "error handling" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint divide(int a, int b) {\n    if (b == 0) throw runtime_error("Division by zero!");\n    return a / b;\n}\n\nint main() {\n    try {\n        cout << divide(10, 2) << endl;\n        cout << divide(10, 0) << endl;\n    } catch (exception& e) {\n        cout << "Error: " << e.what() << endl;\n    }\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    public static void main(String[] args) {\n        try {\n            int result = 10 / 0;\n        } catch (ArithmeticException e) {\n            System.out.println("Error: " + e.getMessage());\n        } finally {\n            System.out.println("Done");\n        }\n    }\n}'
        return 'try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"Error: {e}")\nexcept Exception as e:\n    print(f"Unexpected error: {e}")\nfinally:\n    print("Done")'

    # ── FUNCTION / METHOD ─────────────────────────────────────
    if "function" in p or "method" in p or "def " in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint add(int a, int b) {\n    return a + b;\n}\n\nint multiply(int a, int b) {\n    return a * b;\n}\n\nint main() {\n    cout << add(5, 3) << endl;\n    cout << multiply(5, 3) << endl;\n    return 0;\n}'
        if lang == "java":
            return 'public class Main {\n    static int add(int a, int b) { return a + b; }\n    static int multiply(int a, int b) { return a * b; }\n\n    public static void main(String[] args) {\n        System.out.println(add(5, 3));\n        System.out.println(multiply(5, 3));\n    }\n}'
        return 'def add(a, b):\n    return a + b\n\ndef multiply(a, b):\n    return a * b\n\nprint(add(5, 3))\nprint(multiply(5, 3))'

    # ── DICTIONARY / MAP ──────────────────────────────────────
    if "dictionary" in p or ("dict" in p and lang == "python"):
        return 'student = {\n    "name": "Alice",\n    "age": 20,\n    "grade": "A"\n}\n\nprint(student["name"])\nfor key, value in student.items():\n    print(f"{key}: {value}")'

    # ── LIST COMPREHENSION ────────────────────────────────────
    if "list comprehension" in p or "comprehension" in p:
        return 'numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\nsquares = [x**2 for x in numbers]\nevens = [x for x in numbers if x % 2 == 0]\npairs = [(x, y) for x in range(3) for y in range(3)]\n\nprint("Squares:", squares)\nprint("Evens:", evens)\nprint("Pairs:", pairs)'

    # ── LAMBDA ────────────────────────────────────────────────
    if "lambda" in p:
        return 'square = lambda x: x ** 2\nadd = lambda a, b: a + b\nfilter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))\n\nprint(square(5))\nprint(add(3, 4))\nprint(filter_evens([1,2,3,4,5,6]))'

    # ── DECORATORS ────────────────────────────────────────────
    if "decorator" in p:
        return 'def my_decorator(func):\n    def wrapper(*args, **kwargs):\n        print("Before function call")\n        result = func(*args, **kwargs)\n        print("After function call")\n        return result\n    return wrapper\n\n@my_decorator\ndef greet(name):\n    print(f"Hello, {name}!")\n\ngreet("Alice")'

    # ── GENERATORS ────────────────────────────────────────────
    if "generator" in p or "yield" in p:
        return 'def count_up(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\n\nfor num in count_up(5):\n    print(num)\n\n# Generator expression\nsquares = (x**2 for x in range(5))\nprint(list(squares))'

    # ── TYPE CONVERSION ───────────────────────────────────────
    if "type conversion" in p or "type casting" in p or "casting" in p:
        if lang == "cpp":
            return '#include <iostream>\nusing namespace std;\n\nint main() {\n    double d = 3.14;\n    int i = (int)d;\n    cout << "double: " << d << endl;\n    cout << "int: " << i << endl;\n    return 0;\n}'
        return 'x = 3.14\nprint(int(x))   # 3\nprint(str(x))   # "3.14"\nprint(float("3.14"))  # 3.14\nprint(bool(0))  # False\nprint(bool(1))  # True'

    # ── DEFAULT FALLBACK ──────────────────────────────────────
    if lang == "cpp":
        return f'#include <iostream>\nusing namespace std;\n\n// Program to: {prompt}\nint main() {{\n    // TODO: Implement - {prompt}\n    cout << "Running: {prompt}" << endl;\n    return 0;\n}}'
    if lang == "java":
        return f'public class Main {{\n    // Program to: {prompt}\n    public static void main(String[] args) {{\n        // TODO: Implement - {prompt}\n        System.out.println("Running: {prompt}");\n    }}\n}}'
    return f'# Program to: {prompt}\ndef main():\n    # TODO: Implement - {prompt}\n    print("Running: {prompt}")\n\nmain()'