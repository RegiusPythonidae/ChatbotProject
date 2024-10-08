from extensions import app
from routes import home, login, register, logout, contact, profile

app.run(host="0.0.0.0", debug=True)