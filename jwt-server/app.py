from flask import Flask, jsonify, request
from jose import jwt
import json

app = Flask(__name__)

# Load your JWKS from the file
with open("jwks.json", "r") as f:
    jwks = json.load(f)

@app.route('/.well-known/jwks.json')
def jwks_endpoint():
    return jsonify(jwks)

@app.route('/verify_jwt', methods=['POST'])
def verify_jwt_endpoint():
    try:
        token = request.get_json().get('token')
        if not token:
            return jsonify({"error": "Missing token"}), 400

        # Verify the JWT using the JWKS
        decoded_token = jwt.decode(
            token,
            jwks, 
            algorithms=['RS256'], 
            audience='YOUR_AUDIENCE', 
            issuer='YOUR_ISSUER' 
        )

        return jsonify({"message": "Token verified successfully", "decoded": decoded_token})
    except jwt.JWTDecodeError as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')