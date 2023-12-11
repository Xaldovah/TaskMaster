from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_connection_str = "mysql+pymysql://qbzm5siluzulex65h9g1:pscale_pw_nYCPFy1sNYyC5xhKxbDu2bSAorwCGzUlt8AaMSMb7Pj@aws.connect.psdb.cloud/task_master?charset=utf8mb4"

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
