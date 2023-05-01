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
        * **example 1** `inv.generate_locations(loc_range_x, loc_range_y, loc_range_z)`
        * **example 2** `inv.generate_locations(10, 10, 3)`
    - Or creating them manually with the create_location method (not proffered)
        * **example 1** `create_location(x, y, z, length, width, height, name, s_type)`
        * **example 2** `create_locations(1, 1, 1, 10, 10, 10, 'AA1', 'static')`
6. Create an Item 
    - **example 1** `inv.create_item(name, weight=0)`
    - **example 2** `inv.create_item('Chair', 20)`
7. Create a PackagingType object
    - **example 1** `inv.create_packaging_type_object(item, length, width, height, quantity_type)`
    - **example 2** `inv.create_packaging_type_object('Chair', 5, 5, 5, 'static')`
8. Select Packaging Type object 
    1. `item = inv.item_library['Chair']`
    2. `pt = item.packaging_type_objects[0]`
9. Create a Package
    - **example 1** `inv.create_package(item_name, packaging_type_object, location, item_quantity='default', package_quantity=1)`
    - **example 2** `inv.create_package('Chair', pt, 'AA1', 1, package_quantity=2)`
10. Select Package
    - `package = item.packages[0]`
11. Move Package
    - **example 1** `inv.move_package(package, from_loc, to_loc)`
    - **example 2** `inv.move_package(package, 'AA1', 'AA2')`
