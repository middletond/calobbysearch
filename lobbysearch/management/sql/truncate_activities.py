# Truncate activities table (i.e. a faster delete of Activity objects)
TRUNCATE_ACTIVITIES = """truncate table lobbysearch_activity RESTART IDENTITY CASCADE;"""
