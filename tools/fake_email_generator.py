from itertools import islice
from random import choice, randint
from string import ascii_lowercase

"""Taken from https://homework.nwsnet.de/releases/4c3b/"""

# top-level domains
TLDS = 'com net org mil edu de biz de ch at ru de tv com st br fr de nl dk ar jp eu it es com us ca pl ua'.split()


def gen_name(length):
    """Generate a random name with the given number of characters."""
    return ''.join(choice(ascii_lowercase) for _ in range(length))


def address_generator():
    """Generate fake e-mail addresses."""
    while True:
        # user = gen_name(randint(3, 10))
        host = gen_name(randint(4, 20))
        yield '@{0}.{1}'.format(host, choice(TLDS))


def markup_address(address):
    """Wrap an e-mail address in an XHTML "mailto:" anchor."""
    return '<a href="mailto:%s">%s</a>' % ((address,) * 2)


def fake_email_host(count=1, sep=', ', markup=False):
    """Generate fake e-mail addresses.

    If ``markup`` is true, turn the addresses into "mailto:" XHTML anchors.
    """
    addresses = islice(address_generator(), count)
    if markup:
        addresses = map(markup_address, addresses)
    return sep.join(addresses)


if __name__ == '__main__':
    print(fake_email_host())
    pass
