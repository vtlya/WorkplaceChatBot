from r_model import curator

DB = 'd607u0guj5vloh'
DB_USER = 'enileogmsyfxbb'
DB_HOST = 'ec2-54-220-0-91.eu-west-1.compute.amazonaws.com'
DB_PW = '48ff0ca4fab391c673ef87723ecd0e79af69a70020c94437302790667922682c'

curator_info = curator(DB, DB_USER, DB_HOST, DB_PW)

print(str(curator_info.get_curator(32)))