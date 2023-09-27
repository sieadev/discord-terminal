import requests
from util import login

print('''██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║█████╗██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║╚════╝██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
''')

session = requests.Session()
session.headers.update({
    'Accept': 'application/json'
})

tokenLogin = bool(input("Use Token?(true/false): "))
if tokenLogin:
    while True:
        token = str(input("Token: "))
        fingerPrint = login.StartWithToken(session)
        if fingerPrint is "None":
            print("This token is not valid")
        else:
            print("Successfully logged in.")
            break
else:
    email = str(input("E-Mail: "))
    psw = str(input("Password: "))
    loginReturns = login.Start(session, email, psw)
    fingerPrint = loginReturns[0]
    token = loginReturns[1]
    print(token)
    print(fingerPrint)