# 示例1
class Animal():
    def who(self):
        print("I am an Animal")


class Duck(Animal):
    def who(self):
        print("I am a duck")


class Dog(Animal):
    def who(self):
        print("I am a dog")


class Cat(Animal):
    def who(self):
        print("I am a cat")


class Person:
    def who(self):
        print("I am a Person")


def func(p: Animal):
    p.who()


if __name__ == "__main__":
    duck = Duck()
    dog = Dog()
    cat = Cat()
    p = Person()
    func(duck)
    func(dog)
    func(cat)
