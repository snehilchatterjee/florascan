from flask import Flask, jsonify, request, send_from_directory
import sqlite3
from flask_cors import CORS
import base64
import numpy as np
import cv2
import numpy as np
import torch
from transformers import *

device="cuda" if torch.cuda.is_available() else "cpu"


model_name = "google/vit-base-patch16-384"


image_processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(
    model_name,
    num_labels=447,
    ignore_mismatched_sizes=True,
)

best_checkpoint = 24000
model = ViTForImageClassification.from_pretrained(f"./vit_base_384/checkpoint-{best_checkpoint}").to(device)


app = Flask(__name__)
CORS(app)

#loaded_model = tf.keras.models.load_model("epoch_4th")


def get_db_connection():
    conn = sqlite3.connect("after_pruning.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/app/<path:path>")
def serve_static(path):
    return send_from_directory("app", path)


@app.route("/api/plant/<plant_name>", methods=["GET"])
def api_get_plant(plant_name):
    print(plant_name)
    conn = get_db_connection()
    plant = conn.execute(
        "SELECT id, name, common_name, uses FROM plants WHERE name = ?", (plant_name,)
    ).fetchone()
    if plant is None:
        return jsonify({"error": "Plant not found"})
    states = conn.execute(
        "SELECT state FROM states WHERE plant_id = ? GROUP BY state", (plant["id"],)
    ).fetchall()
    return jsonify(
        binomial_name=plant["name"],
        common_name=plant["common_name"],
        uses=plant["uses"],
        states=[state["state"] for state in states],
    )


@app.route("/api/all_plants", methods=["GET"])
def api_all_plants():
    conn = get_db_connection()
    plants = conn.execute("SELECT name, uses FROM plants").fetchall()
    return jsonify(
        plants=[
            {
                "name": plant["name"],
                "uses": plant["uses"],
            }
            for plant in plants
        ]
    )


@app.route("/api/predict/", methods=["POST"])
def api_predict():
    global loaded_model
    im64 = request.json.get("image")
    imb = base64.b64decode(im64)
    im_arr = np.frombuffer(imb, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    #file = img
    #file = cv2.resize(file, (384, 384))
    #file = np.expand_dims(file, axis=0)
    #file=torch.from_numpy(file).to(device)
    image=torch.from_numpy(img).to(device)
    pixel_values = image_processor(image, return_tensors="pt")["pixel_values"].to("cuda")
    logits=model(pixel_values)
    predictions=torch.softmax(logits.logits,dim=1)
    predicted_class_index = torch.argmax(torch.softmax(logits.logits,dim=1),dim=1).item()
    #predictions = loaded_model.predict(file)
    #predictions=
    #predictions = tf.nn.softmax(predictions).numpy()
    
    conn = get_db_connection()
    print(predicted_class_index + 1)
    #print(np.max(predictions, axis=1)[0])
    name = conn.execute(
        "SELECT class FROM model_labels WHERE id=?",
        (int(predicted_class_index) + 1,),
    ).fetchone()
    name = name["class"]
    return jsonify(
        {"prediction": name, "probability": str(torch.argmax(predictions, dim=1).item())}
    )


if __name__ == "__main__":
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=8080)
    # app.run()  # run app
