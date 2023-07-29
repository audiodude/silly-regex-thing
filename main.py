import re


def matchcall(self, pattern, *args, **kwargs):
  func_regex = re.compile(pattern)
  for prop in dir(self):
    attr = getattr(self, prop)
    if prop.startswith('__') or not callable(attr):
      continue

    if func_regex.match(prop):
      attr(*args, **kwargs)


class MatchedMeta(type):

  def __new__(cls, name, bases, dct):
    _wrapped = bases[0]
    dct['matchcall'] = matchcall
    return type.__new__(_wrapped.__class__, _wrapped.__name__,
                        _wrapped.__bases__, dct)


def MatchCaller(cls):

  class MatchedClass(cls, metaclass=MatchedMeta):
    pass

  return MatchedClass


class Animal:
  sound = '<silence>'

  def __init__(self, name):
    self.name = name

  @property
  def animal_type(self):
    return self.__class__.__name__.lower()

  def walk(self):
    print(f'{self.name} the {self.animal_type} is walking!')

  def talk(self):
    print(f'{self.name} the {self.animal_type} is talking: {self.sound}!')


@MatchCaller
class Cow(Animal):
  sound = 'moo'


def main():
  arthur = Animal('Arthur')
  arthur.talk()
  arthur.walk()

  betsy = Cow('Betsy')
  betsy.matchcall('.alk')


if __name__ == '__main__':
  main()