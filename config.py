config = {
    # application info
    'name': "texfuuin",                                             # navbar application name
    'db_path': "./texfuuin-db.json",                                # path to tinydb file
    'port': 5000,                                                   # port to listen in production mode
    'devel': True,                                                 # use gevent or flask server

    'recaptcha-sitekey': "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
    'recaptcha-secretkey': "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",

    # user management
    'default_user': "anonymous",                                    # user default in new post form
    'admin_trip': "50a3cf2",                                        # tripcode of admin
    'trip_salt': "kasdjhfkasdhfklasjdhfksjadhfkljahsdlkjfhlskj",    # salt added to tripcode

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
        'no-auth': """The specified tripcode is incorrect.""",
        'captcha': """The captcha is incorrect."""
    }
}
