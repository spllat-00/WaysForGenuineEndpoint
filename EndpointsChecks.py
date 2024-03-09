import requests
import json

def statusChecks(URL:str, endpoints:list) -> None:
  finalDict = {"valid":[], "invalid":[]}
  for endpoint in endpoints:
    res = requests.get(url=f"{URL}/{endpoint}")
    if 200 <= res.status_code < 300:
      finalDict["valid"].append(endpoint)
    else:
      finalDict["invalid"].append(endpoint)
  print(json.dumps(finalDict, indent=4))

def characterChecks(URL:str, endpoints:list) -> None:
  finalDict = {"valid":[], "invalid":[]}
  for endpoint in endpoints:
    res = requests.get(url=f"{URL}/{endpoint}")
    data = res.text
    if "We're sorry, we seem to have lost this page, but we don't want to lose you." in data and "Page Not Found" in data:
      finalDict["invalid"].append(endpoint)
    else:
      finalDict["valid"].append(endpoint)
  print(json.dumps(finalDict, indent=4))

def pageSizes(URL:str, endpoints:list) -> None:
  finalDict = {"valid":[], "invalid":[]}
  for endpoint in endpoints:
    res = requests.get(url=f"{URL}/{endpoint}")
    data = res.text
    if 180000 < len(data):
      finalDict["invalid"].append(endpoint)
    else:
      finalDict["valid"].append(endpoint)
  print(json.dumps(finalDict, indent=4))

def characterSimilarity(URL:str, endpoints:list) -> None:

  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.metrics.pairwise import cosine_similarity

  vectorizer = TfidfVectorizer()
  invalidPage = requests.get(url=f"{URL}/thisEndpointWillNeverExistInThisWorldAsThisWillNeverBeCreated").text
  finalDict = {"valid":[], "invalid":[]}
  for endpoint in endpoints:
    data = requests.get(url=f"{URL}/{endpoint}").text
    vectors = vectorizer.fit_transform([invalidPage, data])
    # Calculate the cosine similarity between the vectors
    similarity = cosine_similarity(vectors)[0, 1]
    if 0.8 < similarity:
      finalDict["invalid"].append(endpoint)
    else:
      finalDict["valid"].append(endpoint)
  print(json.dumps(finalDict, indent=4))

def titleChecks(URL:str, endpoints:list) -> None:
  from bs4 import BeautifulSoup

  finalDict = {"valid":[], "invalid":[]}
  for endpoint in endpoints:
    resText = requests.get(url=f"{URL}/{endpoint}").text

    soup = BeautifulSoup(resText, 'html.parser')
    title = soup.find("title").text

    if title == "Page Not Found":
      finalDict["invalid"].append(endpoint)
    else:
      finalDict["valid"].append(endpoint)
  print(json.dumps(finalDict, indent=4))

if __name__ == "__main__":
  baseURL="https://timesofindia.indiatimes.com/"
  endpoints=[
    "india",
    "business",
    "dogs", # Doesn't Exist
    "usa" # Doesn't Exist
  ]
  
  try:
    userInput = int(input("Choose a method to test with:\n\t1. Status Code\n\t2. Character Check\n\t3. Page Size\n\t4. Character Similarity\n\t5. Title Checking\n\t9. Exit\nSelect Option: "))
  except ValueError:
    print(f"Give the correct input.")
    exit()
  if userInput == 1:
    statusChecks(baseURL, endpoints)
  elif userInput == 2:
    characterChecks(baseURL, endpoints)
  elif userInput == 3:
    pageSizes(baseURL, endpoints)
  elif userInput == 4:
    characterSimilarity(baseURL, endpoints)
  elif userInput == 5:
    titleChecks(baseURL, endpoints)
  elif userInput == 9:
    print("Exiting...")
    exit()
  else:
    print("Not a valid option.\n\tExiting...")
    exit()