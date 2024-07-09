from minio import Minio
import urllib3
import io


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
client = Minio('127.0.0.1:9000', access_key="minioadmin", secret_key="minioadmin", cert_check=False)

client.put_object('madsoft-test-task', 'test', io.BytesIO(b'gggg'), 4)
