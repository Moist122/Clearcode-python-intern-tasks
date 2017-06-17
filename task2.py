import re
from itertools import combinations


def damage(spell):
    """
    Function calculating damage
    :param str spell: string with spell
    :rtype: int
    :return: points of damage
    """
    # checking parameter
    if not isinstance(spell, str):
        print("Spell isn't string")
        return

    subspells_damage = {
        'fe': 1,
        'jee': 3,
        'je': 2,
        'ain': 3,
        'dai': 5,
        'ne': 2,
        'ai': 2
    }

    # returning 0 if spell contains too many 'fe
    if re.findall('fe', spell).count('fe') > 1:
        return 0

    # searching for main body of the spell
    spellRegex = r'fe(\w)*ai'
    correct_part_of_spell = re.search(spellRegex, spell)
    if not correct_part_of_spell:
        return 0
    correct_spell = correct_part_of_spell.group()

    # finding all subspells possibly used
    subspellsRegex = re.compile(r'(?=(dai|jee|ain|ne|je|ai|fe))')
    subspells_used = re.findall(subspellsRegex, correct_spell)
    for i in range(len(subspells_used)-1, -1, -1):
        if subspells_used[i] == 'jee':
            subspells_used.insert(i, 'je')
        elif subspells_used[i] == 'ain':
            subspells_used.insert(i, 'ai')
    possibleDamage = []

    # calculating possible damage for diffrent combinations of subspells used
    for i in range(2, len(subspells_used)+1):
        possible_combinations = combinations(subspells_used, i)
        for combination in possible_combinations:
            combinationRegex = re.compile(r'(\w)*'.join(combination))

            if re.search(combinationRegex, correct_spell):
                combinationDamage = 0
                for subspell in combination:
                    combinationDamage += subspells_damage[subspell]
                combinationDamage -=\
                    len(correct_spell) - len(''.join(combination))
                possibleDamage.append(combinationDamage)

    damage = max(possibleDamage)
    if damage > 0:
        return damage
    else:
        return 0
