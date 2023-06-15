# MyVentory: an inventory management system built with Python 

The purpose of MyVentory is to experiment with ideas related to space management and 
possibly build something useful. it may grow into its own independent application or it
may become a set of tools.

## Whats built

#### As of 4/27/2023 most of the basics related to creating an inventory have been built and the following can be done in the Python console

- Locations can be generated or manually created
- Packages and items can be created and moved from one location to another
- Packages can contain other packages
- In the placement of packages, the length, width and height of the package decides if the package can be placed in the desired location
- Identical packages can be detected when adding a new package object to a location, when the identical package is detected the quantity of that identical package is increased rather than adding a new package object to the location.
- Sections can be created within locations as a way of dividing space for organizational reasons

## Whats planned

- 26 to be the limit for generate_locations method argument values for letters representing numbers. Values exceeding 26 will become numbers instead
- Packages can be consolidated into their location
- Packages exist in 3D space within a section
- Algorithms for finding the optimal placement of packages within the inventory
- Support for importing inventories from excel, salesforce and other software applications
- Visualization of the inventory
- Simplification of Item/Package/PackingType creation
- Simplification By creating a GUI
- Large part of the code to be rewritten with pandas and possibly Cython for optimization

## How to use 

1. Clone this repo `git clone https://github.com/Pinklemonade33/MyVentory`
2. With Python console do the following...
3. import the inventory module `from inventory import *`
4. Initialize the inventory class `inv = Inventory()`
5. Create Locations within your inventory object
    - By generating them with the generate_locations method (proffered)
        - `inv.generate_locations(loc_range_x=10, loc_range_y=10, loc_range_z=3)`
    - Or creating them manually with the create_location method (not proffered)
        * `create_location(x=1, y=1, z=1, length=10, width=10, height=10, name='AA1', s_type='static')`
6. Create an Item 
    - `inv.create_item(name='Chair', weight=20)`
7. Create a PackagingType object
    - `inv.create_packaging_type_object(item=Chair, length=5, width=5, height=5, quantity_type='static')`
8. Select Packaging Type object 
    1. `item = inv.item_library['Chair']`
    2. `pt = item.packaging_type_objects[0]`
9. Create a Package
    - `inv.create_package(item_name='Chair', packaging_type_object=pt, location='AA1, item_quantity=1, package_quantity=1)`
10. Select Package
    - `package = item.packages[0]`
11. Move Package
    - `inv.move_package(package=package, from_loc='AA1, to_loc='AA2')`
