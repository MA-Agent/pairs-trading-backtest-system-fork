import json
max_result = {}
from  helpers.model_helper import send_telegram
text = None

with open('backtest_results.json', 'r') as f:
	results_list = json.load(f)
	for result in results_list:
		if 'holdings' not in max_result or max_result['holdings'] < result['holdings']:
			max_result = result
		text = [result['pair'],result['holdings'], result['avg_ratio'], result['num_trades']]
		text = ", ".join(list(map(str,text)))
		print(text)

text = [max_result['pair'],max_result['holdings'], max_result['avg_ratio'], max_result['num_trades']]
text = ", ".join(list(map(str,text)))
send_telegram(text)