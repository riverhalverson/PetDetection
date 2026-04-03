
class Pet:
    name = None
    species = None
    gender = None
    likes = None
    dislikes = None

    def setPet(self, petName):
        if petName == "Skylar":
            Pet.setSkylar(self)
        elif petName == "Wubbo":
            Pet.setWubbo(self)
        else:
            Pet.setSmudge(self)

    def setSkylar(self):
        Pet.name = "Skylar"
        Pet.species = "Dog"
        Pet.gender = "Female"
        Pet.likes = """Rubbing her face on the carpet, eating the cats food, going for hikes and walks, cuddling for,
                     hours on end, standing around looking at the outside world"""
                    
        Pet.dislikes = """Being left alone for any amount of time"""

    def setWubbo(self):
        Pet.name = "Wubbo"
        Pet.species = "Cat"
        Pet.gender = "Male"
        Pet.likes = """Laying in precarious places, strecthing out on the floor, obsessing over food and nutritional yeast,
                     laying out on the balcony for hours at a time, cuddling but only in the office, eating smudges food,
                     being a log on the blanket, finding new hiding spots around the apartment, churu treats,
                     sitting for kibble or treats, getting his teeth brushed, sitting in boxes mysteriously, 
                     jumping really high, being very atheletic, intense grooming routine, supervising while cooking,
                     licking lids on food cans, making biscuits on rivers lap"""
        Pet.dislikes = """Being cuddled against his will, being held especially like a baby, being told what to do, closed doors,
                        being away from people"""

    def setSmudge(self):
        Pet.name = "Smudge"
        Pet.species = "Cat"
        Pet.gender = "Female"
        Pet.likes = """Laying in precarious places, cuddling with you for hours at a time, 
                     sticking her face aggressively into you for pets, sticking her face into armpits, 
                     head butting you, running away from you when you're trying to get her,  
                     yelling at you when shes hungry, not eating when she's supposed to and
                     requiring bribes to eat her food, chewing on strings and things when
                     she's hungry"""
        Pet.dislikes = """Eating food that isn't dry kibble or fancy feast, being held against her"""
