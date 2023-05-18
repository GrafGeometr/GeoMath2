import os
from data import db_session
from init_app import app
import importlib

needs_to_import = [
    f[:-3] for f in os.listdir() if f.endswith("_.py")
]

for module in needs_to_import:
    importlib.import_module(module)


def main():
    db_session.global_init("database/data.db")

    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=8000, host="127.0.0.1")


if __name__ == "__main__":
    main()
