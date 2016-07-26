## Animal is-a object (yes, sort of confusing) look at the extra credit
class Animal(object):
	pass

## dog is-a animal
class Dog(Animal):

	def __init__(self, name):
		## dog has-a name of name
		self.name = name

## cat is-a animal
class Cat(Animal):

	def __init__(self, name):
		## cat has-a name of name
		self.name = name

## Person is-a object
class Person(object):

	def __init__(self, name):
		## Person has-a name of name
		self.name = name

		## Person has-a pet of some kind
		self.pet = None

## Employee is-a Person
class Employee(Person):

	def __init__(self, name, salary):
		## person is-a person
		super(Employee, self).__init__(name)
		## employee has salary
		self.salary = salary

## Fish is-a object
class Fish(object):
	pass

## salmon is-a fish
class Salmon(Fish):
	pass

## halibut is-a fish
class Halibut(Fish):
	pass


## rover is-a Dog
rover = Dog("Rover")

## satan is-a cat
satan = Cat("Satan")

## mary is-a person
mary = Person("Mary")

## mary has-a pet name's satan
mary.pet = satan

## frans is-a employee, he has-a salary of 12000
frank = Employee("Frank", 120000)

## frank has-a pet name's rover
frank.pet = rover

## fish has-a flipper
flipper = Fish()

## salmon has-a crouse
crouse = Salmon()

## halibut has-a harry
harry = Halibut()