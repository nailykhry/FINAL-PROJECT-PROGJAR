import bcrypt

class HashClass:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_password_hex = hashed_password.decode('utf-8')
        return hashed_password_hex

    @staticmethod
    def verify_password(password, hashed_password):
        try:
            password_bytes = password.encode('utf-8')
            hashed_password_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_password_bytes)
        except bcrypt.error as e:
            return False

# # TEST
# # Hash password
# password = "password123"
# hashed_password = HashClass.hash_password(password)
# print("Hashed Password:", hashed_password)

# # Verifikasi password
# input_password = "password123"
# is_verified = HashClass.verify_password(input_password, hashed_password)
# if is_verified:
#     print("Password cocok!")
# else:
#     print("Password tidak cocok!")
