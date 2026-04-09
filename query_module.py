import sys
from collections import Counter
import dataset_module
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            headers = [h.strip().lower() for h in f.readline().strip().split(',')]
            data = {f"row_{i+1}": dict(zip(headers, [b.strip() for b in line.strip().split(',')]))
                    for i, line in enumerate(f)}
        return data
    except Exception:
        return None
    
def filter_data(data, conditions):
    filtered = []
    for row in data.values():
        match = True
        for col, val in conditions.items():
            cell_val = str(row.get(col, '')).lower().strip()
            if isinstance(val, list):
                if not any(b.lower().strip() in cell_val for b in val): match = False
            elif str(val).lower().strip() == '1' and cell_val not in ['1', 'yes', 'true']: match = False
            elif str(val).lower().strip() == '0' and cell_val not in ['0', 'no', 'false']: match = False
            elif str(val).lower().strip() not in cell_val: match = False
        if match: filtered.append(row)
    return filtered

def calc_age_stats(data):
    try:
        ages = [float(row['age']) for row in data if row.get('age') and row['age'].strip()]
        if not ages: return None
        avg = sum(ages)/len(ages)
        modal = Counter(ages).most_common(1)[0][0]
        sorted_ages = sorted(ages)
        median = (sorted_ages[len(ages)//2 - 1] + sorted_ages[len(ages)//2])/2 if len(ages)%2 == 0 else sorted_ages[len(ages)//2]
        return {'average': avg, 'modal': modal, 'median': median}
    except Exception:
        return None

def write_to_csv(filename, data):
    try:
        with open(filename, 'w') as f:
            if not data: return True
            headers = list(data.keys())
            f.write(','.join(headers) + '\n')
            if isinstance(next(iter(data.values())), list):
                for i in range(len(data[headers[0]])):
                    f.write(','.join(str(data[h][i]) for h in headers) + '\n')
            else:
                f.write(','.join(str(data[h]) for h in headers) + '\n')
        return True
    except Exception:
        return False

def query_1(data): # Smokers with hypertension and stroke
    data_q = filter_data(data, {'stroke occurrence':'1','hypertension':'1','smoking status':['1','yes','true','smokes']})
    result = calc_age_stats(data_q) or {}
    return write_to_csv('query1_smokers_hypertension_stroke_age.csv', result), len(data_q)

def query_2(data): # Heart disease and stroke stats
    data_q = filter_data(data, {'stroke occurrence':'1','heart disease':'1'})
    stats = calc_age_stats(data_q) or {}
    stats['avg_glucose'] = sum(float(r.get('average glucose level',0)) for r in data_q)/len(data_q) if data_q else 0
    return write_to_csv('query2_heart_disease_stroke_stats.csv', stats), len(data_q)

def query_3(data): # Hypertension age summary by gender and stroke
    result = {}
    for g in ['male','female']:
        for s in ['1','0']:
            data_q = filter_data(data, {'hypertension':'1','gender':g,'stroke occurrence':s})
            for a,b in (calc_age_stats(data_q) or {}).items():
                result[f'{g}_stroke_{s}_{a}'] = b
    return write_to_csv('query3_hypertension_age_summary.csv', result), sum(len(filter_data(data, {'hypertension':'1','gender':g,'stroke occurrence':s})) for g in ['male','female'] for s in ['1','0'])

def query_4(data): # Smokers age summary by stroke
    result = {}
    for s in ['1','0']:
        data_q = filter_data(data, {'smoking status':['1','yes','true','smokes'],'stroke occurrence':s})
        for a,b in (calc_age_stats(data_q) or {}).items():
            result[f'stroke_{s}_{a}'] = b
    return write_to_csv('query4_smokers_age_summary.csv', result), sum(len(filter_data(data, {'smoking status':['1','yes','true','smokes'],'stroke occurrence':s})) for s in ['1','0'])

def query_5(data): # Residence type stroke age summary
    result = {}
    for r in ['urban','rural']:
        data_q = filter_data(data, {'residence type':r,'stroke occurrence':'1'})
        for a,b in (calc_age_stats(data_q) or {}).items():
            result[f'{r}_{a}'] = b
    return write_to_csv('query5_residence_stroke_age_summary.csv', result), sum(len(filter_data(data, {'residence type':r,'stroke occurrence':'1'})) for r in ['urban','rural'])

def query_6(data): # Dietary habits by stroke
    stroke_habits = set(r['dietary habits'] for r in data.values() if str(r.get('stroke occurrence','')).lower() in ['1','yes','true'] and r.get('dietary habits','').strip())
    no_stroke_habits = set(r['dietary habits'] for r in data.values() if str(r.get('stroke occurrence','')).lower() in ['0','no','false'] and r.get('dietary habits','').strip())
    result = {'Condition': ['Stroke','No Stroke'], 'Habits': ['; '.join(stroke_habits), '; '.join(no_stroke_habits)]}
    return write_to_csv('query6_dietary_habits_stroke.csv', result), len(stroke_habits) + len(no_stroke_habits)

def query_7(data): # Hypertension and stroke patients
    data_q = filter_data(data, {'hypertension':'1','stroke occurrence':'1'})
    result = {a:[r[a] for r in data_q] for a in data_q[0].keys()} if data_q else {}
    return write_to_csv('query7_hypertension_stroke_patients.csv', result), len(data_q)

def query_8(data): # All hypertension patients
    data_q = filter_data(data, {'hypertension':'1'})
    result = {a:[r[a] for r in data_q] for a in data_q[0].keys()} if data_q else {}
    return write_to_csv('query8_hypertension_all_stroke_status.csv', result), len(data_q)

def query_9(data): # Heart disease and stroke patients
    data_q = filter_data(data, {'heart disease':'1','stroke occurrence':'1'})
    result = {a:[r[a] for r in data_q] for a in data_q[0].keys()} if data_q else {}
    return write_to_csv('query9_heart_disease_stroke_patients.csv', result), len(data_q)

def query_10(data): # Age statistics
    ages = [float(r['age']) for r in data.values() if r.get('age') and r['age'].strip()]
    if not ages: return write_to_csv('query10_age_statistics.csv', {}), 0
    mean = sum(ages)/len(ages)
    sorted_ages = sorted(ages)
    result = {
        'mean': mean,
        'std_dev': (sum((x-mean)**2 for x in ages)/(len(ages)-1))**0.5 if len(ages)>1 else 0,
        'min': min(ages),
        'max': max(ages),
        '25th': sorted_ages[int(0.25*len(ages))],
        '50th': sorted_ages[len(ages)//2],
        '75th': sorted_ages[int(0.75*len(ages))]
    }
    return write_to_csv('query10_age_statistics.csv', result), len(ages)

def query_11(data): # Sleep hours by stroke
    stroke_sleep = [float(r['sleep hours']) for r in data.values() if str(r.get('stroke occurrence','')).lower() in ['1','yes','true'] and r.get('sleep hours','').strip()]
    no_stroke_sleep = [float(r['sleep hours']) for r in data.values() if str(r.get('stroke occurrence','')).lower() in ['0','no','false'] and r.get('sleep hours','').strip()]
    result = {
        'Condition': ['Stroke','No Stroke'],
        'Average Sleep Hours': [sum(stroke_sleep)/len(stroke_sleep) if stroke_sleep else 0, sum(no_stroke_sleep)/len(no_stroke_sleep) if no_stroke_sleep else 0]
    }
    return write_to_csv('query11_sleep_hours_stroke.csv', result), len(stroke_sleep) + len(no_stroke_sleep)

def query_12(data, results, records): # Execution log
    result = {
        'Query': [f'Query {i}' for i in range(1,13)],
        'Status': [results.get(f'Query{i}','Failed') for i in range(1,13)],
        'Records Processed': records
    }
    return write_to_csv('query12_execution_log.csv', result)
 
def execute_all_queries(data):
    results = {}
    records = []
    queries = [query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8, query_9, query_10, query_11]
    
    for i, q in enumerate(queries, 1):
        success, count = q(data)
        results[f'Query{i}'] = 'Success' if success else 'Failed'
        records.append(count)
    records.append(len(data))
    results['Query12'] = 'Success' if query_12(data, results, records) else 'Failed'
    
    print('\nFinal Execution Results:')
    for i in range(1,13): print(f'Query {i}: {results[f"Query{i}"]}')
    print(f'\nCompleted {sum(1 for b in results.values() if b == "Success")} queries successfully out of 12')
    return results

if __name__ == "__main__":
    if not (data := load_data('data.csv')):
        sys.exit(1)
    execute_all_queries(data)