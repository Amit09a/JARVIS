from huggingface_hub import InferenceClient

HF_TOKEN = "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"
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)  # Chat-capable model

def chatBot(query):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant named jarvis."},
            {"role": "user", "content": query}
        ]

        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )

        reply = response.choices[0].message["content"]
        print("[BOT]:", reply)
        return reply

    except Exception as e:
        import traceback
        print("❌ Error in chatBot():")
        traceback.print_exc()
        return "Sorry, I couldn't process that."