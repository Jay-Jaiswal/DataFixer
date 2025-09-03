import requests

BASE = 'http://127.0.0.1:8000/api'
CSV_PATH = 'c:/SDC gemni/SDC gemni/test_dirty.csv'

def test_analyze():
    with open(CSV_PATH,'rb') as f:
        files = {'file': ('test_dirty.csv', f, 'text/csv')}
        r = requests.post(f'{BASE}/upload-and-analyze/', files=files)
        print('Analyze status:', r.status_code)
        try:
            print('Analyze response JSON:')
            print(r.json())
        except Exception as e:
            print('Failed to parse JSON:', e)

def test_clean():
    with open(CSV_PATH,'rb') as f:
        files = {'file': ('test_dirty.csv', f, 'text/csv')}
        r = requests.post(f'{BASE}/clean-file/', files=files)
        print('Clean status:', r.status_code)
        print('Content-Type:', r.headers.get('Content-Type'))
        print('First 500 bytes of response:')
        print(r.content[:500])

if __name__ == '__main__':
    test_analyze()
    test_clean()
