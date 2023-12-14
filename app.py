import timm
import torch
import warnings
import gradio as gr
import cv2

device="cuda" if torch.cuda.is_available() else "cpu"
warnings.filterwarnings("ignore")

model_name="vit_base_patch8_224.augreg_in21k_ft_in1k"
model=timm.create_model(model_name)
model.head=torch.nn.Linear(in_features=model.head.in_features,out_features=2)
state_dict=torch.load("models/vit_base_patch8_224.augreg_in21k_feature_extractor/checkpoint-5.pth")
model.load_state_dict(state_dict)

def flip_text(x):
    return x[::-1]


def model_inf(x):
    im=torch.tensor(cv2.resize(x,(224,224)))
    im=torch.from_numpy(cv2.resize(x,(224,224))).type(torch.float32)
    im=im.permute(2,0,1)
    im=im.unsqueeze(dim=0)
    result=torch.argmax(torch.softmax(model(im),dim=1),dim=1)
    print(result)
    if(result):
        return "Pneumonia"
    else:
        return "Normal"



with gr.Blocks() as app:
    gr.Markdown("Pneumonia Classifier")
    with gr.Tab("Classification by image"):
        with gr.Row():
            gr.Interface(fn=model_inf, inputs="image", outputs="text",allow_flagging="never")
    with gr.Tab("Classification by audio"):
        gr.Interface(fn=flip_text, inputs="audio", outputs="text",allow_flagging="never")



app.launch(share=True)
