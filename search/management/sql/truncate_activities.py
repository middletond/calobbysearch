# Truncate activities table (i.e. a faster delete of Activity objects)
TRUNCATE_ACTIVITIES = """truncate table lobbying_activity RESTART IDENTITY CASCADE;"""
