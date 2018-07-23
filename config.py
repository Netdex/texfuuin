config = {
    # application info
    'name': "texfuuin",
    'db_path': "./texfuuin-db.json",
    'port': 5000,
    'devel': False,

    # user management
    'default_user': "anonymous",
    'admin_trip': "50a3cf2",
    'trip_salt': "kasdjhfkasdhfklasjdhfksjadhfkljahsdlkjfhlskj",

    # validation
    'uname_limit': 32,
    'title_limit': 32,
    'message_limit': 5000,

    # error
    'error_msgs': {
        'post-id': """The specified post could not be found.""",
        'uname-limit': """The specified username is not valid.""",
        'title-limit': """The specified title is not valid.""",
        'message-limit': """The specified message is not valid.""",
        'no-auth': """The specified tripcode is incorrect."""
    }
}
