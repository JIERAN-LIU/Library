class Constant(object):
    BINDINGS = (
        ('Paperback', 'Paperback'),
        ('Hardback', 'Hardback'),
        ('Thread', 'Thread')
    )
    BOOK_SUBJECTS = (
        ('General Works', 'General Works'),
        ('Philosophy (General) ', 'Philosophy (General) '),
        ('Auxiliary Sciences of History', 'Auxiliary Sciences of History'),
        ('History', 'History'),
        ('History of America', 'History of America'),
        ('Local History of America', 'Local History of America'),
        ('Geography', 'Geography'),
        ('Social sciences', 'Social sciences'),
        ('Political Science', 'Political Science'),
        ('Law', 'Law'),
        ('Education', 'Education'),
        ('Music', 'Music'),
        ('Fine arts', 'Fine arts'),
        ('Language and Literature', 'Language and Literature'),
        ('Science', 'Science'),
        ('Medicine', 'Medicine'),
        ('Agriculture', 'Agriculture'),
        ('Technology', 'Technology'),
        ('Military Science', 'Military Science'),
        ('Naval science', 'Naval science'),
        ('Library Science. Information Resources (General)', 'Library Science. Information Resources (General)')
    )

    BOOK_SUBJECT_CODE = {
        'General Works': 'A',
        'Philosophy (General) ': 'B',
        'Auxiliary Sciences of History': 'C',
        'History': 'D',
        'History: America': 'F',
        'Geography': 'G',
        'Social sciences': 'H',
        'Political Science': 'J',
        'Law': 'K',
        'Education': 'L',
        'Music': 'M',
        'Fine arts': 'N',
        'Language and Literature': 'P',
        'Science': 'Q',
        'Medicine': 'R',
        'Agriculture': 'S',
        'Technology': 'T',
        'Military Science': 'U',
        'Naval science': 'V',
        'Library Science. Information Resources (General)': 'Z'
    }

    LANGUAGES = (
        ('Thai', 'Thai'),
        ('English', 'English'),
        ('Chinese(Simplified)', 'Chinese(Simplified)'),
        ('Chinese(Traditional)', 'Chinese(Traditional)'),
        ('Spanish', 'Spanish'),
        ('German', 'German'),
        ('French', 'French'),
        ('Japanese', 'Japanese')
    )
    PAY_METHODS = (
        ('Cash', 'Cash'),
        ('Paypal', 'Paypal'),
        ('Credit card', 'Credit card')
    )
    PAY_METHOD_CASH = 'Cash'
    CURRENCY_SYMBOLS = (
        ('THB', '฿'),
        ('USD', '$'),
        ('CNY', '￥'),
        ('GBP', '￡'),
        ('DEM', 'DM.'),
        ('FRP', 'FF'),
        ('ESP', 'Pts.'),
        ('JPY', 'J.'),
    )
    CURRENCY_SYMBOL_THB = '฿'

    BOOK_COPY_STATUS = (
        ('Available', 'Available'),
        ('On-Borrowing', 'On Borrowing'),
        ('Deleted', 'Deleted'),
    )

    BOOK_COPY_STATUS_ON_BORROWING = 'On Borrowing'

    BOOK_STATUS = (
        ('Available', 'Available'),
        ('Deleted', 'Deleted'),
    )

    BOOK_STATUS_DELETED = 'Deleted'
    BOOK_STATUS_AVAILABLE = 'Available'

    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    )

    GENDERS_UNKNOWN = 'Unknown'

    BOOK_MEDIA_TYPE = (
        ('Text-Book', 'Text Book'),
        ('Printed-Text', 'Printed Text'),
        ('Thesis', 'Thesis'),
        ('Video', 'Video'),
        ('Sound-Recording', 'Sound Recording'),
        ('E-Document', 'Electronic Document'),
        ('Multimedia-Document', 'Multimedia Document'),
    )

    BORROW_ACTION = (
        'Return',
        'Renew',
        'Fine'
    )

    BORROW_ACTION_RETURN = 'Return'
    BORROW_ACTION_RENEW = 'Renew'
    BORROW_ACTION_FINE = 'Fine'

    NATIONALITY = (
        ('Chinese', 'Chinese'),
        ('American', 'American'),
        ('German', 'German'),
        ('Japanese', 'Japanese'),
        ('English', 'English'),
        ('French', 'French'),
        ('Thai', 'Thai'),
    )

    MAX_BORROW_DAY = 7

    ROLES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Reader', 'Reader'),
    )

    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_READER = 'Reader'
