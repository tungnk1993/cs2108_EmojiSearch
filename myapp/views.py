from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json, traceback
# Create your views here.
@csrf_exempt
def hello(request):
	return render(request, 'hello.html', {'message': 'nkt'})

@csrf_exempt
def test(request):
	emoji_list = []
	for i in range(43):
		emoji_list.append(''.join([str(i), '.png']))
	return render(request, 'index.html', {'emoji_list': emoji_list})

@csrf_exempt
def process_query(main_query, rf_query):
	try:
		query_main = [int(item) for item in json.loads(main_query[0])]
		query_rf = [int(json.loads(rf_query[0]))]

		print 'FINAL MAIN QUERY = ', query_main
		print 'FINAL RF QUERY = ', query_rf

		URL = 'C:\\Users\\User\\Desktop\\CS2108_A3\\features\\'
		MAIN_FACTOR = 0.8
		RF_FACTOR = 0.2

		result_array = {}
		for emo_id in query_main:
			features_path = ''.join([URL, str(emo_id), '.txt'])
			features_file = open(features_path, 'r')
			for line in features_file:
				image_name, value = line.strip().split(' ')
				print image_name, value
				if image_name not in result_array:
					result_array[image_name] = 0.0
				result_array[image_name] = result_array[image_name] + MAIN_FACTOR * float(value)
			features_file.close()
			MAIN_FACTOR *= 0.9

		for emo_id in query_rf:
			features_path = ''.join([URL, str(emo_id), '.txt'])
			features_file = open(features_path, 'r')
			for line in features_file:
				image_name, value = line.strip().split(' ')
				print image_name, value
				if image_name not in result_array:
					result_array[image_name] = 0.0
				result_array[image_name] = result_array[image_name] + RF_FACTOR * float(value)
			features_file.close()

		print '-------------------------'
		result_list = []
		for key in result_array:
			new_tuple = (key, result_array[key])
			result_list.append(new_tuple)

		final_list = sorted(result_list, key=lambda tup: -tup[1])
		return_list = final_list[:10]
		for result in return_list:
			print result

		return return_list
	except:
		traceback.print_exc()

@csrf_exempt
def query(request):
	print "AJAX Contact"
	if request.is_ajax() or request.method == "POST":
		try:
			query_data = dict(request.POST)
			print "Main query = ", query_data["query"]
			print "RF = ", query_data["rf"]
			
			image_list = process_query(query_data["query"], query_data["rf"])

			output_list = [item[0] for item in image_list]

			print output_list
			json_response = json.dumps(output_list)
			return HttpResponse(json_response, content_type='application/json')
		except:
			traceback.print_exc()



