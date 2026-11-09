import requests # type: ignore
from openpyxl import Workbook # type: ignore

def check_ip(ip_address, api_key, ws):
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'
    headers = {'x-apikey': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if 'data' in result:
            data = result['data']['attributes']
            as_owner = data.get('as_owner', 'N/A')
            country = data.get('country', 'N/A')
            community_score = data.get('last_analysis_stats', {}).get('malicious', 0) + \
                              data.get('last_analysis_stats', {}).get('suspicious', 0) + \
                              data.get('last_analysis_stats', {}).get('Phishing', 0) + \
                              data.get('last_analysis_stats', {}).get('malware', 0)
            last_analysis_results = data.get('last_analysis_results', {})
            
            # Count detections
            detection_count = 0
            for result in last_analysis_results.values():
                if result['result'] in ['suspicious', 'malware', 'malicious', 'phishing']:
                    detection_count += 1
            
            # Get details of each detection 
            suspicious = []
            malware = []
            malicious = []
            phishing = []
            clean = []
            for vendor, result in last_analysis_results.items():
                if result['result'] == 'suspicious':
                    suspicious.append(vendor)
                elif result['result'] == 'malware':
                    malware.append(vendor)
                elif result['result'] == 'malicious':
                    malicious.append(vendor)
                elif result['result'] == 'phishing':
                    phishing.append(vendor)
                elif result['result'] == 'clean':
                    clean.append(vendor)
            
            ws.append([
                ip_address, 
                as_owner, 
                country, 
                detection_count,
                ', '.join(suspicious),
                ', '.join(malware),
                ', '.join(malicious),
                ', '.join(phishing),
                ', '.join(clean)
            ])

        else:
            ws.append([ip_address, 'No information available', '', '', '', '', '', '', ''])
    else:
        ws.append([ip_address, 'Error occurred while querying VirusTotal API', '', '', '', '', '', '', ''])

def main():
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual VirusTotal API key
    file_path = 'listip.txt'

    wb = Workbook()
    ws = wb.active
    ws.append(['IP Address', 'AS Owner', 'Country', 'Detection', 'Suspicious', 'Malware', 'Malicious', 'Phishing', 'Clean'])

    try:
        with open(file_path, 'r') as file:
            ip_addresses = file.readlines()
            for ip_address in ip_addresses:
                ip_address = ip_address.strip()
                check_ip(ip_address, api_key, ws)
        
        wb.save("virus_total_results.xlsx")
        print("Results have been saved to virus_total_results.xlsx")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    
if __name__ == "__main__":
    main()