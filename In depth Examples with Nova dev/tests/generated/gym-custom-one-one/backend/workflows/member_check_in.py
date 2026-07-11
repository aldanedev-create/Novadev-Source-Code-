"""Workflow generated for MemberCheckIn."""

def describe():
    return [{'kind': 'input', 'name': 'Member', 'props': {}}, {'kind': 'uses', 'name': 'GymTools.status', 'props': {}}, {'kind': 'creates', 'name': 'CheckIn', 'props': {}}]

USES = 'GymTools.status'
CREATES = ['CheckIn']
