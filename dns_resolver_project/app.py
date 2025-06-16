from flask import Flask, render_template, request, jsonify
from backend.resolver import resolve_dns

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/resolve')
def resolve():
    domain = request.args.get("domain", "").strip()
    record_type = request.args.get("record_type", "A").strip()
    dns_server = request.args.get("dns_server", "8.8.8.8").strip()
    reverse = request.args.get("reverse", "false").lower() == "true"

    if not domain:
        return jsonify({"error": "Domain or IP is required."})

    dns_data = resolve_dns(domain, record_type, dns_server, reverse)
    return jsonify(dns_data)

if __name__ == "__main__":
    app.run(debug=True)
