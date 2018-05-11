

from apputils.settings import Configuration, BaseConfigView


class ColorsDict(BaseConfigView):
  red = 0
  blue = 0
  yellow = 0


class ColorListItem(BaseConfigView):
  name = None
  value = None


class SampleModel(BaseConfigView):
  colors_dict = ColorsDict
  colors_list = [ColorListItem]


def main():
  cfg = Configuration(custom_cfg_path="./config_sample", config_name="myconfiguration.json")
  sample = SampleModel(serialized_obj=cfg.get("example_section"))

  print("Dict object print: ")
  print("Red: {}".format(sample.colors_dict.red))
  print("Blue: {}".format(sample.colors_dict.blue))
  print("Yellow: {}".format(sample.colors_dict.yellow))

  print("\n\n")

  print("List object print")

  for obj in sample.colors_list:
    print("{}: {}".format(obj.name, obj.value))


if __name__ == '__main__':
  main()




