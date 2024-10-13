species_list = [
    {
        "name": "African Elephant",
        "scientific_name": "Loxodonta africana",
        "description": "The largest land animal, known for its tusks and impressive size.",
    },
    {
        "name": "Cape Buffalo",
        "scientific_name": "Syncerus caffer",
        "description": "A large, powerful bovine known for its dangerous horns and aggressive nature.",
    },
    {
        "name": "Lion",
        "scientific_name": "Panthera leo",
        "description": "The 'King of the Jungle,' a large and powerful carnivore that roams the savannas.",
    },
    {
        "name": "Leopard",
        "scientific_name": "Panthera pardus",
        "description": "A stealthy and adaptable predator, famous for its spotted coat.",
    },
    {
        "name": "Cheetah",
        "scientific_name": "Acinonyx jubatus",
        "description": "The fastest land animal, capable of reaching speeds over 60 miles per hour.",
    },
    {
        "name": "Eland",
        "scientific_name": "Taurotragus oryx",
        "description": "The largest species of antelope, known for its spiral horns and slow movements.",
    },
    {
        "name": "Greater Kudu",
        "scientific_name": "Tragelaphus strepsiceros",
        "description": "An antelope with impressive, twisted horns and a striking appearance.",
    },
    {
        "name": "Lesser Kudu",
        "scientific_name": "Tragelaphus imberbis",
        "description": "A smaller and more elusive antelope with spiraled horns and beautiful markings.",
    },
    {
        "name": "Sable Antelope",
        "scientific_name": "Hippotragus niger",
        "description": "A striking antelope with long, backward-curving horns and dark, glossy coat.",
    },
    {
        "name": "Roan Antelope",
        "scientific_name": "Hippotragus equinus",
        "description": "A large antelope known for its distinctive facial markings and robust horns.",
    },
    {
        "name": "Waterbuck",
        "scientific_name": "Kobus ellipsiprymnus",
        "description": "A large antelope often found near water sources, with a distinctive white ring around its rump.",
    },
    {
        "name": "Giraffe",
        "scientific_name": "Giraffa camelopardalis",
        "description": "The tallest land animal, known for its long neck and spotted coat.",
    },
    {
        "name": "Zebra",
        "scientific_name": "Equus quagga",
        "description": "A horse-like animal with a distinctive black-and-white striped coat.",
    },
    {
        "name": "Impala",
        "scientific_name": "Aepyceros melampus",
        "description": "A graceful and fast antelope, known for its agility and impressive leaps.",
    },
    {
        "name": "Wildebeest",
        "scientific_name": "Connochaetes taurinus",
        "description": "A large, bearded antelope, known for its annual migration across the Serengeti.",
    },
    {
        "name": "Bushbuck",
        "scientific_name": "Tragelaphus scriptus",
        "description": "A shy and elusive antelope, usually found in dense vegetation near water.",
    },
    {
        "name": "Common Duiker",
        "scientific_name": "Sylvicapra grimmia",
        "description": "A small and swift antelope, often found in savannas and grasslands.",
    },
    {
        "name": "Steenbok",
        "scientific_name": "Raphicerus campestris",
        "description": "A small, reddish antelope, known for its solitary behavior and fast speed.",
    },
    {
        "name": "Oribi",
        "scientific_name": "Ourebia ourebi",
        "description": "A small, slender antelope with a distinctive white tail, usually found in open plains.",
    },
    {
        "name": "Hartebeest",
        "scientific_name": "Alcelaphus buselaphus",
        "description": "A large antelope with a long, narrow face and horns that curve backward.",
    },
    {
        "name": "Warthog",
        "scientific_name": "Phacochoerus africanus",
        "description": "A wild pig with large tusks, known for its resilience and burrowing habits.",
    },
    {
        "name": "Bushpig",
        "scientific_name": "Potamochoerus larvatus",
        "description": "A wild pig species that thrives in dense forests and savannas, known for its nocturnal behavior.",
    },
    {
        "name": "Crocodile",
        "scientific_name": "Crocodylus niloticus",
        "description": "A large, carnivorous reptile, often found in rivers and lakes, known for its powerful bite.",
    },
    {
        "name": "Hippopotamus",
        "scientific_name": "Hippopotamus amphibius",
        "description": "A massive, semi-aquatic mammal, known for its aggressive behavior and large jaws.",
    },
    {
        "name": "Baboon",
        "scientific_name": "Papio anubis",
        "description": "A large primate species, known for its social behavior and adaptability to different environments.",
    },
    {
        "name": "Hyena",
        "scientific_name": "Crocuta crocuta",
        "description": "A scavenger and predator, known for its powerful jaws and social hierarchy.",
    },
    {
        "name": "Oryx",
        "scientific_name": "Oryx beisa",
        "description": "A large antelope with long, straight horns, adapted to live in arid environments.",
    },
    {
        "name": "Topi",
        "scientific_name": "Damaliscus lunatus",
        "description": "A swift antelope, known for its endurance and speed, often seen in open grasslands.",
    },
    {
        "name": "Reedbuck",
        "scientific_name": "Redunca arundinum",
        "description": "A medium-sized antelope found near wetlands and rivers, known for its distinctive whistling sound.",
    },
    {
        "name": "Klipspringer",
        "scientific_name": "Oreotragus oreotragus",
        "description": "A small antelope adapted to rocky terrain, known for its nimble movements.",
    },
    {
        "name": "Grant’s Gazelle",
        "scientific_name": "Nanger granti",
        "description": "A large gazelle with striking black and white markings, common in open plains.",
    },
    {
        "name": "Thomson’s Gazelle",
        "scientific_name": "Eudorcas thomsonii",
        "description": "A small gazelle, known for its speed and agility, commonly seen in the Serengeti.",
    },
]

from django.core.management.base import BaseCommand
from bm_hunting_settings.models import Species


# class Species(models.Model):
#     name = models.CharField(max_length=100)
#     scientific_name = models.CharField(max_length=100, null=True, blank=True)
#     description = models.TextField()


class Command(BaseCommand):
    help = "Add species"

    def handle(self, *args, **options):
        # country_choices = [{"code": code, "name": name} for code, name in countries]
        for species in species_list:
            Species.objects.create(
                name=species["name"],
                scientific_name=species["scientific_name"],
                description=species["description"],
            )
            self.stdout.write(self.style.SUCCESS(f"Added {species['name']}"))
