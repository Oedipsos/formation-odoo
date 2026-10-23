from refuge.models.species import Dragon, Phoenix, Unicorn, StatueDragon


def end_of_day_report(residents: list) -> None:
    for resident in residents:
        print(f"--- {resident.name} ---")
        print(resident.special_ability())
        print(f"Mission duration if sent: {resident.mission_duration_days()} days")
        print(resident)


end_of_day_report([Dragon("&", "d", 42, "f")])
end_of_day_report([Phoenix("&", "d", 42)])
end_of_day_report([Unicorn("&", "d", 42)])
end_of_day_report([StatueDragon("&", "d", 42, "f")])
