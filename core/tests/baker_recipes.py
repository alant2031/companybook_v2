from model_bakery.recipe import Recipe, foreign_key, seq
from core.models import Company, Subscriber

company_tekno = Recipe(Company, razao="Tekno Solutions Ltda.")
subscriber_tekno = Recipe(
    Subscriber,
    logo="tiger.png",
    company=foreign_key(company_tekno),
    username="john_doe",
    photo1="eggs.png",
    photo2="eggs.png",
    photo3="eggs.png",
    photo4="eggs.png",
)

company_view = Recipe(Company, document=seq("0780802800010"))
subscriber_view = Recipe(
    Subscriber, company=foreign_key(company_view), username=seq("mulan")
)
