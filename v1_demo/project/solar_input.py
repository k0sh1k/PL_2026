# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet, Satellite


def read_space_objects_data_from_file(input_filename):
    """Читает тела из файла и создаёт объекты.

    Формат строк:
      Star      R цвет x y
      Planet    R цвет star_id cx cy orbit_r k phase
      Satellite R цвет star_id cx cy orbit_r k phase
    """
    objects = []
    with open(input_filename, encoding="utf-8") as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_body_parameters(line, planet)
                objects.append(planet)
            elif object_type == "satellite":
                satellite = Satellite()
                parse_body_parameters(line, satellite)
                objects.append(satellite)
            else:
                print("Unknown space object")
    return objects


def parse_star_parameters(line, star):
    """Звезда: Star R цвет x y"""
    parts = line.split()
    star.R = int(parts[1])
    star.color = parts[2]
    star.x = float(parts[3])
    star.y = float(parts[4])


def parse_body_parameters(line, body):
    """Планета/спутник: <Тип> R цвет star_id cx cy orbit_r k phase"""
    parts = line.split()
    body.R = int(parts[1])
    body.color = parts[2]
    body.star_id = int(parts[3])
    body.cx = float(parts[4])
    body.cy = float(parts[5])
    body.orbit_r = float(parts[6])
    body.k = int(parts[7])
    body.start_angle = float(parts[8])
    body.angle = body.start_angle


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет тела в файл в том же формате, в каком читает."""
    with open(output_filename, 'w', encoding="utf-8") as out_file:
        for obj in space_objects:
            if obj.type == "star":
                out_file.write("Star %d %s %f %f\n" % (obj.R, obj.color, obj.x, obj.y))
            else:
                type_name = obj.type.capitalize()
                out_file.write("%s %d %s %d %f %f %f %d %f\n" % (
                    type_name, obj.R, obj.color, obj.star_id,
                    obj.cx, obj.cy, obj.orbit_r, obj.k, obj.start_angle))


if __name__ == "__main__":
    print("This module is not for direct call!")
