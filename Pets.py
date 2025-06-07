
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
        Pet.likes = "Rubbing her face on the carpet, eating the cats food, going for hikes and walks"
        Pet.dislikes = "Being left alone for any amount of time"

    def setWubbo(self):
        Pet.name = "Wubbo"
        Pet.species = "Cat"
        Pet.gender = "Male"
        Pet.likes = ("Laying in precarious places, streching out on the floor, obsessing over food and nutritional yeast, " +
                     "laying out on the balcony for hours at a time, cuddling but only in the office, eating smudges food")
        Pet.dislikes = "Being cuddled against his will, being held"

    def setSmudge(self):
        Pet.name = "Smudge"
        Pet.species = "Cat"
        Pet.gender = "Female"
        Pet.likes = ("Laying in precarious places, cuddling with you for hours at a time, " +
                     "sticking her face aggressively into you for pets, sticking her face into armpits")
        Pet.dislikes = "Eating food that isn't dry kibble or fancy feast"
