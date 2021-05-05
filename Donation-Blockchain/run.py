from app import app,results
import sys
import argparse
import re
from app import static_data as sd

if __name__ == "__main__":

    """
    se ejecuta como python run.py localhost 5000 192.168.1.67 5000 True
    """
    app.run(host=results.ip_cliente,port=results.puerto_cliente, use_reloader=False)