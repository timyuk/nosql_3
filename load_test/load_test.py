import time
from pymongo import MongoClient
import random
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

client = MongoClient("mongodb://mongos:27017", maxPoolSize=200)
db = client.university

def insert_one_record(_):
    db.grades.insert_one({
        "student_id": f"S{random.randint(0,9999)}",
        "course_id": f"C{random.randint(0,12)}",
        "teacher_id": f"T{random.randint(0,3)}",
        "grade": random.randint(1,10)
    })

def read_one_record(_):
    db.grades.find_one({"student_id": f"S{random.randint(0,9999)}"})

def test_inserts(n, workers=50):
    start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(insert_one_record, range(n))
    end = time.time()
    return end-start

def test_reads(n, workers=50):
    start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(read_one_record, range(n))
    end = time.time()
    return end-start

if __name__ == '__main__':
    threads_list = [1, 10, 50, 100]
    runs_list = [1000, 10000]

    insert_results = {1000: [], 10000: []}
    read_results = {1000: [], 10000: []}
    print("Запуск нагрузочного тестирования на запись")
    for threads in threads_list:
        for runs in runs_list:
            time_taken = test_inserts(runs, threads)
            print(f"Потоков: {threads}, Вставок: {runs}, Время: {time_taken:.2f} сек")
            insert_results[runs].append(time_taken)

    print("Запуск нагрузочного тестирования на чтение")
    for threads in threads_list:
        for runs in runs_list:
            time_taken = test_reads(runs, threads)
            print(f"Потоков: {threads}, Чтений: {runs}, Время: {time_taken:.2f} сек")
            read_results[runs].append(time_taken)


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    ax1.plot(threads_list, insert_results[1000], label='Запись (1000)', marker='o', color='blue', linestyle='-')
    ax1.plot(threads_list, insert_results[10000], label='Запись (10000)', marker='s', color='darkblue',
             linestyle='--')
    ax1.set_title('Производительность MongoDB: Операции записи')
    ax1.set_xlabel('Количество одновременных потоков')
    ax1.set_ylabel('Время выполнения (секунды)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)

    ax2.plot(threads_list, read_results[1000], label='Чтение (1000)', marker='^', color='green', linestyle='-')
    ax2.plot(threads_list, read_results[10000], label='Чтение (10000)', marker='d', color='darkgreen',
             linestyle='--')
    ax2.set_title('Производительность MongoDB: Операции чтения')
    ax2.set_xlabel('Количество одновременных потоков')
    ax2.set_ylabel('Время выполнения (секунды)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    file_name = 'chart.png'
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
