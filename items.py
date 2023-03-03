class ItemLibrary:
    def __init__(self):
        self.items = list()

    def add(self, item_object):
        self.items.append(item_object)

    def remove(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                break
        else:
            raise ValueError('Name does not exist')

    def total_volume(self):
        total_volume = 0
        for item in self.items:
            total_volume += item.total_volume()

        return total_volume


class Item:
    def __init__(self, name, weight, locations=None):
        self.name = name
        self.locations = locations
        self.weight = weight
        self.packaging_type_objects = list()
        self.packages = list()

    def create_packaging_type_object(self, length, width, height, quantity_type, item_object, max_quantity=None):
        new_packaging_type_object = PackagingType(length, width, height, quantity_type, item_object, max_quantity)
        self.packaging_type_objects.append(new_packaging_type_object)

    def add_packaging_type_object(self, packaging_type_object):
        self.packaging_type_objects.append(packaging_type_object)

    def remove_packaging_type_object(self, packaging_type_object):
        self.packaging_type_objects.remove(packaging_type_object)

    def add_package(self, package):
        self.packages.append(package)

    def remove_package(self, package):
        self.packages.remove(package)

    @staticmethod
    def add_child_package(self, package, parent):
        parent.child = package

    @staticmethod
    def remove_child_package(self, package, parent):
        parent.child = None


class PackagingType:
    def __init__(self, length, width, height, quantity_type, item_object, max_quantity=None):

        if quantity_type == 'static':
            pass
        elif quantity_type == 'flexable':
            if max_quantity is None:
                ValueError('max_quantity must be set for flexable quantity_type')
            else:
                self.max_quantity = max_quantity

        self.item_object = item_object
        self.length = length
        self.width = width
        self.height = height
        self.quantity_type = quantity_type


class Package:
    def __init__(self, packaging_type_object, item_quantity, location, parent, child=None):
        self.packaging_type_object = packaging_type_object
        self.parent = parent
        self.child = child
        self.location = location
        self.item_quantity = item_quantity
        self.weight = packaging_type_object.item_object.weight * item_quantity
