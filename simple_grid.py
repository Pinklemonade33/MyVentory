class SimpleGrid:
    def __init__(self, x, y, max_x_pix, max_y_pix, thickness=1, margins=1):
        self.grid = dict()
        self.max_rows = y
        self.max_columns = x
        cord_x = margins
        cord_y = margins
        x_add = (int(max_x_pix) - margins * 2) / x
        y_add = (int(max_y_pix) - margins * 2) / y
        self.x_max = x_add * x
        self.y_max = y_add * y
        first_1 = True
        for a in range(1, y + 1):
            if first_1 is True:
                first_1 = False
            else:
                cord_x = margins
                cord_y += y_add

            x_grid = {a: dict()}
            self.grid.update(x_grid)
            first_2 = True
            for b in range(1, x + 1):
                if first_2 is True:
                    first_2 = False
                else:
                    cord_x += x_add

                borders = {'top': (cord_y, cord_x), 'bottom': (cord_y + y_add - thickness, cord_x),
                           'left': (cord_y, cord_x),  'right': (cord_y, cord_x + x_add - thickness)}

                border_thickness = {'top': thickness, 'bottom': thickness,
                                    'left': thickness, 'right': thickness}

                h = y_add
                w = x_add

                values = {'color': 0, 'values': 0, 'coordinates': [cord_y, cord_x],
                          'height': h, 'width': w,
                          'borders': borders, 'thickness': border_thickness}

                y_grid = {b: values}
                self.grid[a].update(y_grid)

    def size(self, x_cord, y_cord, x_size, y_size, p_cells):
        def verify_space():
            if sum_w > self.x_max and sum_h > self.y_max:
                raise 'No width space,' + ' ' + 'No height space'
            elif sum_w > self.x_max:
                raise 'No width space'
            elif sum_h > self.y_max:
                raise 'No height space'
            elif not sum_w > self.x_max and not sum_h > self.y_max:
                pass

        x_list = list()
        y_list = list()
        for y in range(1, self.max_rows):
            if self.grid[y][x_cord] not in p_cells and y != y_cord:
                y_list_add = [y, x_cord]
                y_list.append(y_list_add)

        for x in range(1, self.max_columns):
            if self.grid[y_cord][x] not in p_cells and x != x_cord:
                x_list_add = [y_cord, x]
                x_list.append(x_list_add)

        sum_w = self.grid[y_cord][x_cord]['width'] * len(x_list)
        sum_h = self.grid[y_cord][x_cord]['height'] * len(y_list)
        reduce_w = (sum_w - x_size) / len(x_list)
        reduce_h = (sum_h - y_size) / len(y_list)
        verify_space()

        for y in y_list:
            self.grid[y][x_cord]['width'] -= reduce_w

        for x in x_list:
            self.grid[y_cord][x]['height'] -= reduce_h

        self.grid[y_cord][x_cord]['height'] = y_size
        self.grid[y_cord][x_cord]['width'] = x_size







