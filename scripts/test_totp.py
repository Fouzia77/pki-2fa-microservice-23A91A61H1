import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.totp_utils import generate_totp_code, verify_totp_code

hex_seed = "aca9248155fad9e07bb4183425b42c1f72b39f1e6c226223968e9b574ab9b5c9"



code = generate_totp_code(hex_seed)
print("Generated OTP:", code)

is_valid = verify_totp_code(hex_seed, code)
print("Is valid:", is_valid)