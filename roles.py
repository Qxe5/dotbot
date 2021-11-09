def get_role(role_string, roles):
    for role in roles:
        if role.name == role_string:
            return role

def roles_tostring(roles):
    return [role.name for role in roles]

def isTrainee(member):
    return 'Staff Trainee' in roles_tostring(member.roles)

def isStaff(member):
    return 'Server Staff' in roles_tostring(member.roles)

def isMod(member):
    return 'Chat Moderator' in roles_tostring(member.roles)
