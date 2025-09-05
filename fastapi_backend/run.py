from app import app

if __name__ == "__main__":
    # Run in debug false by default for safety; host 0.0.0.0 for container use
    app.run(host="0.0.0.0", port=5000, debug=False)
