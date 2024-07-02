import requests

# Replace these values with your own
API_KEY = 'fYAk4VbiynSj_9WjjWLrpWk4VmqtdYG5y3K'
API_SECRET = 'LL7vUeTibdXrjdVfuSgQvr'
DOMAIN = 'ciftec.com'
SUBDOMAIN = 'embroidery'

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def get_record_ip():
    headers = {
        'Authorization': f'sso-key {API_KEY}:{API_SECRET}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://api.godaddy.com/v1/domains/{DOMAIN}/records/A/{SUBDOMAIN}', headers=headers)
    return response.json()[0]['data']

def update_dns_record(ip):
    headers = {
        'Authorization': f'sso-key {API_KEY}:{API_SECRET}',
        'Content-Type': 'application/json'
    }
    payload = [{
        'data': ip,
        'ttl': 600  # Time to live in seconds
    }]
    response = requests.put(f'https://api.godaddy.com/v1/domains/{DOMAIN}/records/A/{SUBDOMAIN}', json=payload, headers=headers)
    return response.status_code == 200

def main():
    public_ip = get_public_ip()
    current_ip = get_record_ip()
    
    if public_ip != current_ip:
        if update_dns_record(public_ip):
            print(f'Successfully updated IP to {public_ip}')
        else:
            print('Failed to update DNS record')
    else:
        print('No update needed, IP has not changed')

if __name__ == '__main__':
    main()
