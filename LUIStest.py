import requests
import json
  
subscription_key = '8355105d4af94a93804f5debce7cf292'     ## 貼上你的key

def predict_sentence_test(prediction_url, body):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key ,
    }
    url = prediction_url
    response = requests.request("POST", url, data = body, headers=headers)
    response_text = json.loads(response.text)      
    
    # print(response_text)                                                           #print出所有json的資料    
    print("Intent:{}".format(response_text["topScoringIntent"]['intent']))           #單獨print出這個句子的intent
    for i in range(len(response_text["entities"])) :                                 
        print("Entity:{}".format(response_text["entities"][i]["entity"]))            #將所有讀到的entity列印出來

#測試 從訓練好的luis app問取得一句話的intent及entity等資料
prediction_url = 'https://linestocknews-authoring.cognitiveservices.azure.com/luis/v2.0/apps/b8f9254d-0777-46bb-b239-25a08a5f5d55'   # 貼上的你的endpoint url + luis app id
prediction_sentence = "我要訂閱台積電"
prediction_sentence_json = json.dumps(prediction_sentence)
predict_sentence_test(prediction_url, prediction_sentence_json)