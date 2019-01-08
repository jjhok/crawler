from multiprocessing import Process, Pool
import os

def doubler(number): 
    
    result = number * 2 
    proc = os.getpid() 
    print('{0} doubled to {1} by process id: {2}'.format( number, result, proc))

numbers = [5, 10, 15, 20, 25] 
procs = []   
pool = Pool(4)

print(pool.map(doubler, numbers))
# pool.map(doubler, numbers)

print("END")