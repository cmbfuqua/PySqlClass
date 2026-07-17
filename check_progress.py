import os
import subprocess
import sys

def main():
    print("=== Curriculum Progress Board ===")
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and f.startswith('folder_')]
    folders.sort()

    total_tasks = 0
    passed_tasks = 0

    for folder in folders:
        print(f"\nChecking {folder}...")
        tests_dir = os.path.join(folder, "tests")
        if not os.path.isdir(tests_dir):
            print("  No tests folder found.")
            continue

        for test_file in ["test_practice.py", "test_assignment.py"]:
            test_path = os.path.join(tests_dir, test_file)
            if os.path.exists(test_path):
                total_tasks += 1
                result = subprocess.run([sys.executable, "-m", "pytest", test_path, "-q", "--disable-warnings"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"  [x] {test_file} PASSED")
                    passed_tasks += 1
                else:
                    print(f"  [ ] {test_file} FAILED")

    print(f"\nOverall Progress: {passed_tasks}/{total_tasks} tasks completed.")
    if total_tasks > 0:
        print(f"Completion: {int((passed_tasks / total_tasks) * 100)}%")

if __name__ == "__main__":
    main()
