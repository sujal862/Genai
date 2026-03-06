# You save Memory
# you don't want results immediately 
# lazy evaluation : A generator: Gives values one by one instead of giving everything at once.

def serve_chai():
    yield "Cup 1: adrak chai"
    yield "Cup 2: Ginger Chai"
    yield "Cup 3: Elaichi Chai"

# When yield runs:
    # Function pauses
    # Remembers its position
    # Next time continues from where it stopped
    # Very important:
    # Generator = paused function with memory.


stall = serve_chai()

for cup in stall:
    print(cup)

# using next
def chai_cup():
    yield "Cup 1"   # Pause here and give "Cup 1"
    yield "Cup 2"   # When resumed, pause here and give "Cup 2"
    yield "Cup 3"   # When resumed again, pause here and give "Cup 3"

chai = chai_cup()   # Calling function does NOT run it fully.
                    # It returns a generator object.

print(next(chai))   # Starts function execution.
                    # Runs until first yield.
                    # Output: "Cup 1"

print(next(chai))   # Continues from where it paused.
                    # Runs until second yield.
                    # Output: "Cup 2"

print(next(chai))   # Continues again.
                    # Runs until third yield.
                    # Output: "Cup 3"