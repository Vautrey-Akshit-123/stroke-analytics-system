from query_module import query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10, query_11
from dataset_module import load_data
def load_data(filename):
    """Loads data from CSV."""
    try:
        with open(filename, 'r') as f:
            headers = [h.strip().lower() for h in f.readline().strip().split(',')] # Get and clean headers
            data = {f"row_{i+1}": dict(zip(headers, [b.strip() for b in line.strip().split(',')])) # Create row dictionaries
                    for i, line in enumerate(f)}
        print(f"Loaded {len(data)} records")
        return data
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def read_csv(filename, is_multi_row=False):
    """Reads CSV into structured format."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) <= 1: return None # Handle empty or header-only files
            headers = lines[0].strip().split(',')
            if is_multi_row:
                values = [line.strip().split(',') for line in lines[1:]]
                return {h: [b[i] for b in values] for i, h in enumerate(headers)} # Column-oriented dictionary
            if len(lines) == 2: return dict(zip(headers, lines[1].strip().split(','))) # Single row dictionary
            return [dict(zip(headers, line.strip().split(','))) for line in lines[1:]] # List of row dictionaries
    except Exception:
        return None

def display_results(results, query_num):
    """Displays query results."""
    if not results:
        print("No results found\n" + "="*50)
        return
    print("="*50)
    if isinstance(results, dict):
        for a, b in results.items():
            print(f"{a}: {b}") # Print dictionary
    else:
        fields = ['id', 'age', 'gender', 'hypertension', 'stroke occurrence', 'heart disease', 'smoking status']
        widths = {f: max(len(f), max(len(str(r.get(f, ''))) for r in results)) for f in fields}
        print("|".join(f" {f:<{widths[f]}} " for f in fields)) # Print header
        print("-" * (sum(widths.values()) + 3*len(fields))) # Print separator
        for r in results:
            print("|".join(f" {r.get(f, ''):<{widths[f]}} " for f in fields)) # Print rows
    print("="*50)

def execute_query_1(data): return query_1(data)[0] and read_csv('query1_smokers_hypertension_stroke_age.csv')
def execute_query_2(data): return query_2(data)[0] and read_csv('query2_heart_disease_stroke_stats.csv')
def execute_query_3(data): return query_3(data)[0] and read_csv('query3_hypertension_age_summary.csv')
def execute_query_4(data): return query_4(data)[0] and read_csv('query4_smokers_age_summary.csv')
def execute_query_5(data): return query_5(data)[0] and read_csv('query5_residence_stroke_age_summary.csv')
def execute_query_6(data): return query_6(data)[0] and read_csv('query6_dietary_habits_stroke.csv', True)
def execute_query_7(data): return query_7(data)[0] and read_csv('query7_hypertension_stroke_patients.csv')
def execute_query_8(data): return query_8(data)[0] and read_csv('query8_hypertension_all_stroke_status.csv')
def execute_query_9(data): return query_9(data)[0] and read_csv('query9_heart_disease_stroke_patients.csv')
def execute_query_10(data): return query_10(data)[0] and read_csv('query10_age_statistics.csv')
def execute_query_11(data): return query_11(data)[0] and read_csv('query11_sleep_hours_stroke.csv', True)

def show_menu():
    """Displays the main menu."""
    data = load_data('data.csv')
    if not data: return print("Failed to load data. Exiting.")
    queries = {1: ("Smokers+hypertension+stroke", execute_query_1),
               2: ("Heart disease+stroke", execute_query_2),
               3: ("Hypertension by gender", execute_query_3),
               4: ("Smokers by stroke", execute_query_4),
               5: ("Residence by stroke", execute_query_5),
               6: ("Dietary habits", execute_query_6),
               7: ("Hypertension+stroke patients", execute_query_7),
               8: ("All hypertension", execute_query_8),
               9: ("Heart disease+stroke patients", execute_query_9),
               10: ("Age stats", execute_query_10),
               11: ("Sleep hours", execute_query_11)}
    while True:
        print("\n"+"="*50+"\nSTROKE DATA ANALYTICS\n"+"="*50)
        print("\nQueries:\n" + "\n".join(f" {i}-{desc}" for i, (desc, _) in queries.items()) + "\n 0-Exit")
        try:
            choice = int(input("\nEnter query (0-11): "))
            if choice == 0: break
            if choice in queries:
                print(f"\n{'='*50}\nQUERY {choice}: {queries[choice][0]}\n{'='*50}")
                results = queries[choice][1](data)
                if not results: print(f"Query {choice} returned no matching records")
                display_results(results, choice)
                input("\nPress Enter...")
            else: print("Invalid choice.")
        except ValueError:
            print("Enter a valid number.")

if __name__ == "__main__":
    show_menu()