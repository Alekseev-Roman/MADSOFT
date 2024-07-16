from minio import Minio
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = Minio(
    endpoint='127.0.0.1:9000',
    http_client=urllib3.ProxyManager("http://s3_db:9000"),
    access_key="minioadmin",
    secret_key="minioadmin",
    cert_check=False,
    secure=False
)
