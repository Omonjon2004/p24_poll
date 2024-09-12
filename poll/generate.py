from faker import Faker
from poll.models import Poll, Choice, Vote
from account.models import Account


fake = Faker()

def create_fake_poll():
    question = fake.sentence()
    author = Account.objects.order_by('?').first()
    poll = Poll.objects.create(question=question, author=author)
    return poll

def create_fake_choices(poll):
    for _ in range(3):
        answer = fake.sentence()
        Choice.objects.create(answer=answer, poll=poll)

def create_fake_votes(poll):
    choices = poll.choices.all()
    for choice in choices:
        for _ in range(3):
            voted_by = Account.objects.order_by('?').first()
            Vote.objects.create(choice=choice, voted_by=voted_by, poll=poll)

def create_test_data():

    for _ in range(5):
        poll = create_fake_poll()
        create_fake_choices(poll)
        create_fake_votes(poll)

create_test_data()
