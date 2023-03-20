import gradio as gr
import openai


def get_ans(user_content, chat_data_, chat_log_, api_key):
    chat_data_.append({"role": "user", "content": user_content})
    res_ = request_ans(api_key, chat_data_)
    res = res_.choices[0].message.content
    while res.startswith("\n") != res.startswith("？"):
        res = res[1:]
    chat_data_.append({"role": 'assistant', "content": res})

    chat_log_.append([user_content, res])

    return chat_log_, chat_log_, "", chat_data_


def request_ans(api_key, msg):
    # openai.proxy = {'http': "http://127.0.0.1:8001", 'https': 'http://127.0.0.1:8001'}
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=msg,
        temperature=0.2
    )

    return response


def config(api_key, company, job):
    prompt = f"你是一名熟悉{company}的面试官。用户将成为候选人，您将向用户询问{job}职位的面试问题。希望你只作为面试官回答。不要一次写出所有的问题。希望你只对用户进行面试。问用户问题，等待用户的回答。不要写解释。你需要像面试官一样一个一个问题问用户，等用户回答。 若用户回答不上某个问题，那就继续问下一个问题 "
    content = [{"role": "system", "content": prompt}, {"role": "user", "content": "面试官你好"}]

    res_ = request_ans(api_key, content)
    res = res_.choices[0].message.content
    while res.startswith("\n") != res.startswith("？"):
        res = res[1:]

    history = [["面试官您好！", res]]

    return history, history, api_key, content


with gr.Blocks(title="AI面试官") as block:
    chat_log = gr.State()
    key = gr.State()
    chat_data = gr.State()

    gr.Markdown("""<h1><center>AI面试官</center></h1>""")
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot()
            message = gr.Textbox(label="你的回答")

            message.submit(
                fn=get_ans,
                inputs=[
                    message,
                    chat_data,
                    chat_log,
                    key
                ],
                outputs=[chatbot, chat_log, message, chat_data]
            )

            submit = gr.Button("发送")
            submit.click(
                get_ans,
                inputs=[
                    message,
                    chat_data,
                    chat_log,
                    key
                ],
                outputs=[chatbot, chat_log, message, chat_data],
            )

        with gr.Column():
            # temperature = gr.Slider(label="Temperature", minimum=0, maximum=1, step=0.1, value=0.9)
            # max_tokens = gr.Slider(label="Max Tokens", minimum=10, maximum=400, step=10, value=150)
            # top_p = gr.Slider(label="Top P", minimum=0, maximum=1, step=0.1, value=1)
            # frequency_penalty = gr.Slider(
            #     label="Frequency Penalty",
            #     minimum=0,
            #     maximum=1,
            #     step=0.1,
            #     value=0,
            # )
            # presence_penalty = gr.Slider(
            #     label="Presence Penalty",
            #     minimum=0,
            #     maximum=1,
            #     step=0.1,
            #     value=0.6,
            # )

            openai_token = gr.Textbox(label="OpenAI API Key")
            company = gr.Textbox(label="你面试的公司")
            job = gr.Textbox(label="你面试的岗位")

            start = gr.Button("开始面试")
            start.click(
                config,
                inputs=[
                    openai_token,
                    company,
                    job
                ],
                outputs=[chatbot, chat_log, key, chat_data]
            )

if __name__ == "__main__":
    block.launch()
