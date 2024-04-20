import rules

@rules.predicate
def is_fleet_manager(user):
    # Sprawdź czy użytkownik ma rolę zarządcy floty
    return user.is_authenticated and user.groups.filter(name='Fleet Managers').exists()

rules.add_perm('app.add_car', is_fleet_manager)