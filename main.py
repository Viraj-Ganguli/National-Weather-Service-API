import requests
import json

test_mode = True # True for debug mode, False to make live API requests to NWS

# list of states
states =['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']

def main():
	
	while True:
		print("Weather Menu Options")
		print("----------------------")
		print("1) Get NWS weather terms")
		print("2) Get aviation alerts for the DC area")
		print("3) Get weather alert counts by state")
		print("4) Get all weather alerts for a state")
		print("5) Get Fairfax, VA Forecast")
		print("6) EXIT")
		
		choice = int(input("\nWhich option (type number): "))
		if choice == 1:
		  get_weather_terms()
		elif choice == 2:
		  get_aviation_alerts()
		elif choice == 3:
		  get_alert_counts()
		elif choice == 4:
		  get_state_alerts()
		elif choice == 5:
		  get_fairfax_weather()
		elif choice == 6:
		  break
		else:
		  print("Please type a valid selection")


def get_weather_terms():
	print("WEATHER TERMS")
	url = "https://api.weather.gov/glossary"
	nws_dict = connect_to_endpoint(url)
	glossary = nws_dict["glossary"]
	
	for item in glossary:
		print("TERM: " + str(item["term"]))
		print("DEFINITION: " + str(item["definition"]))
		print()
	  

def get_aviation_alerts():
	url = "https://api.weather.gov/aviation/cwsus/ZDC/cwas"
	print("\nDMV AREA AVIATION ALERTS")
	print("========================")
	nws_dict = connect_to_endpoint(url)
	alerts = nws_dict["features"] #get features list from dict that has alerts
	
	if len(alerts) == 0:
		print("There are no current aviation alerts in the DMV")
	else:
		print("There are " + str(len(alerts)) + " aviation alerts for the DMV.\n\n")
		for alert in alerts:
			print("EFFECTIVE: " + alert["properties"]["issueTime"])
			print("HEADLINE: " + alert["properties"]["text"])
			print()


def get_alert_counts():
  url = "https://api.weather.gov/alerts/active/count"
  nws_dict = connect_to_endpoint(url)
  state_alerts = nws_dict["areas"]

  for state in state_alerts:
          print(state, state_alerts[state])
        # TBD YOUR CODE HERE
	#TBD YOUR CODE HERE 
	#Look at alert_counts.json for a sample JSON response
	#Loop Over the state_alerts dictionary and print out count of alerts






def get_state_alerts():
	#prompt the user for state and get alerts  
  while True:
    state = input("\nEnter a state abbreviation:").upper()
    if state in states:
      break
    else:
      print("Invalid state entered.")
	
  url = "https://api.weather.gov/alerts/active?area=" + state
  nws_dict = connect_to_endpoint(url)
  alertInfo = nws_dict["features"][0]["properties"]
  print("===============================================================")
  print(alertInfo["headline"])
  print("===============================================================")
  print(alertInfo["effective"])
  print("===============================================================")
  print(alertInfo["description"])
  print("===============================================================")
  
	#TBD YOUR CODE HERE
	#Look at alerts.json for a sample JSON response
	#Connect to the NWS and get alerts for a state, then print those alerts out
	

def get_fairfax_weather():
	#Fairfax county area weather zone
  url = "https://api.weather.gov/zones/forecast/VAZ053/forecast"
  nws_dict = connect_to_endpoint(url)
  FCInfo = nws_dict["properties"]["periods"]
  print("\nFAIRFAX VA 7-DAY FORECAST")
  print("=========================")
  for entry in FCInfo:
    print(entry["name"].upper(), ":")
    print(
          "☀️ " if "sunny" in entry["detailedForecast"]
          else "🌙 " if "clear" in entry["detailedForecast"]
          else "⛅ " if "partly" in entry["detailedForecast"]
          else "🌧️ " if "rain" in entry["detailedForecast"]
          else "❄️ " if "snow" in entry["detailedForecast"]
          else "☁️ " if "cloud" in entry["detailedForecast"]
          else "",
          entry["detailedForecast"]
    )
    print("===============================================")

  
  
	#TBD YOUR CODE HERE
	#Look at fairfax.json for a sample JSON response
	#Loop over the periods dictionary and print the forecast
	#You must include weather symbol graphics (emojis) per the lab documentation



def connect_to_endpoint(url):
	# TRY TO CONNECT TO NWS API
	try:
		if not test_mode:
			response = requests.get(url)
	
		if response.status_code != 200:
			print("Error: Invalid request")
			#return a blank dictionary
			return {}
		
		#get JSON response
		response_dict = response.json()
		
		#save JSON for debugging uses
		with open('data.json', 'w') as fp:
			json.dump(response_dict, fp)
	#CALL THIS CODE IF IN FIREWALL MODE, OPENS LOCAL JSON DATA FILE
	except:
		print("ALERT: You are in Firewall mode")

		if "glossary" in url:
			file = "terms.json"
		elif "count" in url:
			file = "alert_counts.json"
		elif "aviation" in url:
			file = "aviation.json"
		elif "area" in url:
			file = "alerts.json"
		elif "forecast" in url:
			file = "fairfax.json"

		with open(file, 'r') as fp:
			response_dict = json.load(fp)
	
	return response_dict


if __name__ == "__main__":
  main()