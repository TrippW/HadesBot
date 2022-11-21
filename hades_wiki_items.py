import re
from wiki_matcher.wiki import WikiItem, WikiItems

def _clean_name(name):
    return re.sub('\s+', ' ', name).casefold()

class Boon(WikiItem):
    def __init__(self, god, name, descr):
        super().__init__(name)
        self.god = god
        self.descr = descr

    def key_names(self):
        res =  [ _clean_name(self.name) ]
        for possessive in ['', "'s"]:
            res.append(_clean_name(f'{self.god+possessive} {self.name} boon'))
        return res

    def full_descr(self):
        return f"**{self.name} ({self.god})** - {self.descr}"
    def __repr__(self):
        return f"<Boon {self.god} {self.name}>"

class DuoBoon(WikiItem):
    def __init__(self, name, descr, gods, requirements):
        super().__init__(name)
        self.gods = gods
        self.descr = descr
        self.requirements = requirements
    def key_names(self):
        res =  [ _clean_name(self.name) ]
        for gods in [ self.gods, self.gods[::-1] ]:
            for joined_gods in [' and '.join(gods), '/'.join(gods), ' + '.join(gods), '+'.join(gods)]:
                for possessive in ['', "'s"]:
                    res.append(_clean_name(joined_gods+possessive+' duo boon'))
                    res.append(_clean_name(joined_gods+possessive+' boon'))
        return res
    def full_descr(self):
        gods = '+'.join(self.gods).replace('\n', '')
        return f"**Duo Boon {self.name} ({gods})** - {self.descr}\nRequirements: {self.requirements}"
    def __repr__(self):
        return f"<DuoBoon {'+'.join(self.gods)} {self.name}>"

class LegendaryBoon(WikiItem):
    def __init__(self, name, descr, god, requirements):
        super().__init__(name)
        self.god = god
        self.descr = descr
        self.requirements = requirements

    def key_names(self):
        res =  [ _clean_name(self.name) ]
        for possessive in ['', "'s"]:
            res.append(_clean_name(self.god+possessive+' legendary boon'))
            res.append(_clean_name(self.god+possessive+' legendary'))
        return res
    def full_descr(self):
        return f"**Legendary Boon {self.name} ({self.god})** - {self.descr}\nRequirements: {self.requirements}"
    def __repr__(self):
        return f"<Legendary Boon {self.god} {self.name}>"

class Keepsake(WikiItem):
    def __init__(self, name, source, descr):
        super().__init__(name)
        self.source = source
        self.descr = descr
        self.item_type = 'Keepsake'

    def key_names(self):
        res =  [ _clean_name(self.name) ]
        for possessive in ['', "'s"]:
            res.append(_clean_name(self.source+possessive+' '+self.item_type))
            res.append(_clean_name(self.source+possessive+' '+self.name))
        return res

    def full_descr(self):
        return f"**{self.name} ({self.source}'s {self.item_type})** - {self.descr}"
    def __repr__(self):
        return f"<{self.item_type} {self.name} ({self.source})>"

class Companion(Keepsake):
    def __init__(self, name, source, descr):
        super().__init__(name, source, descr)
        self.item_type = 'Companion'

class Character(WikiItem):
    def __init__(self, name, link):
        super().__init__(name)
        self.link = link
    def full_descr(self):
        return f"[{self.name} - Potential Spoilers]({self.link})"
    def __repr__(self):
        return f"<Character {self.name} ({self.link})>"

class MirrorOfNightTalents(WikiItem):
    def __init__(self, name, descr, ranks):
        super().__init__(name)
        self.descr = descr
        self.ranks = ranks

    def full_descr(self):
        return f"{self.name} Talent - Potential Spoilers\nDescr:\n>!{self.descr}!<\nRanks: >!{self.ranks}!<"
    def __repr__(self):
        return f"<MirrorOfNightTalents {self.name}>"
