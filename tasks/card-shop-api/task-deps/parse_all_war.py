import re
import json
from pathlib import Path

war_data = {}

# Parse each HTML file
html_files = list(Path('.').glob('*.shtml'))

for html_file in html_files:
    with open(html_file, 'r') as f:
        content = f.read()
    
    # Extract player name from title
    title_match = re.search(r'<title>([^<]+?) Stats', content)
    if not title_match:
        continue
    player_name = title_match.group(1)
    
    # Find all rows in the standard batting table
    row_pattern = r'<tr id="players_standard_batting\.(\d{4})"[^>]*>(.*?)</tr>'
    rows = re.findall(row_pattern, content, re.DOTALL)
    
    player_years = {}
    for year, row_content in rows:
        # Extract WAR from the row
        war_match = re.search(r'data-stat="b_war"[^>]*csk="([^"]+)"', row_content)
        if war_match:
            war_value = float(war_match.group(1))
            player_years[int(year)] = war_value
    
    if player_years:
        war_data[player_name] = player_years

# Print organized by player
for player_name in sorted(war_data.keys()):
    print(f"\n{player_name}:")
    years = war_data[player_name]
    for year in sorted(years.keys()):
        print(f"  {year}: {years[year]:.2f}")
    # Find best year
    best_year = max(years.items(), key=lambda x: x[1])
    print(f"  Best: {best_year[0]} with WAR {best_year[1]:.2f}")

# Save to JSON for programmatic access
with open('war_data_parsed.json', 'w') as f:
    json.dump(war_data, f, indent=2)

