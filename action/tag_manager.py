#!/usr/bin/python
# -*- coding: utf-8 -*-

from action import base_manager
from entity import tag as tag_entity
from helper import hint
from helper import translator

class TagManager(base_manager.BaseManager):
    """ Handle tag related actions.

    Member:
    db -- The database connection.
    hints -- List of hints which occurred during action handling (list hint).
    """

    def __init__(self, db):
        self.db = db
        self.hints = []

    def action(self, language):
        """ Handle action for given class name. Returns found entities. """
        _ = translator.Translator.instance(language)

        # Handle actions.
        action = self.get_form('action') or 'show'

        if action == 'new':
            name = self.get_form('name')
            if self.__name_ok(name, language):
                tag = tag_entity.Tag(name=name)
                tag.save(self.db)
                hint_text = _('New tag "{}" has been created.').format(name)
                self.hints.append(hint.Hint(hint_text))

        elif action == 'new-synonym':
            parent = self.get_form('id')
            name = self.get_form('name')
            if self.__name_ok(name, language):
                tag = tag_entity.Tag(name=name, synonym_of=parent)
                tag.save(self.db)
                hint_text = _('New synonym "{}" has been created.').format(name)
                self.hints.append(hint.Hint(hint_text))

        elif action == 'edit':
            is_delete = self.get_form('delete') is not None
            id = int(self.get_form('id'))
            name = self.get_form('name')
            entity = tag_entity.Tag.find_pk(self.db, id)
            entity.name = name

            if is_delete:
                entity.delete(self.db)
                hint_text = _('Tag "{}" has been removed.').format(name)
                self.hints.append(hint.Hint(hint_text))
            else:
                if self.__name_ok(name, language):
                    entity.save(self.db)
                    hint_text = _('Tag "{}" has been updated.').format(name)
                    self.hints.append(hint.Hint(hint_text))

        # Load content.
        return tag_entity.Tag.find_all(self.db)

    def __name_ok(self, name, language):
        """ Validates the name. Returns True if ok. """
        _ = translator.Translator.instance(language)

        if not name:
            hint_text = _('Name must not be empty.').format(name)
            self.hints.append(hint.Hint(hint_text))
            return False

        exists = tag_entity.Tag.name_exists(self.db, name)
        if exists:
            hint_text = _('Tag "{}" already exists.').format(name)
            self.hints.append(hint.Hint(hint_text))
        return not exists