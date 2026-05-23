import os
import torch
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from wtforms import FileField, SubmitField, FloatField
from wtforms.validators import InputRequired

from PIL import Image
from torchvision import transforms

# =========================
# YOUR MODEL IMPORTS
# =========================
from utils.models import VGGEncoder, Decoder
from utils.utils import adaIN


# =========================
# FLASK APP CONFIG
# =========================
app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecretkey"

app.config["UPLOAD_FOLDER"] = "static/uploads"

app.config["ALLOWED_EXTENSIONS"] = {
    "png",
    "jpg",
    "jpeg"
}

Bootstrap(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# =========================
# FORM
# =========================
class UploadForm(FlaskForm):

    content = FileField(
        "Content Image",
        validators=[InputRequired()]
    )

    style = FileField(
        "Style Image",
        validators=[InputRequired()]
    )

    alpha = FloatField(
        "Alpha",
        default=1.0
    )

    submit = SubmitField("Transfer Style")


# =========================
# DEVICE
# =========================
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Loading models...")


# =========================
# LOAD MODELS
# =========================
encoder = VGGEncoder("vgg_normalised.pth").to(device)

decoder = Decoder().to(device)

decoder.load_state_dict(
    torch.load(
        "experiments/experiment1/decoder_epoch_2.pth",
        map_location=device
    )
)

encoder.eval()
decoder.eval()

print("Models loaded successfully!")


# =========================
# CHECK FILE EXTENSION
# =========================
def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_EXTENSIONS"]
    )


# =========================
# IMAGE TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor()
])


# =========================
# SAVE IMAGE
# =========================
def save_image(tensor, path):

    image = tensor.cpu().clone()

    image = image.squeeze(0)

    image = image.clamp(0, 1)

    image = transforms.ToPILImage()(image)

    image.save(path)


# =========================
# STYLE TRANSFER
# =========================
def style_transfer(
    content_image,
    style_image,
    alpha=1.0
):

    content = transform(content_image).unsqueeze(0).to(device)

    style = transform(style_image).unsqueeze(0).to(device)

    with torch.no_grad():

        content_features = encoder(
            content,
            is_test=True
        )

        style_features = encoder(
            style,
            is_test=True
        )

        t = adaIN(
            content_features,
            style_features
        )

        t = alpha * t + (1 - alpha) * content_features

        output = decoder(t)

    return output


# =========================
# MAIN ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def index():

    form = UploadForm()

    result_image = None

    content_image = None

    style_image = None

    error = None

    if request.method == "POST":

        try:

            # =========================
            # GET FILES
            # =========================
            content_file = request.files.get("content")

            style_file = request.files.get("style")

            alpha = float(request.form.get("alpha", 1.0))

            # =========================
            # VALIDATION
            # =========================
            if not content_file or not style_file:

                error = "Please upload both images."

                return render_template(
                    "index.html",
                    form=form,
                    error=error
                )

            if (
                not allowed_file(content_file.filename)
                or
                not allowed_file(style_file.filename)
            ):

                error = "Invalid file format."

                return render_template(
                    "index.html",
                    form=form,
                    error=error
                )

            # =========================
            # SAVE INPUT FILES
            # =========================
            content_filename = secure_filename(
                content_file.filename
            )

            style_filename = secure_filename(
                style_file.filename
            )

            content_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                content_filename
            )

            style_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                style_filename
            )

            content_file.save(content_path)

            style_file.save(style_path)

            # =========================
            # LOAD IMAGES
            # =========================
            content_pil = Image.open(
                content_path
            ).convert("RGB")

            style_pil = Image.open(
                style_path
            ).convert("RGB")

            # =========================
            # RUN MODEL
            # =========================
            output = style_transfer(
                content_pil,
                style_pil,
                alpha
            )

            # =========================
            # SAVE OUTPUT
            # =========================
            result_filename = (
                "stylized_" + content_filename
            )

            result_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                result_filename
            )

            save_image(output, result_path)

            result_image = result_filename

            content_image = content_filename

            style_image = style_filename

        except Exception as e:

            error = str(e)

    return render_template(
        "index.html",
        form=form,
        result_image=result_image,
        content_image=content_image,
        style_image=style_image,
        error=error
    )


# =========================
# SERVE UPLOADS
# =========================
@app.route("/uploads/<filename>")
def send_image(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================
# SERVE EXAMPLES
# =========================
@app.route("/examples/<path:filename>")
def send_example(filename):

    return send_from_directory(
        "examples",
        filename
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )