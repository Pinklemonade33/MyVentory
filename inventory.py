import itertools


class Inventory:
    def __init__(self):
        self.item_library = dict()
        self.location_library = dict()

    # region Location // Methods

    def create_location(self, x, y, z, length, width, height, name, s_type, consolidation='partial'):
        new_location = Location(x, y, z, length, width, height, name, s_type, consolidation)
        self.location_library.update({name: new_location})

    def generate_locations(self, loc_range_x, loc_range_y, loc_range_z,
                           start_x=0, start_y=0, start_z=0, length=10, width=10, height=10,
                           s_type='static', buffer_x=0, buffer_y=0,
                           buffer_z=0, loc_type='lln', consolidation='partial'):

        current_x = start_x

        for x in range(1, loc_range_x):
            if x > 1:
                current_x += length + 1 + buffer_x
            current_y = start_y

            if loc_type[0] == 'l':
                x_loc = chr(ord('@') + x)
            elif loc_type[0] == 'n':
                x_loc = x + 1
            else:
                raise ValueError

            for y in range(1, loc_range_y):
                if y > 1:
                    current_y += width + 1 + buffer_y
                current_z = start_z

                if loc_type[1] == 'l':
                    y_loc = chr(ord('@') + y)
                elif loc_type[1] == 'n':
                    y_loc = y + 1
                else:
                    raise ValueError

                for z in range(loc_range_z):
                    if z > 1:
                        current_z += height + 1 + buffer_z

                    if loc_type[2] == 'l':
                        z_loc = chr(ord('@') + z)
                    elif loc_type[2] == 'n':
                        z_loc = z + 1
                    else:
                        raise ValueError

                    name = str(x_loc) + str(y_loc) + str(z_loc)
                    self.create_location(x=current_x, y=current_y, z=current_z,
                                         length=length, s_type=s_type,
                                         width=width, height=height, name=name,
                                         consolidation=consolidation)

    # endregion

    # region Location - Item // Methods

    def move_package(self, package, from_loc, to_loc):
        self.location_library[from_loc].remove_package(package)
        self.location_library[to_loc].add_package(package)
        package.location = to_loc

    # endregion

    # region Item // Methods

    def create_item(self, name, weight=0):
        new_item = Item(name, weight)
        new_item_dic = {name: new_item}
        self.item_library.update(new_item_dic)

    def create_package(self, item_name, packaging_type_object, location, item_quantity='default',
                       parent=None, child=None, package_quantity=1):

        if parent is None:
            parent = self.item_library[item_name]

        if item_quantity == 'default':
            item_quantity = packaging_type_object.max_quantity

        new_package = Package(packaging_type_object, item_quantity, location, parent, child,
                              package_quantity)

        self.item_library[item_name].add_package(new_package)
        self.location_library[location].add_package(new_package)

    def create_packaging_type_object(self, item_name, length, width, height, quantity_type,
                                     max_quantity=None):

        new_packaging_type_object = PackagingType(length, width, height, quantity_type,
                                                  self.item_library[item_name], max_quantity)

        for x in self.item_library[item_name].packaging_type_objects:
            for value_1, value_2 in zip(vars(x).values(), vars(new_packaging_type_object).values()):
                if value_1 != value_2:
                    break
            else:
                raise ValueError('this packaging_type_object already exists')

        self.item_library[item_name].packaging_type_objects.append(new_packaging_type_object)

    def create_package_stack(self, item_name, packaging_type_objects, item_quantities, locations,
                             parents, children, package_quantities):

        new_package = None

        for packaging_type_object, item_quantity, location, parent, child, package_quantity \
                in zip(packaging_type_objects, item_quantities, locations, parents, children, package_quantities):
            new_package = Package(packaging_type_object, item_quantity, location, parent, child, package_quantity)

        if new_package is not None:
            self.item_library[item_name].add_package(new_package)
        elif new_package is None:
            raise ValueError('Cannot add None to item_library')

    def get_packages(self, packaging_type_object=None, item_quantity=None,
                     location=None, parent=None, child=None,
                     weight=None, package_quantity=None, item=None):

        def check_package(package):
            nonlocal arguments_dict

            for key, value in arguments_dict:
                if vars(package)[key] != value:
                    return False
            else:
                return True

        arguments_dict = {'packaging_type_object': packaging_type_object,
                          'item_quantity': item_quantity, 'location': location,
                          'parent': parent, 'child': child, 'weight': weight,
                          'package_quantity': package_quantity}

        arguments_dict = {k: v for (k, v) in arguments_dict.items() if v is not None}

        matching_packages = list()

        if item is None:
            if parent is not None:
                item = get_head(parent)
            elif child is not None:
                item = get_head(child)

        if item is not None:
            for x in self.item_library[item].packages:
                if check_package(x) is True:
                    matching_packages.append(x)

        elif location is not None:
            for x in self.location_library[location]:
                if check_package(x) is True:
                    matching_packages.append(x)

        else:
            for x in self.item_library:
                for y in x.packages:
                    if check_package(x) is True:
                        matching_packages.append(x)

        return matching_packages

    def remove_package(self, item_name, packaging_type_object, location, package_quantity,
                       parent, child, amount):

        package = self.get_package(item_name, packaging_type_object, location, package_quantity,
                                   parent, child)

    def get_package(self, item_name, packaging_type_object, location, package_quantity,
                    parent, child):

        for x in self.item_library[location].items[item_name].packages:
            if x.packaging_type_object == packaging_type_object \
                    and x.parent == parent and x.child == child:
                return x

    # endregion


class Location:
    def __init__(self, x, y, z, length, width, height, name, s_type, consolidation):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.items = dict()
        self.total_lwh = [length, width, height]
        main_section = Section(x, y, z, length, width, height, s_type='dynamic', consolidation='partial')
        self.sections = [main_section]

        if s_type == 'static' or s_type == 'dynamic':
            self.s_type = s_type
        else:
            raise ValueError('s_type must be static or dynamic')

        if consolidation == 'full' or consolidation == 'partial':
            self.consolidation = consolidation
        else:
            raise ValueError('consolidation must be partial or full')

    def get_sections_lwh(self, free, dynamic=True):
        total_lwh = [0, 0, 0]

        for x in self.sections:
            if free:
                t_length = x.free_lwh[0]
                t_width = x.free_lwh[1]
                t_height = x.free_lwh[2]
            elif not free:
                t_length = x.total_lwh[0]
                t_width = x.total_lwh[1]
                t_height = x.total_lwh[2]
            else:
                raise ValueError('free must be boolean')

            if dynamic:
                if x.s_type == 'dynamic':
                    total_lwh[0] += t_length
                    total_lwh[1] += t_width
                    total_lwh[2] += t_height
            elif not dynamic:
                total_lwh[0] += t_length
                total_lwh[1] += t_width
                total_lwh[2] += t_height
            else:
                raise ValueError('dynamic must be boolean')

        return total_lwh

    def create_section(self, x, y, z, length, width, height, s_type, consolidation,
                       space_from=None, space_from_type='even'):

        s_lwh = self.get_sections_lwh(True)
        if s_lwh[0] < length and s_lwh[1] < width and s_lwh[2] < height:
            raise ValueError('Not enough free space available')
        else:
            if space_from is None:
                space_from = [0]

            if space_from_type == 'even':
                t_length = length / len(space_from)
                t_width = width / len(space_from)
                t_height = height / len(space_from)
                for x in space_from:
                    section = self.sections[x]
                    section.free_lwh[0] -= t_length
                    section.free_lwh[1] -= t_width
                    section.free_lwh[2] -= t_height

            elif space_from_type == 'order':
                a_length = length.copy()
                a_width = width.copy()
                a_height = height.copy()
                for x in space_from:
                    section = self.sections[x]
                    if a_length / section.free_lwh[0] >= 1:
                        t_length = section.free_lwh[0]
                    else:
                        t_length = section.free_lwh[0] * (a_length / section.free_lwh[0])

                    if a_width / section.free_lwh[0] >= 1:
                        t_width = section.free_lwh[1]
                    else:
                        t_width = section.free_lwh[1] * (a_width / section.free_lwh[1])

                    if a_height / section.free_lwh[2] >= 1:
                        t_height = section.free_lwh[2]
                    else:
                        t_height = section.free_lwh[2] * (a_height / section.free_lwh[2])

                    a_length -= t_length
                    a_width -= t_width
                    a_height -= t_height

                    section.free_lwh[0] -= t_length
                    section.free_lwh[1] -= t_width
                    section.free_lwh[2] -= t_height

            new_section = Section(x, y, z, length, width, height, s_type, consolidation)
            self.sections.update({name: new_section})

    def remove_section(self, index, space_to=None, space_to_type='even'):
        if space_to is None:
            space_to = [0]

        for x in space_to:
            if self.sections[x].s_type == 'static':
                raise ValueError('cannot add space to static section')

        length = self.sections[index].total_lwh[0]
        width = self.sections[index].total_lwh[1]
        height = self.sections[index].total_lwh[2]

        if space_to_type == 'even':
            t_length = length / len(space_to)
            t_width = width / len(space_to)
            t_height = height / len(space_to)
            for x in space_to:
                section = self.sections[x]
                section.free_lwh[0] += t_length
                section.free_lwh[1] += t_width
                section.free_lwh[2] += t_height
                section.total_lwh[0] += t_length
                section.total_lwh[1] += t_width
                section.total_lwh[2] += t_height

        self.sections.pop(index)

    def add_package(self, package):
        for x in self.sections:
            if package.item_object in x.assigned_items:
                section = x
                break
        else:
            section = self.sections[0]

        section.add_package(package)

    def get_packages(self):
        return [x for y in self.sections for x in y.packages]

    def get_items(self):
        return {key: value for x in self.sections for key, value in x.items.items()}

    def check_sections(self, package):
        p_lwh = [package.packaging_type_object.length,
                 package.packaging_type_object.width,
                 package.packaging_type_object.height]

        sections = list()
        for section in self.sections:
            if section.s_type == 'dynamic':
                if package.item_object in section.assigned_items:
                    s_lwh = section.remaining_lwh
                    for x in itertools.permutations(p_lwh):
                        for y in s_lwh:
                            if y / x < 1:
                                break
                        else:
                            sections.append(Section)

        if len(sections) > 0:
            return sections
        else:
            return False

    @staticmethod
    def rotate_dims(package, dims):
        p_lwh = [package.packaging_type_object.length,
                 package.packaging_type_object.width,
                 package.packaging_type_object.height]

        for x in itertools.permutations(p_lwh):
            for y in dims:
                if y / x < 1:
                    break
            else:
                return x

    def consolidate_location(self, section=None):
        p_lwh = list()
        if self.consolidation == 'full':
            for x in self.packages:
                p_lwh.append([x.package_type_object.length, x.package_type_object.width, x.package_type_object.height])


class Section:
    def __init__(self, x, y, z, length, width, height, s_type, consolidation):
        self.x = x
        self.y = y
        self.z = z
        self.items = dict()
        self.packages = list()
        self.packaging_type_objects = list()
        self.free_lwh = [length, width, height]
        self.total_lwh = [length, width, height]
        self.assigned_items = dict()

        if s_type == 'static' or s_type == 'dynamic':
            self.s_type = s_type
        else:
            raise ValueError('s_type must be static or dynamic')

        if consolidation == 'full' or consolidation == 'partial':
            self.consolidation = consolidation
        else:
            raise ValueError('consolidation must be partial or full')

    def add_package(self, package):

        if package.packaging_type_object not in self.packaging_type_objects:
            self.packaging_type_objects.append(package.packaging_type_object)

        self.items.update({package.item_object.name: package.item_object})
        self.packages.append(package)

    def set_layout(self):
        dims = [itertools.permutations([x.length, x.width, x.height]) for x in self.packaging_type_objects]


class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.packaging_type_objects = list()
        self.packages = list()

    def add_package(self, package):
        residing_package = self.check_for_same(package)
        if residing_package is False:
            self.packages.append(package)
        else:
            residing_package.package_quantity += package.package_quantity

    def check_for_same(self, package):
        def check_for_same_recursion(package_1, package_2):
            for (key_1, val_1), (key_2, val_2) in zip(vars(package_1).items(), vars(package_2).items()):
                if key_1 != 'package_quantity':
                    if val_1 != val_2:
                        return False
            return True

        depth = get_depth(package)
        for old_package in self.packages:
            if depth == get_depth(old_package):
                counter = 0
                while counter <= depth:
                    if check_for_same_recursion(package, old_package) is False:
                        break
                    else:
                        counter += 1
                else:
                    return old_package
        return False

    def remove_package(self, package, amount):
        residing_package = self.check_for_same(package)
        if residing_package is False:
            raise ValueError('Package does not exist')
        else:
            residing_package.package_quantity -= amount
            if residing_package.package_quantity == 0:
                self.packages.remove(residing_package)

    def all_locations(self):
        loc = list()
        for x in self.packages:
            if x.location not in loc:
                loc.append(x.location)


class PackagingType:
    def __init__(self, length, width, height, quantity_type, item_object, max_quantity):

        if quantity_type == 'static':
            pass
        elif quantity_type == 'flexable':
            pass
        else:
            raise ValueError('quantity_type must be either static or flexable')

        self.max_quantity = max_quantity
        self.item_object = item_object
        self.length = length
        self.width = width
        self.height = height
        self.quantity_type = quantity_type


class Package:
    def __init__(self, packaging_type_object, item_quantity,
                 location, parent, child=None, package_quantity=1):

        self.package_quantity = package_quantity
        self.packaging_type_object = packaging_type_object
        self.parent = parent
        self.child = child
        self.location = location
        self.item_quantity = item_quantity
        self.item_object = packaging_type_object.item_object
        self.weight = self.item_object.weight * item_quantity


def get_depth(node):
    counter = 0
    while node.child is not None:
        counter += 1
        node = node.child

    return counter


def get_head(node):
    if isinstance(node, Item) is True:
        return node

    while isinstance(node.parent, Item) is False:
        node = node.parent

    return node


def get_prior_nodes(node):
    nodes = list()
    while isinstance(node, Package) is True:
        nodes.append(node)
        node = node.parent

    return nodes


def error_handler(error):
    if error == 'space':
        pass


def get_closest_fit(dims_list, dim_to_fit):
    best_fit = None
    for dims in dims_list:
        for dim in itertools.permutations(dims):
            fit = list()
            for x, y in zip(dim, dim_to_fit):
                fit.append(x - y)

            new_fit = list()
            if best_fit is None:
                best_fit = fit
            else:
                for x, y in zip(fit, best_fit):
                    if x - y >= 0:
                        new_fit.append(x - y)
                    else:
                        break
                else:
                    if sum(new_fit) <= sum(best_fit):
                        best_fit = new_fit

    return best_fit