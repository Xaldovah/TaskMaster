from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_connection_str = "mysql+pymysql://k3g2212tk6dkgvji7hdo:pscale_pw_7gFM09rPP9HhwhOFU225b8LOK3R6iIzawXOCIEqtGK2@aws.connect.psdb.cloud/task_master?charset=utf8mb4"

engine = create_engine(
    db_connection_str,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem",
        }
    })

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
