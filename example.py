from inventory import *

inv = Inventory()
inv.generate_locations(10, 10, 3)
inv.create_item('Chair', 20)
inv.create_packaging_type_object('Chair', 5, 5, 5, 'static')
item = inv.item_library['Chair']
pt = item.packaging_type_objects[0]
inv.create_package('Chair', pt, 'AA1', 1, package_quantity=2)
package = item.packages[0]
inv.move_package(package, 'AA1', 'AA2')
