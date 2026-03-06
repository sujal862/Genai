from multiprocessing import Process
import time

def brew_chai(name):
    print(f"Start of {name} chai brewing")
    time.sleep(3) # 3 sec rukega
    print(f"End of {name} chai brewing")

if __name__ == "__main__": # see Notes in down
    # Yaha 3 processes create ho rahe hain. (using Comprehension)
    # Process1 → brew_chai("Chai Maker #1")
    # Process2 → brew_chai("Chai Maker #2")
    # Process3 → brew_chai("Chai Maker #3")  and ya tino bs bn ka ak array mai stored hai 
    chai_makers = [
        Process(target=brew_chai, args=(f"Chai Maker #{i+1}", ))
        for i in range(3)
    ]

    #start all process
    for p in chai_makers:
        p.start()

    #wait for all process to complete (is line ka agga ka code all process ka complete hona ka bad hi execute hoga)
    for p in chai_makers:
        p.join()

    # ya line tb run hogi jb tino process complete hojayga
    print("All chai Serverd")




# Notes : (IMP)

# if __name__ == "__main__": multiprocessing programs me bahut important hota hai. Jab Python me koi naya process (child process) create hota hai,
# to Python us script (full program) ko fir se run karta hai. Agar hum is guard ka use na karein, to child process ke andar bhi wahi code fir se run ho sakta hai jo naye processes create karta hai,
# jis se infinite processes ban sakte hain aur program crash ho sakta hai. Isliye if __name__ == "__main__": ka use kiya jata hai taaki sirf main program hi new process create kare, 
# aur jab child processes script(full program) ko run karein to wo us part ko execute na karein. Ye multiprocessing ko safely run karne ke liye zaroori practice hai.