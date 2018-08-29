import random
from itertools import islice
from random import choice, randint
from string import ascii_lowercase

import faker


fake = faker.Faker()


def generate_numbers(l, as_string=False):
    result = ''
    for i in range(l):
        n = random.randint(0, 9)
        result = result + str(n)
    if as_string:
        return result
    else:
        if result.startswith('0'):
            result = result + '0'
        return int(result)


def generate_string(str_length=10):
    a = ''
    for i in range(1):
        a = a.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                            for x in range(str_length)])
    return a


class FakeHostEmailGenerator:
    """Taken from https://homework.nwsnet.de/releases/4c3b/"""
    TLDS = 'com net org mil edu de biz de ch at ru de tv com st br fr de nl dk ar jp eu it es com us ca pl ua'.split()

    def gen_name(self, length):
        """Generate a random name with the given number of characters."""
        return ''.join(choice(ascii_lowercase) for _ in range(length))

    def address_generator(self):
        """Generate fake e-mail addresses."""
        while True:
            # user = gen_name(randint(3, 10))
            host = self.gen_name(randint(4, 20))
            yield '@{0}.{1}'.format(host, choice(self.TLDS))

    def markup_address(self, address):
        """Wrap an e-mail address in an XHTML "mailto:" anchor."""
        return '<a href="mailto:%s">%s</a>' % ((address,) * 2)

    def fake_email_host(self, count=1, sep=', ', markup=False):
        """Generate fake e-mail addresses.

        If ``markup`` is true, turn the addresses into "mailto:" XHTML anchors.
        """
        addresses = islice(self.address_generator(), count)
        if markup:
            addresses = map(self.markup_address, addresses)
        return sep.join(addresses)


def generate_phone_number():
    return str(generate_numbers(12))


def generate_street_name():
    return fake.street_name()


def generate_post_index():
    return str(generate_numbers(5))


# region Organization data
def generate_organization_name():
    return fake.company()


def generate_code_of_organization(type_of_organization, length=None):
    if type_of_organization == 1:
        return str(generate_numbers(8))
    elif type_of_organization == 2:
        return str(generate_numbers(10))
    elif type_of_organization == 3:
        return generate_string(length)
# endregion Organization data


if __name__ == '__main__':
    # print(FakeHostEmailGenerator().fake_email_host())
    print(generate_code_of_organization(3, 5))
    print(generate_organization_name())
    pass
