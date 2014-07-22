import GURPS_Dice as GD
from GURPS_Tables import OrbitalSpace

class PlanetSystem:
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, innerlimit, outerlimit, snowline,
                 innerforbidden=None, outerforbidden=None):
        self.roller = GD.DiceRoller()
        self.__innerlimit = innerlimit
        self.__outerlimit = outerlimit
        self.__snowline = snowline
        self.__forbidden = False
        if innerforbidden is not None and outerforbidden is not None:
            self.__innerforbidden = innerforbidden
            self.__outerforbidden = outerforbidden
            self.__forbidden = True
        self.makegasgiantarrangement()
        self.placegasgiant()
        self.createorbits()
        self.printinfo()

    def printinfo(self):
        print("--------------------")
        print(" Planet System Info ")
        print("--------------------")
        print("GG Arrngmnt:\t{}".format(self.__gasarrangement))
        print("Frst GG Orb:\t{}".format(self.__firstgasorbit))
        print("     Orbits:\t{}".format(self.__orbitarray))

    def allowedorbit(self, testorbit):
        result  = testorbit >= self.__innerlimit
        result &= testorbit <= self.__outerlimit
        if self.__forbidden and result:
            result2 = testorbit <= self.__innerforbidden
            result2 |= testorbit >= self.__outerforbidden
            return result & result2
        else:
            return result

    def makegasgiantarrangement(self):
        dice = self.roll(3,0)
        self.__gasarrangement = 'None'
        if dice > 10:
            self.__gasarrangement = 'Conventional'
        if dice > 12:
            self.__gasarrangement = 'Eccentric'
        if dice > 14:
            self.__gasarrangement = 'Epistellar'

    def placegasgiant(self):
        orbit = 0
        if self.__gasarrangement == 'Conventional':
            orbit = (1 + (self.roll(2,-2) * 0.05)) * self.__snowline
        if self.__gasarrangement == 'Eccentric':
            orbit = self.roll(1,0) * 0.125 * self.__snowline
        if self.__gasarrangement == 'Epistellar':
            orbit = self.roll(3,0) * 0.1 * self.__innerlimit
        self.__firstgasorbit = orbit


    def createorbits(self):
        orbits = []
        if self.__gasarrangement == 'None':
            # Create orbits outwards from the inner limit
            orbits += [self.__innerlimit]
            orbitsout = self.orbitoutward(self.__innerlimit)
            orbits += orbitsout
        else:
            # Create orbits inwards then outwards from first gas giant
            orbits += [self.__firstgasorbit]
            orbitsin = self.orbitinward(self.__firstgasorbit)
            orbitsout = self.orbitoutward(self.__firstgasorbit)
            orbits = orbitsin + orbits
            orbits += orbitsout
        self.__orbitarray = orbits

    def orbitoutward(self, startorbit):
        allowed = True
        orbits = []
        oldorbit = startorbit
        neworbit = 0
        while(allowed):
            orbsep = OrbitalSpace[self.roll(3,0)]
            neworbit = oldorbit * orbsep
            if self.allowedorbit(neworbit) and neworbit - oldorbit >= 0.15:
                orbits += [neworbit]
                oldorbit = neworbit
            else:
                allowed = False
                # Check to fit one last orbit
                if self.allowedorbit(oldorbit * 1.4) and neworbit - oldorbit >= 0.15:
                    orbits += [oldorbit * 1.4]
                    # Because this worked we'll try to do this one more time
                    oldorbit = oldorbit * 1.4
                    allowed = True
        return orbits

    def orbitinward(self, startorbit):
        print("Entered OrbitInward")
        allowed = True
        orbits = []
        oldorbit = startorbit
        neworbit = 0
        while(allowed):
            print(" Orbits: {}".format(orbits))
            orbsep = OrbitalSpace[self.roll(3,0)]
            print(" Rolled an orbsep = {}".format(orbsep))
            neworbit = oldorbit / orbsep
            print(" New Orbit would be {}".format(neworbit))
            if self.allowedorbit(neworbit) and oldorbit - neworbit >= 0.15:
                print(" It is allowed.")
                orbits = [neworbit] + orbits
                oldorbit = neworbit
            else:
                allowed = False
                # Check to fit one last orbit
                if self.allowedorbit(oldorbit / 1.4) and oldorbit - neworbit >= 0.15:
                    orbits = [oldorbit / 1.4] + orbits
                    # Because this worked we'll try to do this one more time
                    oldorbit = oldorbit / 1.4
                    allowed = True
        print("Returning {}".format(orbits))
        return orbits