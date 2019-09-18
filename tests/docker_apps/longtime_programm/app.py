from random import randrange
import time

def main():
    runtime = randrange(4)
    print "I am waiting for", runtime, "minutes"
    for i in range(runtime):
        time.sleep(30)
        print "Waited half a minute"
        time.sleep(30)
        print "Waited for", i+1, " minutes"
    print "I finished waiting"

if __name__ == "__main__":
    main()
