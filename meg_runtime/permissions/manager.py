"""Multimedia Extensible Git (MEG) permissions manager

All users always have the default role. All permissions can be removed from the default role, but the role can never be removed.
"""

#TODO: implement the functions for adding and removing permissions

import json
from meg_runtime.logger import Logger


class PermissionsManager(dict):
    """Permissions manager - one for each repository"""

    def __init__(self, path, user):
        """Load the repository permission file"""
        self._user = user
        self._filepath = path
        self.update({
            "roles": {
                "default": [],
                "admin": []
            },
            "files": {},
            "general": {
                "users_remove_locks": [],
                "roles_remove_locks": ["default", "admin"],
                "users_add_locks": [],
                "roles_add_locks": ["default", "admin"],
                "users_write": [],
                "roles_write": ["default", "admin"],
                "users_grant": [],
                "roles_grant": ["default", "admin"],
                "users_modify_roles": [],
                "roles_modify_roles": ["default", "admin"]
            }
        })
        try:
            self.update(json.load(open(path)))
        except Exception as e:
            # Log that loading the configuration failed
            Logger.warning('MEG Permission: {0}'.format(e))
            Logger.warning('MEG Permission: Could not load permissions file <' + path + '>, using default permissions')
        if 'default' not in self['roles']:
            self['roles']['default'] = []
        if user not in self['roles']['default']:
            self['roles']['default'].append(user)

    def can_lock(self):
        """Return True if the current user can lock a specific path"""
        return self._general_check('roles_add_locks', 'users_add_locks')

    def can_write(self, path):
        """Return True if the current user can write to a specific path"""
        roles = self._get_roles()
        fileHasPermissions = path in self['files']
        for role in roles:
            if role in self['general']['roles_write']:
                return True
            if fileHasPermissions and role in self['files'][path]['roles_write']:
                return True
        if self._user in self['general']['users_write']:
            return True
        if fileHasPermissions and self._user in self['files'][path]['users_write']:
            return True
        return False

    def can_remove_lock(self):
        return self._general_check('roles_remove_locks', 'users_remove_locks')

    def can_grant_permissions(self):
        return self._general_check('roles_grant', 'users_grant')

    def grant_role(self, user, role):
        pass

    def remove_role(self, user, role):
        pass

    def create_role(self, role):
        pass

    def delete_role(self, role):
        pass

    def add_role_permission(self, role, key, file=None):
        """Add a permission to a role
        Defaults to general permission, if file is given, permission will only apply to that file

        Args:
            role (string): role name
            key (string): permission name
            file (string, optional): file path of file to grant role permission to
        """
        pass

    def remove_role_permission(self, role, key, file=None):
        pass

    def add_user_permission(self, user, key, file=None):
        pass

    def remove_user_permission(self, user, key, file=None):
        pass 

    def _general_check(self, roleKey, userKey):
        roles = self._get_roles()
        for role in roles:
            if role in self['general'][roleKey]:
                return True
        if self._user in self['general'][userKey]:
            return True
        return False

    def save(self, filepath=None):
        """Save currenly held permissions / roles to file"""
        if not filepath is None:
            self._filepath = filepath
        json.dump(self, open(self._filepath, 'w+'))

    def _get_roles(self):
        """Get a list of users from the configuration file."""
        return [role for role in self['roles']
                if self._user in self['roles'][role]]
