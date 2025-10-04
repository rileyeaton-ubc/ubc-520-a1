import time
import matplotlib.pyplot as plt
from pybloom_live import BloomFilter
from cuckoo_filter import CuckooFilter

class LoginChecker:
    """
    Abstract base class for login checking implementations.
    Tracks performance metrics including comparisons and login count.
    """
    def __init__(self):
        """
        Input: None
        Output: None
        Initializes comparison counter and login count to 0.
        """
        self.comparisons = 0
        self.login_count = 0

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Abstract method to be implemented by subclasses.
        """
        raise NotImplementedError

    def check_exists(self, name):
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Abstract method to be implemented by subclasses.
        """
        raise NotImplementedError

    def reset_stats(self):
        """
        Input: None
        Output: None
        Resets the comparison counter to 0.
        """
        self.comparisons = 0

class ListLinearSearchChecker(LoginChecker):
    """
    Login checker using a list with linear search.
    Time complexity: O(n) for both add and lookup operations.
    """
    def __init__(self):
        """
        Input: None
        Output: None
        Initializes an empty list to store logins.
        """
        super().__init__()
        self.logins = []

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Performs linear search to check for duplicates, then appends if unique.
        """
        for login in self.logins:
            self.comparisons += 1
            if login == name:
                return False
        self.logins.append(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Performs linear search through the list to find the name.
        """
        for login in self.logins:
            self.comparisons += 1
            if login == name:
                return True
        return False

class SortedArrayBinarySearchChecker(LoginChecker):
    """
    Login checker using a sorted array with binary search.
    Time complexity: O(log n) for search, O(n) for insertion due to array shifting.
    """
    def __init__(self):
        """
        Input: None
        Output: None
        Initializes an empty sorted list to store logins.
        """
        super().__init__()
        self.logins = []

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Uses binary search to find insertion position, maintains sorted order.
        """
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
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Uses binary search to efficiently locate the name in sorted array.
        """
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
    """
    Login checker using a hash table (Python set).
    Time complexity: O(1) average case for both add and lookup operations.
    """
    def __init__(self):
        """
        Input: None
        Output: None
        Initializes an empty set to store logins using hash-based lookup.
        """
        super().__init__()
        self.logins = set()

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Uses hash table for O(1) duplicate checking, then adds to set.
        """
        self.comparisons += 1
        if name in self.logins:
            return False
        self.logins.add(name)
        self.login_count += 1
        return True

    def check_exists(self, name):
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Uses hash table for O(1) average case lookup.
        """
        self.comparisons += 1
        return name in self.logins

class BloomFilterChecker(LoginChecker):
    """
    Login checker using a Bloom filter with a backing set.
    Bloom filter provides fast negative lookups with possible false positives.
    Time complexity: O(1) for bloom filter checks, O(1) for set verification.
    """
    def __init__(self, capacity=1000000, error_rate=0.001):
        """
        Input: capacity (int) - Maximum number of elements, error_rate (float) - False positive rate
        Output: None
        Initializes a Bloom filter and backing set for duplicate checking.
        """
        super().__init__()
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.logins = set()

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Checks Bloom filter first, then verifies with set to handle false positives.
        """
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
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Uses Bloom filter for fast negative checks, verifies positives with set.
        """
        self.comparisons += 1
        if name not in self.bloom:
            return False
        self.comparisons += 1
        return name in self.logins

class CuckooFilterChecker(LoginChecker):
    """
    Login checker using a Cuckoo filter with a backing set.
    Cuckoo filter provides fast lookups with possible false positives and supports deletion.
    Time complexity: O(1) for cuckoo filter checks, O(1) for set verification.
    """
    def __init__(self, capacity=1000000, error_rate=0.001):
        """
        Input: capacity (int) - Maximum number of elements (unused), error_rate (float) - False positive rate (unused)
        Output: None
        Initializes a Cuckoo filter and backing set for duplicate checking.
        """
        super().__init__()
        self.cuckoo = CuckooFilter(table_size=10000, bucket_size=4, fingerprint_size=8)
        self.logins = set()

    def add_login(self, name):
        """
        Input: name (str) - The login name to add
        Output: bool - True if added successfully, False if already exists
        Checks Cuckoo filter first, then verifies with set to handle false positives.
        """
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
        """
        Input: name (str) - The login name to check
        Output: bool - True if login exists, False otherwise
        Uses Cuckoo filter for fast negative checks, verifies positives with set.
        """
        self.comparisons += 1
        if name not in self.cuckoo:
            return False
        self.comparisons += 1
        return name in self.logins

def load_logins_from_file(filename):
    """
    Input: filename (str) - Path to file containing login names (one per line)
    Output: list[str] - List of login names with whitespace stripped
    Reads login names from a file, removing empty lines and whitespace.
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def run_test(checker_class, num_logins, num_lookups, login_file=None):
    """
    Input:
        - checker_class (class) - LoginChecker subclass to test
        - num_logins (int) - Number of logins to add
        - num_lookups (int) - Number of lookup operations to perform
        - login_file (str, optional) - Path to file with login data
    Output: dict - Performance metrics including times and comparison counts
    Benchmarks a login checker implementation with add and lookup operations.
    """
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
    """
    Input: results (dict) - Performance metrics from run_test
    Output: None
    Prints formatted performance results including times and comparison counts.
    """
    print(f"\n{results['algorithm']}")
    print(f"Size: {results['num_logins']}")
    print(f"Add time: {results['add_time']:.4f}s")
    print(f"Add comparisons: {results['add_comparisons']:,} (avg {results['add_comparisons']/results['num_logins']:.1f})")
    print(f"Lookup time: {results['lookup_time']:.4f}s")
    print(f"Lookup comparisons: {results['lookup_comparisons']:,} (avg {results['lookup_comparisons']/results['num_lookups']:.1f})")

def main():
    """
    Input: None
    Output: None
    Main function that runs performance tests on all checker implementations,
    prints results, and generates performance comparison plots.
    """
    # Define test configurations
    test_sizes = [100, 500, 1000, 2000, 5000]
    DATA_PATH = "./data/logins.txt"
    IMG_PATH = "./img/login_checker_performance.png"
    IMG_PATH_ZOOMED = "./img/login_checker_performance_zoomed.png"
    IMG_PATH_COMPARISONS = "./img/login_checker_comparisons.png"
    IMG_PATH_COMPARISONS_ZOOMED = "./img/login_checker_comparisons_zoomed.png"
    all_results = []

    # Run performance tests for each size and algorithm
    for size in test_sizes:
        for checker_class in [ListLinearSearchChecker, SortedArrayBinarySearchChecker, HashTableChecker, BloomFilterChecker, CuckooFilterChecker]:
            results = run_test(checker_class, size, size, login_file=DATA_PATH)
            all_results.append(results)
            print_results(results)

    # Set up plotting configuration    
    algorithms = ['SortedArrayBinarySearchChecker', 'HashTableChecker', 'BloomFilterChecker', 'CuckooFilterChecker']
    algorithms.append('ListLinearSearchChecker') # Only add if you want to be waiting a long time (need a baseline)
    colors = ['red', 'blue', 'green', 'purple', 'orange']

    # Create side-by-side plots for add and lookup times
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot performance data for each algorithm
    for i, algo in enumerate(algorithms):
        algo_results = [r for r in all_results if r['algorithm'] == algo]
        sizes = [r['num_logins'] for r in algo_results]
        add_times = [r['add_time'] for r in algo_results]
        lookup_times = [r['lookup_time'] for r in algo_results]

        # Plot add times on left subplot
        ax1.plot(sizes, add_times, marker='o', label=algo.replace('Checker', ''), color=colors[i])
        # Plot lookup times on right subplot
        ax2.plot(sizes, lookup_times, marker='o', label=algo.replace('Checker', ''), color=colors[i])

    # Configure add time plot
    ax1.set_xlabel('Number of logins')
    ax1.set_ylabel('Time (s)')
    ax1.set_title('Add Time')
    ax1.legend()
    ax1.grid(True)

    # Configure lookup time plot
    ax2.set_xlabel('Number of logins')
    ax2.set_ylabel('Time (s)')
    ax2.set_title('Lookup Time')
    ax2.legend()
    ax2.grid(True)

    # Save the final plot
    plt.tight_layout()
    plt.savefig(IMG_PATH)
    print(f'\nFull plot saved to {IMG_PATH}')

    # Create zoomed-in plot without ListLinearSearch for better visibility of fast algorithms
    algorithms_zoomed = ['SortedArrayBinarySearchChecker', 'HashTableChecker', 'BloomFilterChecker', 'CuckooFilterChecker']
    colors_zoomed = ['blue', 'green', 'purple', 'orange']

    fig_zoomed, (ax1_zoomed, ax2_zoomed) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot performance data for fast algorithms only
    for i, algo in enumerate(algorithms_zoomed):
        algo_results = [r for r in all_results if r['algorithm'] == algo]
        sizes = [r['num_logins'] for r in algo_results]
        add_times = [r['add_time'] for r in algo_results]
        lookup_times = [r['lookup_time'] for r in algo_results]

        # Plot add times on left subplot
        ax1_zoomed.plot(sizes, add_times, marker='o', label=algo.replace('Checker', ''), color=colors_zoomed[i])
        # Plot lookup times on right subplot
        ax2_zoomed.plot(sizes, lookup_times, marker='o', label=algo.replace('Checker', ''), color=colors_zoomed[i])

    # Configure add time plot
    ax1_zoomed.set_xlabel('Number of logins')
    ax1_zoomed.set_ylabel('Time (s)')
    ax1_zoomed.set_title('Add Time (Zoomed - Fast Algorithms Only)')
    ax1_zoomed.legend()
    ax1_zoomed.grid(True)

    # Configure lookup time plot
    ax2_zoomed.set_xlabel('Number of logins')
    ax2_zoomed.set_ylabel('Time (s)')
    ax2_zoomed.set_title('Lookup Time (Zoomed - Fast Algorithms Only)')
    ax2_zoomed.legend()
    ax2_zoomed.grid(True)

    # Save the zoomed plot
    plt.tight_layout()
    plt.savefig(IMG_PATH_ZOOMED)
    print(f'Zoomed plot saved to {IMG_PATH_ZOOMED}')

    # Create comparison count plots (theoretical complexity validation)
    algorithms_all = ['ListLinearSearchChecker', 'SortedArrayBinarySearchChecker', 'HashTableChecker', 'BloomFilterChecker', 'CuckooFilterChecker']

    fig_comp, (ax1_comp, ax2_comp) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot comparison counts for all algorithms
    for i, algo in enumerate(algorithms_all):
        algo_results = [r for r in all_results if r['algorithm'] == algo]
        sizes = [r['num_logins'] for r in algo_results]
        add_comparisons = [r['add_comparisons'] / r['num_logins'] for r in algo_results]  # Average per operation
        lookup_comparisons = [r['lookup_comparisons'] / r['num_lookups'] for r in algo_results]

        # Plot average comparisons
        ax1_comp.plot(sizes, add_comparisons, marker='o', label=algo.replace('Checker', ''), color=colors[i])
        ax2_comp.plot(sizes, lookup_comparisons, marker='o', label=algo.replace('Checker', ''), color=colors[i])

    # Configure comparison plots
    ax1_comp.set_xlabel('Number of logins')
    ax1_comp.set_ylabel('Average Comparisons per Operation')
    ax1_comp.set_title('Add Comparisons (Theoretical Complexity)')
    ax1_comp.legend()
    ax1_comp.grid(True)

    ax2_comp.set_xlabel('Number of logins')
    ax2_comp.set_ylabel('Average Comparisons per Operation')
    ax2_comp.set_title('Lookup Comparisons (Theoretical Complexity)')
    ax2_comp.legend()
    ax2_comp.grid(True)

    plt.tight_layout()
    plt.savefig(IMG_PATH_COMPARISONS)
    print(f'Comparison count plot saved to {IMG_PATH_COMPARISONS}')

    # Create zoomed comparison plot (without linear search)
    fig_comp_zoom, (ax1_comp_zoom, ax2_comp_zoom) = plt.subplots(1, 2, figsize=(12, 5))

    for i, algo in enumerate(algorithms_zoomed):
        algo_results = [r for r in all_results if r['algorithm'] == algo]
        sizes = [r['num_logins'] for r in algo_results]
        add_comparisons = [r['add_comparisons'] / r['num_logins'] for r in algo_results]
        lookup_comparisons = [r['lookup_comparisons'] / r['num_lookups'] for r in algo_results]

        ax1_comp_zoom.plot(sizes, add_comparisons, marker='o', label=algo.replace('Checker', ''), color=colors_zoomed[i])
        ax2_comp_zoom.plot(sizes, lookup_comparisons, marker='o', label=algo.replace('Checker', ''), color=colors_zoomed[i])

    # Configure zoomed comparison plots
    ax1_comp_zoom.set_xlabel('Number of logins')
    ax1_comp_zoom.set_ylabel('Average Comparisons per Operation')
    ax1_comp_zoom.set_title('Add Comparisons (Zoomed - Fast Algorithms)')
    ax1_comp_zoom.legend()
    ax1_comp_zoom.grid(True)

    ax2_comp_zoom.set_xlabel('Number of logins')
    ax2_comp_zoom.set_ylabel('Average Comparisons per Operation')
    ax2_comp_zoom.set_title('Lookup Comparisons (Zoomed - Fast Algorithms)')
    ax2_comp_zoom.legend()
    ax2_comp_zoom.grid(True)

    plt.tight_layout()
    plt.savefig(IMG_PATH_COMPARISONS_ZOOMED)
    print(f'Zoomed comparison count plot saved to {IMG_PATH_COMPARISONS_ZOOMED}')


if __name__ == "__main__":
    main()
