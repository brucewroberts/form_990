import sys

import app

if __name__ == '__main__':
    application = app.create_app()

    if len(sys.argv) == 2 and sys.argv[1] == 'https':
        application.run( host='0.0.0.0', port = '5001', ssl_context='adhoc' )
    else:
        application.run( host='0.0.0.0', port = '5001' )

