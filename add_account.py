import sys
import time
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication

ACCESS_INFO = None
app = None
print("Press CTRL+Z to close the browser.")
time.sleep(1)

def perform_account_addition(ACCESS_INFO):
    parts = ACCESS_INFO.split('%')
    user_id = parts[0]
    p_constants = f"user_id = '{user_id}'\nACCESS_INFO = '{ACCESS_INFO}'"
    with open('private_constants.py', 'w') as file:
        file.write(p_constants)
        print("Account added successfully.")

# Close the application
def close_app():
    global app
    if app:
        app.quit()

# Start qapp
app = QApplication([])

# Captures cookie of interest and save to storage.
is_adding = False
def on_cookie_added(cookie):
    
    global is_adding
    if is_adding:
        return
    is_adding = True
    
    global ACCESS_INFO, scapmpid, scsession
    cookie_name = cookie.name().data().decode()
    cookie_value = cookie.value().data().decode()
    if cookie_name == "ACCESS_INFO":
        ACCESS_INFO = cookie_value
    if ACCESS_INFO:
        print("Adding account...")
        perform_account_addition(ACCESS_INFO)
        store.deleteAllCookies()
        close_app()
    else:
        is_adding = False

view = QWebEngineView()
page = QWebEnginePage()

# Access the cookie store via the page
store = page.profile().cookieStore()

# Clear existing cookies
store.deleteAllCookies()

# Connect a slot to the cookieAdded signal
store.cookieAdded.connect(on_cookie_added)

user_agent = page.profile().httpUserAgent()
view.setPage(page)

# Load a URL
url = QUrl("https://www.streamraiders.com")
view.setUrl(url)

view.show()
app.exec_()