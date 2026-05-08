import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app

app = create_app('development')
with app.app_context():
    rules = sorted([(r.rule, sorted(r.methods - {'HEAD','OPTIONS'})) for r in app.url_map.iter_rules()])
    for rule, methods in rules:
        print(f"{rule} -> {','.join(methods)}")
