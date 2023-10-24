import random
from model_bakery import baker

docs = [
    "99726674000135",
    "46211198000153",
    "07808028000107",
    "54408794000156",
    "95778399000142",
    "17858840000153",
    "47858280000153",
]
phones = [
    "(44)91234567",
    "(82)99345678",
    "(19)984561239",
    "(33)33456789",
    "(75)52791123",
    "(92)35678901",
]
usernames = [
    "john_doe",
    "jane12doe",
    "doeJohn",
    "JJane_",
    "john_doe_12",
    "jane_14127",
    "john_jones1274",
    "jane14_anne",
    "joanne12_1212",
    "june14april_30",
    "J_Jones_A12",
    "john_doe_12",
    "jane_15727",
    "jane_jones1273",
    "june_doe",
    "june12doe",
    "doeJones",
]


def gen_cnpj():
    return random.choice(docs)


def gen_phone():
    return random.choice(phones)


def gen_username():
    return random.choice(usernames)


baker.generators.add("core.models.DocumentField", gen_cnpj)
baker.generators.add("core.models.PhoneField", gen_phone)
baker.generators.add("core.models.UsernameField", gen_username)
