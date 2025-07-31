# Before running, make sure you have the Azure AI Text Analytics library installed:
# pip install azure-ai-textanalytics==5.3.0

import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def extract_chinese_key_phrases(text_to_analyze):
    """
    Analyzes a Chinese text string and extracts key phrases using Azure Text Analytics.

    Args:
        text_to_analyze (str): The Chinese text to be analyzed.

    Returns:
        list: A list of the extracted key phrases. Returns an empty list if an error occurs.
    """
    try:
        # It's recommended to store your key and endpoint as environment variables
        # for better security, rather than hardcoding them in the script.
        endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
        key = os.environ["AZURE_LANGUAGE_KEY"]
    except KeyError:
        print("ERROR: Please set the AZURE_LANGUAGE_ENDPOINT and AZURE_LANGUAGE_KEY environment variables.")
        return []

    # Authenticate the client with your key and endpoint
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    documents = [
        {"id": "1", "language": "zh-hans", "text": text_to_analyze}
    ]

    try:
        # Call the API to extract key phrases
        response = text_analytics_client.extract_key_phrases(documents=documents)
        
        extracted_phrases = []
        for doc in response:
            if not doc.is_error:
                print(f"Extracted key phrases from document id {doc.id}:")
                for phrase in doc.key_phrases:
                    print(f" - {phrase}")
                    extracted_phrases.append(phrase)
            else:
                print(f"Error processing document id {doc.id}: {doc.error.message}")
        
        return extracted_phrases

    except Exception as err:
        print(f"An error occurred: {err}")
        return []


# Sample Chinese sentence. 
# Translation: "The weather in Beijing is very good today, suitable for traveling."
chinese_sentence = """红色联合”对“四．二八兵团”总部大楼的攻击已持续了两天，他们的旗帜在大楼周围躁动地飘扬着，仿佛渴望干柴的火种。
“红色联合”的指挥官心急如焚，他并不惧怕大楼的守卫者，那二百多名“四．二八”战士，与诞生于l966年初、经历过大检阅和大串联的“红色联合”相比要稚嫩许多。他怕的是大楼中那十几个大铁炉子，里面塞满了烈性炸药，用电雷管串联起来，他看不到它们，但能感觉到它们磁石般的存在，开关一合，玉石俱焚，而“四．二八”的那些小红卫兵们是有这个精神力量的。比起已经在风雨中成熟了许多的第一代红卫兵，新生的造反派们像火炭上的狼群，除了疯狂还是疯狂。
大楼顶上出现了一个娇小的身影，那个美丽的女孩子挥动着一面“四．二八”的大旗，她的出现立刻招来了一阵杂乱的枪声，射击的武器五花八门，有陈旧的美式卡宾枪[…]”
"""

print(f"Analyzing sentence: '{chinese_sentence}'")

# To run this example, you first need to set your Azure credentials.
# See the setup instructions below the code.
# Example of setting environment variables in your terminal (replace with your actual values):
# export AZURE_LANGUAGE_ENDPOINT="https://your-resource-name.cognitiveservices.azure.com/"
# export AZURE_LANGUAGE_KEY="your-secret-api-key"

key_phrases = extract_chinese_key_phrases(chinese_sentence)

if key_phrases:
    print("\n--- Summary of Extracted Phrases ---")
    for i, phrase in enumerate(key_phrases, 1):
        print(f"{i}. {phrase}")
else:
    print("No key phrases were extracted or an error occurred.")

