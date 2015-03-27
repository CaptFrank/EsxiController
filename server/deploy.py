__author__ = 'fpapinea'

# Create a log file under /var/log/esxicontroller

# Create Tables
"""
    # Create base tables
    db.session.add(EngineStatus())
    db.session.add(WebStatus())
    db.session.add(CommandStats(COMMAND_SOURCE_WEB))
    db.session.add(CommandStats(COMMAND_SOURCE_ENGINE))
    db.session.commit()
    """