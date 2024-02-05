class DBInfo:
    dbname = "ScamDataDB"
    connectname = f"{dbname}.db"
    init_script_path = "src/scripts/createdb.sql"


class HTMLPages:
    class Path:
        home = "src/pages/HomePage.html"
