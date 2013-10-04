from bottle import request

class ManageIdName:
    """ Action handler for simple id-name-managing pages.

    Member:
    db -- The database connection.
    """

    def __init__(self, db):
        self.db = db

    def handle(self, class_name):
        """ Handle action for given class name. Returns found entities. """
        # Handle actions.
        action = request.forms.get('action') or 'show'
        if action == 'new':
            name = request.forms.get('name')
            cat = class_name(name=name)
            cat.save(self.db)
        elif action == 'edit':
            is_delete = request.forms.get('delete') is not None
            id = request.forms.get('id')
            name = request.forms.get('name')
            entity = class_name(id, name)
            if is_delete:
                entity.delete(self.db)
            else:
                entity.save(self.db)

        # Load content.
        return class_name.find_all(self.db)