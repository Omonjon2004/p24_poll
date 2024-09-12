from faker import Faker
from django.utils.text import slugify
from account.models import Account, AccountProfile, Interest


fake = Faker()



def create_unique_slug(name):
    slug = slugify(name)
    original_slug = slug
    count = 1


    while Interest.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{count}"
        count += 1

    return slug



def create_fake_account():
    username = fake.user_name()
    email = fake.email()
    phone = fake.phone_number()
    account = Account.objects.create_user(username=username, email=email, phone=phone, password="password")
    return account


def create_fake_account_profile(account):
    city = fake.city()
    passport_number = fake.random_number(digits=6, fix_len=True)
    passport_letter = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    profile = AccountProfile.objects.create(
        account=account,
        city=city,
        passport_number=passport_number,
        passport_letter=passport_letter
    )
    return profile


def create_fake_interests():
    for _ in range(5):
        interest_name = fake.word()
        slug = create_unique_slug(interest_name)
        Interest.objects.create(name=interest_name, slug=slug)



def create_test_data():

    create_fake_interests()


    for _ in range(10):
        account = create_fake_account()
        profile = create_fake_account_profile(account)
        interests = Interest.objects.order_by('?')[:3]
        profile.interests.set(interests)


create_test_data()
