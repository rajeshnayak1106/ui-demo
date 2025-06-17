import gradio as gr


def greet(name, temperature):
    greeting = f"Hello, {name}!" if name else "Hello!"
    return f"{greeting} Current temperature is {temperature}°C"

with gr.Blocks() as demo:
    gr.Markdown("## Gradio Feature Demo")
    gr.Markdown("Enter your name and select a temperature to see Gradio in action.")
    with gr.Row():
        name_input = gr.Textbox(label="Name", placeholder="Data Scientist")
        temp_slider = gr.Slider(minimum=-10, maximum=40, value=20, label="Temperature")
    greet_btn = gr.Button("Greet")
    output = gr.Textbox(label="Greeting")

    greet_btn.click(fn=greet, inputs=[name_input, temp_slider], outputs=output)

if __name__ == "__main__":
    demo.launch(server_port=8001,inbrowser=True)
