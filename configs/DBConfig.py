import os

#DB_URI = "postgres://postgres:1234@localhost:5432/teams"
DB_URI = "postgres://vnprsuimytwqas:86ceac9666a2f4180e730139466598c6a96f0db7c238f9a97fb0fc93c4fa005d@ec2-52-7-39-178.compute-1.amazonaws.com:5432/df8rg8ssjeh1dn"
class DBConfig():
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_CONNECTION_STRING", os.environ.get("SQLALCHEMY_DATABASE_URI", DB_URI))
