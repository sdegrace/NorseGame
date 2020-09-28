from game.lib.lib import *
from random import choice, randint
import pandas as pd


def initialize_game():
    game = Game()
    materials = Material.from_yaml('data/materials.yaml')
    for material in materials:
        game_object = game.register_object(material)
        game_object.build(game)

    organs = Organ.from_yaml('data/organs.yaml')
    for organ in organs:
        game_object = game.register_object(organ)
        game_object.build(game)

    body_parts = BodyPart.from_yaml('data/body_parts.yaml')
    for bp in body_parts:
        game_object = game.register_object(bp)
        game_object.build(game)

    body_plans = BodyPlan.from_yaml('data/body_plans.yaml')
    for bp in body_plans:
        game_object = game.register_object(bp)
        game_object.build(game)

    return game


def initialize_player_characters(num, game):
    with open('data/backstory.yaml') as file:
        backstory = yaml.safe_load(file)
    for c in range(num):
        character = Character(name='Test', soul=Soul(), body=Body('Human', game.get_object('BodyPlan_tailless_humanoid')))
        for question in backstory:
            print(question['text'])
            for i, (id, option) in enumerate(question['options'].items()):
                print('\t' + id + ": ", option['text'])
            response = input('Your choice: ')
            while response not in question['options']:
                response = input('Your response must be one the options above... \nYour choice: ')
            response = question['options'][response]
            if 'alignment_changes' in response:
                for deity, points in response['alignment_changes'].items():
                    character.gain_favor(deity.lower(), points)
            if 'skill_changes' in response:
                for skill, points in response['skill_changes'].items():
                    character.gain_skill(skill.lower(), points)
            for skill in character.soul.skills:
                character.gain_skill(skill, randint(0, 4))


def test_backstory_balance():
    character = Character(name='Test', soul=Soul(), body=Body('Human', game.get_object('BodyPlan_tailless_humanoid')))
    skills = pd.DataFrame(character.soul.skills, index=[0])
    alignments = pd.DataFrame(character.soul.deity_favor, index=[0])
    with open('data/backstory.yaml') as file:
        backstory = yaml.safe_load(file)
    for i in range(10000):

        character = Character(name='Test', soul=Soul(), body=Body('Human', game.get_object('BodyPlan_tailless_humanoid')))
        for question in backstory:
            response = choice(list(question['options'].values()))
            if 'alignment_changes' in response:
                for deity, points in response['alignment_changes'].items():
                    character.gain_favor(deity.lower(), points)
            if 'skill_changes' in response:
                for skill, points in response['skill_changes'].items():
                    character.gain_skill(skill.lower(), points * 2.2)
            for skill in character.soul.skills:
                character.gain_skill(skill, randint(0, 4))
        skills = pd.concat([skills, pd.DataFrame(character.soul.skills, index=[0])])
        alignments = pd.concat([alignments, pd.DataFrame(character.soul.deity_favor, index=[0])])
    skills.to_excel('skills.xlsx')
    alignments.to_excel('alignments.xlsx')

if __name__ == '__main__':
    game = initialize_game()
    initialize_player_characters(1, game)


