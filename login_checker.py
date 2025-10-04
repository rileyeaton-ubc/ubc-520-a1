import time
import matplotlib.pyplot as plt
from pybloom_live import BloomFilter
from cuckoo_filter import CuckooFilter

class LoginChecker:
    def __init__(self):
        self.comparisons = 0
        self.login_count = 0

    def add_login(self, name):
        raise NotImplementedError

    def check_exists(self, name):
        raise NotImplementedError

    def reset_stats(self):
        self.comparisons = 0

class ListLinearSearchChecker(LoginChecker):
    def __init__(self):
        super().__init__()
        self.logins = []

    def add_login(self, name):
        for login in self.logins:
            self.comparisons += 1
            if login == name:
                return False
        self.logins.append(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        for login in self.logins:
            self.comparisons += 1
            if login == name:
                return True
        return False

class SortedArrayBinarySearchChecker(LoginChecker):
    def __init__(self):
        super().__init__()
        self.logins = []

    def add_login(self, name):
        left, right = 0, len(self.logins) - 1
        while left <= right:
            self.comparisons += 1
            mid = (left + right) // 2
            if self.logins[mid] == name:
                return False
            elif self.logins[mid] < name:
                left = mid + 1
            else:
                right = mid - 1
        self.logins.insert(left, name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        left, right = 0, len(self.logins) - 1
        while left <= right:
            self.comparisons += 1
            mid = (left + right) // 2
            if self.logins[mid] == name:
                return True
            elif self.logins[mid] < name:
                left = mid + 1
            else:
                right = mid - 1
        return False

class HashTableChecker(LoginChecker):
    def __init__(self):
        super().__init__()
        self.logins = set()

    def add_login(self, name):
        self.comparisons += 1
        if name in self.logins:
            return False
        self.logins.add(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        self.comparisons += 1
        return name in self.logins

class BloomFilterChecker(LoginChecker):
    def __init__(self, capacity=1000000, error_rate=0.001):
        super().__init__()
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.logins = set()

    def add_login(self, name):
        self.comparisons += 1
        if name in self.bloom:
            self.comparisons += 1
            if name in self.logins:
                return False
        self.bloom.add(name)
        self.logins.add(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        self.comparisons += 1
        if name not in self.bloom:
            return False
        self.comparisons += 1
        return name in self.logins

class CuckooFilterChecker(LoginChecker):
    def __init__(self, capacity=1000000, error_rate=0.001):
        super().__init__()
        self.cuckoo = CuckooFilter(table_size=10000, bucket_size=4, fingerprint_size=8)
        self.logins = set()

    def add_login(self, name):
        self.comparisons += 1
        if name in self.cuckoo:
            self.comparisons += 1
            if name in self.logins:
                return False
        self.cuckoo.insert(name)
        self.logins.add(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        self.comparisons += 1
        if name not in self.cuckoo:
            return False
        self.comparisons += 1
        return name in self.logins

def load_logins_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def run_test(checker_class, num_logins, num_lookups, login_file=None):
    checker = checker_class()

    if login_file:
        logins = load_logins_from_file(login_file)[:num_logins]
    else:
        logins = [f"user{i}" for i in range(num_logins)]

    start_time = time.time()
    for login in logins:
        checker.add_login(login)
    add_time = time.time() - start_time
    add_comparisons = checker.comparisons
    checker.reset_stats()

    lookup_names = []
    for i in range(num_lookups):
        if i % 2 == 0 and i // 2 < len(logins):
            lookup_names.append(logins[i // 2])
        else:
            lookup_names.append(f"nonexistent{i}")

    start_time = time.time()
    found_count = sum(1 for name in lookup_names if checker.check_exists(name))
    lookup_time = time.time() - start_time
    lookup_comparisons = checker.comparisons

    return {
        'algorithm': checker_class.__name__,
        'num_logins': num_logins,
        'num_lookups': num_lookups,
        'add_time': add_time,
        'add_comparisons': add_comparisons,
        'lookup_time': lookup_time,
        'lookup_comparisons': lookup_comparisons,
        'lookups_found': found_count
    }

def print_results(results):
    print(f"\n{results['algorithm']}")
    print(f"Size: {results['num_logins']}")
    print(f"Add time: {results['add_time']:.4f}s")
    print(f"Add comparisons: {results['add_comparisons']:,} (avg {results['add_comparisons']/results['num_logins']:.1f})")
    print(f"Lookup time: {results['lookup_time']:.4f}s")
    print(f"Lookup comparisons: {results['lookup_comparisons']:,} (avg {results['lookup_comparisons']/results['num_lookups']:.1f})")

def main():
    test_sizes = [100, 500, 1000, 2000, 5000]
    DATA_PATH = "./data/logins.txt"
    IMG_PATH = "./img/login_checker_performance.png"
    all_results = []

    for size in test_sizes:
        for checker_class in [ListLinearSearchChecker, SortedArrayBinarySearchChecker, HashTableChecker, BloomFilterChecker, CuckooFilterChecker]:
            results = run_test(checker_class, size, size, login_file=DATA_PATH)
            all_results.append(results)
            print_results(results)

    algorithms = ['ListLinearSearchChecker', 'SortedArrayBinarySearchChecker', 'HashTableChecker', 'BloomFilterChecker', 'CuckooFilterChecker']
    colors = ['red', 'blue', 'green', 'purple', 'orange']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for i, algo in enumerate(algorithms):
        algo_results = [r for r in all_results if r['algorithm'] == algo]
        sizes = [r['num_logins'] for r in algo_results]
        add_times = [r['add_time'] for r in algo_results]
        lookup_times = [r['lookup_time'] for r in algo_results]

        ax1.plot(sizes, add_times, marker='o', label=algo.replace('Checker', ''), color=colors[i])
        ax2.plot(sizes, lookup_times, marker='o', label=algo.replace('Checker', ''), color=colors[i])

    ax1.set_xlabel('Number of logins')
    ax1.set_ylabel('Time (s)')
    ax1.set_title('Add Time')
    ax1.legend()
    ax1.grid(True)

    ax2.set_xlabel('Number of logins')
    ax2.set_ylabel('Time (s)')
    ax2.set_title('Lookup Time')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(IMG_PATH)
    print(f'\nPlot saved to {IMG_PATH}')


if __name__ == "__main__":
    main()
