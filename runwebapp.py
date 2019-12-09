"""Run the webapp from here"""

from app import KKWEBAPP

if __name__ == "__main__":
    KKWEBAPP.run(host="0.0.0.0", port=8080, debug=True)
