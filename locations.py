class Locations:
    def __init__(self):
        self.locations = dict()

    def generate_locations(self, loc_type, loc_range_x, loc_range_y, loc_range_z):
        for x in range(1, loc_range_x):
            if loc_type[0] == 'l':
                x_loc = chr(ord('@') + x)
            elif loc_type[0] == 'n':
                x_loc = x + 1
            else:
                raise ValueError

            for y in range(1, loc_range_y):
                if loc_type[1] == 'l':
                    y_loc = chr(ord('@') + y)
                elif loc_type[1] == 'n':
                    y_loc = y + 1
                else:
                    raise ValueError

                for z in range(loc_range_z):
                    if loc_type[2] == 'l':
                        z_loc = chr(ord('@') + z)
                    elif loc_type[2] == 'n':
                        z_loc = z + 1
                    else:
                        raise ValueError

                    loc = {str(x_loc) + str(y_loc) + str(z_loc): None}

                    self.locations.update(loc)



