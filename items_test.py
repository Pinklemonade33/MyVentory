import items
import copy

library = items.ItemLibrary()
new_item = items.Item('ssh-158', 2)
new_package_type = items.PackagingType(2, 2, 2, 'static', new_item)

a = [1, 4, 6]


def get_dict_key(dic, keys):
    for key in keys:
        dic = dic[key]
    return dic


def create_test_tree(amounts):
    roots = list()
    root = object()
    for b in amounts:
        root = copy.deepcopy(new_package_type)
        branch_1 = root
        for r in range(b):
            branch_2 = copy.deepcopy(new_package_type)
            branch_1.add_packaging_type_object(branch_2)
            branch_1 = branch_2

        roots.append(root)
    return roots


return_root = create_test_tree(a)
new_item.packaging_type_objects = return_root


def tree_to_dict(node, return_dict=None, keys=None):
    if return_dict is None:
        return_dict = dict()

    if keys is None:
        keys = list()

    for index, c in enumerate(node.packaging_type_objects):
        if len(c.packaging_type_objects) == 0:
            new_dict = {index: None}
            if len(keys) != 0:
                temp_dic = get_dict_key(return_dict, keys)
                return_dict[temp_dic].update(new_dict)
            else:
                return_dict.update(new_dict)

        elif len(c.packaging_type_objects) > 0:
            new_dict = {index: c}
            return_dict.update(new_dict)
            return_dict_return = tree_to_dict(c, return_dict)
            return_dict[index] = return_dict_return

    return return_dict


dik = tree_to_dict(new_item)
print(dik)


