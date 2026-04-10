from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.x509 import SubjectAlternativeName, IPAddress
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import ipaddress

SERVER_IP = "10.172.156.238"   # 🔴 CHANGE THIS

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CN Project"),
    x509.NameAttribute(NameOID.COMMON_NAME, SERVER_IP),
])

cert = x509.CertificateBuilder().subject_name(subject)\
.issuer_name(issuer)\
.public_key(key.public_key())\
.serial_number(x509.random_serial_number())\
.not_valid_before(datetime.datetime.utcnow())\
.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
.add_extension(
    SubjectAlternativeName([IPAddress(ipaddress.IPv4Address(SERVER_IP))]),
    critical=False
)\
.sign(key, hashes.SHA256())

with open("server.key", "wb") as f:
    f.write(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()
    ))

with open("server.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Certificate generated for:", SERVER_IP)