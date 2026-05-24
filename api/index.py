from cryptography.fernet import Fernet
import json
from http.server import BaseHTTPRequestHandler
import io
import sys

# === YOUR ENCRYPTED TOOL ===
k = b'u76_X8M9T3V5z_X1L0v_pQ9a2B4n6M8k0L2j4H6G8F0='
c = b'PASTE_YOUR_FULL_ENCRYPTED_STRING_HERE'

def handler(request):
    try:
        cipher = Fernet(k)
        decoded_code = cipher.decrypt(c).decode('utf-8')

        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        exec(decoded_code, globals())

        sys.stdout = old_stdout
        output = mystdout.getvalue()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "message": "Tool Deployed Successfully",
                "output": output if output else "Tool Loaded"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


class VercelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = handler(self)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response["body"].encode())

    def do_POST(self):
        response = handler(self)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response["body"].encode())
