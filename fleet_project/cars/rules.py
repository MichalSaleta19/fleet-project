import rules


@rules.predicate
def is_authenticated(user):
    return user.is_authenticated


@rules.predicate
def is_client(user):
    return user.groups.filter(name="Clients").exists()


@rules.predicate
def is_driver(user):
    return user.groups.filter(name="Drivers").exists()


@rules.predicate
def is_fleet_manager(user):
    return user.groups.filter(name="FleetManagers").exists()


@rules.predicate
def fleet_manager_or_driver_required(user):
    return is_fleet_manager(user) and is_driver(user)


@rules.predicate
def fleet_manager_or_client_required(user):
    return is_fleet_manager(user) and is_client(user)


@rules.predicate
def driver_or_client_required(user):
    return is_driver(user) and is_client(user)


rules.add_rule("is_authenticated", is_authenticated)
rules.add_rule("is_client", is_client)
rules.add_rule("is_driver", is_driver)
rules.add_rule("is_fleet_manager", is_fleet_manager)
rules.add_rule("is_fleet_manager_or_driver", fleet_manager_or_driver_required)
rules.add_rule("is_fleet_manager_or_client", fleet_manager_or_client_required)
rules.add_rule("is_driver_or_client", driver_or_client_required)
