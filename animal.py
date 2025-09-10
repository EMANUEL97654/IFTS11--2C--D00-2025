from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def sleep(self):
        pass

    @abstractmethod
    def move(self):
        pass


class Perro(Animal):
    def speak(self):
        print("El perro ladra")

    def eat(self):
        print("El perro come")

    def sleep(self):
        print("El perro duerme")

    def move(self):
        print("El perro camina")

class Gato(Animal):
    def speak(self):
        print("El gato maulla")

    def eat(self):
        print("El gato come")

    def sleep(self):
        print("El gato duerme")

    def move(self):
        print("El gato camina")