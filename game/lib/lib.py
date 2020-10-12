import yaml
import pandas as pd
import numpy as np
from PIL import Image


class GameObject:

    def __init__(self, registered=False, built=False, _registry_lookup=None):
        self.registered = registered
        self.registry_lookup = _registry_lookup
        self.built = built

    def build(self, game):
        self.built = True


class Character(GameObject):

    def __init__(self, name=None, soul=None, body=None, backstory=None):
        super().__init__()
        self.soul = soul
        self.body = body
        self.name = name
        self.backstory = backstory

    def gain_skill(self, skill, points):
        self.soul.skills[skill] += points * self.soul.get_governing_deity_favor(skill)

    def gain_favor(self, deity, points):
        self.soul.deity_favor[deity] += points


class Soul(GameObject):

    def __init__(self, odin_favor=0, thor_favor=0, loki_favor=0,
                 tactics=0, lore=0, perception=0, investigation=0, deduction=0,
                 power=0, athletics=0, healing=0, intimidation=0, performance=0,
                 accuracy=0, speed=0, persuasion=0, deception=0, stealth=0):
        super().__init__()
        self.deity_favor = {'odin': odin_favor,
                            'thor': thor_favor,
                            'loki': loki_favor}
        self.skills = {'tactics': tactics, 'lore': lore, 'perception': perception, 'investigation': investigation,
                       'deduction': deduction,
                       'power': power, 'athletics': athletics, 'healing': healing, 'intimidation': intimidation,
                       'performance': performance,
                       'accuracy': accuracy, 'speed': speed, 'persuasion': persuasion, 'deception': deception,
                       'stealth': stealth}

    def get_governing_deity(self, skill):
        governing_deities = {'tactics': 'odin', 'lore': 'odin', 'perception': 'odin', 'investigation': 'odin',
                             'deduction': 'odin',
                             'power': 'thor', 'athletics': 'thor', 'healing': 'thor', 'intimidation': 'thor',
                             'performance': 'thor',
                             'accuracy': 'loki', 'speed': 'loki', 'persuasion': 'loki', 'deception': 'loki',
                             'stealth': 'loki'}
        return governing_deities[skill]

    def get_governing_deity_favor(self, skill):
        return self.deity_favor[self.get_governing_deity(skill)]

    @property
    def odin_favor(self):
        return self.deity_favor['odin']

    @property
    def thor_favor(self):
        return self.deity_favor['thor']

    @property
    def loki_favor(self):
        return self.deity_favor['loki']

    @property
    def tactics(self):
        return self.skills['tactics']

    @property
    def lore(self):
        return self.skills['lore']

    @property
    def perception(self):
        return self.skills['perception']

    @property
    def investigation(self):
        return self.skills['investigation']

    @property
    def deduction(self):
        return self.skills['deduction']

    @property
    def power(self):
        return self.skills['power']

    @property
    def athletics(self):
        return self.skills['athletics']

    @property
    def healing(self):
        return self.skills['healing']

    @property
    def intimidation(self):
        return self.skills['intimidation']

    @property
    def performance(self):
        return self.skills['performance']

    @property
    def accuracy(self):
        return self.skills['accuracy']

    @property
    def speed(self):
        return self.skills['speed']

    @property
    def persuasion(self):
        return self.skills['persuasion']

    @property
    def deception(self):
        return self.skills['deception']

    @property
    def stealth(self):
        return self.skills['stealth']


class BodyPlan(GameObject):

    def __init__(self, name=None, body_plan=None):
        super().__init__(_registry_lookup='BodyPlan_' + name)
        self.body_plan = body_plan
        self.name = name

    @staticmethod
    def from_yaml(filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)

            bodies = [BodyPlan(bp['name'], bp['body_plan']) for bp in loaded_yamls if bp is not None]
        return bodies

    def build(self, game):
        self.body_plan = self._build(self.body_plan, game)
        super(BodyPlan, self).build(game)

    @staticmethod
    def _build(body_plan, game):
        if type(body_plan) == dict:
            return {game.get_object('BodyPart_' + key): BodyPlan._build(val, game) for key, val in body_plan.items()}
        elif type(body_plan) == str:
            return game.get_object('BodyPart_' + body_plan)
        elif type(body_plan) == list:
            return [BodyPlan._build(item, game) for item in body_plan]
        else:
            raise Exception('Uninterpretable BodyPlan: ' + str(body_plan))


class Body(GameObject):

    def __init__(self, name=None, body_plan=None):
        super().__init__(_registry_lookup='Body_' + name)
        self.body_plan = body_plan
        self.name = name

    @staticmethod
    def from_yaml(filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)

            bodies = [Body(bp['name'], bp['body_plan']) for bp in loaded_yamls if bp is not None]
        return bodies

    def build(self, game):
        self.body_plan = game.get_object('BodyPlan_' + self.body_plan)
        super(Body, self).build(game)


class BodyPart(GameObject):

    def __init__(self, name=None, layers=None, can_grasp=None, grasped_object=None, functioning=None):
        super().__init__(_registry_lookup='BodyPart_' + name)
        self.name = name
        self.layers = layers
        self.can_grasp = can_grasp
        self.grasped_object = grasped_object
        self.functioning = functioning

    @staticmethod
    def from_yaml(filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)

            body_parts = [BodyPart(bp['name'], bp['layers'], bp['can_grasp']) for bp in loaded_yamls if bp is not None]
        return body_parts

    def build(self, game):
        super(BodyPart, self).build(game)
        for layer in self.layers:
            mat_name = layer['material']
            mat_ref = game.get_object('Material_' + mat_name)
            layer['material'] = mat_ref


class Organ(GameObject):

    def __init__(self, name=None, material=None, blood_percentage=None, injury_timings=None, current_injury_level=None):
        super().__init__(_registry_lookup='Organ_' + name)
        self.name = name
        self.material = material
        self.blood_percentage = blood_percentage
        self.injury_timings = injury_timings
        self.current_injury_level = current_injury_level

    @staticmethod
    def from_yaml(filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)

            body_parts = [Organ(organ['name'], organ['material'], organ['blood_percentage'], organ['injury_timings'])
                          for organ in loaded_yamls if organ is not None]
        return body_parts

    def build(self, game):
        super(Organ, self).build(game)
        self.material = game.get_object('Material_' + self.material)


class Material(GameObject):

    def __init__(self, name, density, compressive_yield=None, compressive_ult=None, tensile_yield=None, tensile_ult=None,
                 shear_yield=None, shear_ult=None, mod_of_elasticity=None, shear_modulus=None, strain_at_fracture=None,
                 color=None):
        super().__init__(_registry_lookup='Material_' + name)
        self.name = name
        self.color = color
        self.density = float(density)
        self.compressive_yield = float(compressive_yield) if compressive_yield is not None else None
        self.compressive_ult = float(compressive_ult) if compressive_ult is not None else None
        self.tensile_yield = float(tensile_yield) if tensile_yield is not None else None
        self.tensile_ult = float(tensile_ult) if tensile_ult is not None else None
        self.shear_yield = float(shear_yield) if shear_yield is not None else None
        self.shear_ult = float(shear_ult) if shear_ult is not None else None
        self.mod_of_elasticity = float(mod_of_elasticity) if mod_of_elasticity is not None else None
        self.shear_modulus = float(shear_modulus) if shear_modulus is not None else None
        self.strain_at_fracture = float(strain_at_fracture) if strain_at_fracture is not None else None

    @staticmethod
    def from_yaml(filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)
            materials = []
            for mat in loaded_yamls:
                if mat is not None:
                    materials.append(Material(
                        mat['name'], mat['density'], mat['compressive_yield'], mat['compressive_ult'],
                        mat['tensile_yield'],
                        mat['tensile_ult'],
                        mat['tensile_yield'] * .577 if 'shear_yield' not in mat.keys() else mat['shear_yield'],
                        mat['tensile_ult'] * .577 if 'shear_ult' not in mat.keys() else mat['shear_ult'],
                        mat['mod_of_elasticity'], mat['shear_modulus'], mat['strain_at_fracture'], mat['color']
                    ))
        return materials

    def to_yaml(self):
        yaml_dict = {'name': self.name,
                     'density': self.density,
                     'tensile_ult': self.tensile_ult,
                     'tensile_yield': self.tensile_yield,
                     'compressive_yield': self.compressive_yield,
                     'compressive_ult': self.compressive_ult,
                     'mod_of_elasticity': self.mod_of_elasticity,
                     'shear_modulus': self.shear_modulus,
                     'strain_at_fracture': self.strain_at_fracture,
                     'color': self.color}

        return yaml.dump({key: var for key, var in yaml_dict.items() if var is not None})


class Scene:

    def __init__(self, name, size=(1000, 1000), layout=None, material_mapping=None):
        if layout is None:
            self.layout = np.zeros(size)
            self.size = size
        else:
            self.layout = layout
            self.size = layout.shape
        if material_mapping is None:
            self.material_mapping = {}
        else:
            self.material_mapping = material_mapping

    def from_yaml(self, filename):
        with open(filename) as file:
            loaded_yamls = yaml.safe_load_all(file)
        scenes = []
        for scene in loaded_yamls:
            if scene is not None:
                layout_file = scene['filename']
                im = Image.open(layout_file)
                im = np.array(im)
                assert im.shape[1] == scene['length']
                assert im.shape[0] == scene['width']

                scenes.append(Scene(name=scene['name'], layout=im, material_mapping=scene['material_mapping']))

        return scenes

    def to_yaml(self):
        return yaml.dump({'name': self.name})

class Game:

    def __init__(self, object_registry: pd.DataFrame = None):
        if object_registry is None:
            self.object_registry = pd.DataFrame(columns=['GameObject'])
        else:
            self.object_registry = object_registry
        self.registry_index_counter = 0

    def register_object(self, game_object: GameObject):
        if game_object.registry_lookup is None:
            game_object.registry_lookup = str(type(game_object)) + str(self.registry_index_counter)
        if game_object.registry_lookup not in self.object_registry.index:
            self.object_registry.loc[game_object.registry_lookup] = game_object
            game_object.registered = True
        return game_object

    def get_object(self, lookup):
        return self.object_registry.loc[lookup].iloc[0]
