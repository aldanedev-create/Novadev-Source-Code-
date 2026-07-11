"""Workflow generated for CreateBooking."""

def describe():
    return [{'kind': 'input', 'name': 'Booking', 'props': {}}, {'kind': 'uses', 'name': 'BookingTools.confirm', 'props': {}}, {'kind': 'creates', 'name': 'Booking', 'props': {}}]

USES = 'BookingTools.confirm'
CREATES = ['Booking']
