import numpy as np
class simulator:
    def __init__(self, rate=0.015, soft=60, hard=70, ratemod=0.025, fifty=True):
        self.rate = rate
        self.soft = soft
        self.hard = hard
        self.ratemod = ratemod
        self.fifty = fifty

        self.count = 0
        self.pity = 0
        self.prev = True
        self.limited = 0
        self.standard = 0

    def pull(self):
        if self.pity == self.hard:
            self.fiftyfifty()
            return
        # Get current rate
        currentRate = self.rate + max(0, self.pity-self.soft) * self.ratemod
        result = np.random.choice([0,1], p=[1-currentRate, currentRate])
        # If pulled a high *
        if result:
            self.fiftyfifty()
        else:
            self.pity += 1
                 
        self.count += 1
    
    def fiftyfifty(self):
        self.pity = 0
        # If previous high * was limited
        if self.fifty:
            if self.prev:
                # Do 50/50
                if np.random.choice([0,1]):
                    # Success
                    self.limited += 1
                    self.prev = True
                else:
                    self.standard += 1
                    self.prev = False
            # Guaranteed limited
            else:
                self.limited += 1
                self.prev = True
        else:
            if np.random.choice([0,1]):
                # Success
                self.limited += 1
                self.prev = True
            else:
                self.standard += 1
                self.prev = False

def generalStats():
    sim = simulator()
    for x in range(1000000):
        sim.pull()
    print("Total Pulls, Limited Units, Standard Units")
    print(sim.count, sim.limited, sim.standard)
    print("Consolidated probability of success")
    print(np.round((sim.limited+sim.standard)/sim.count, 5))
    print("Avg pulls for High *")
    print(np.round(sim.count/(sim.limited+sim.standard), 2))

def specificStats(trials, pulls, numLimited):
    success = 0
    limited = 0
    standard = 0
    for x in range(trials):
        sim = simulator()
        for y in range(pulls):
            sim.pull()
        limited += sim.limited
        standard += sim.standard
        if sim.limited >= numLimited:
            success += 1
    print("Chance of success")
    print(np.round(success/trials, 5))
    print("Avg Limited, Avg Standard")
    print(limited/trials, standard/trials)
def main():
    specificStats(10000, 183, 3)
    return

if __name__ == '__main__':
    main()