import base64
import time

import PIL.Image
import google.generativeai as genai

from autotrader.autotrader.config.env_config import EnvConfig


class RetrieveRegNumberPipeline:
    def process_item(self, item, spider):
        for img_path in item['image_paths']:
            license_num = self.get_license_num_from_base64_image(img_path)
            # license_num = self.get_license_num_pil_image(img_path)
            if not license_num:
                # print("Could not Extract License Plate.")
                continue
            print(f"License Number: {license_num}")

            # if item['plate'] and item['plate'] not in license_num:
            #     print(f"Plate# {item['plate']} Not Matched with License Number")
            #     continue

            reg_no = item['registration_hidden'].lower()
            if reg_no and license_num.lower().startswith(reg_no[0]) or license_num.lower().endswith(reg_no[-1]):
                item['license_number'] = license_num
                break
            else:
                item['license_number'] = "License Plate Not Visible"
                print(f"Registration Hidden: {item['registration_hidden']} Not Matched with License Number")

            time.sleep(3)

        return item

    def get_license_num_from_base64_image(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                img_data = image_file.read()
            img_base64 = base64.b64encode(img_data).decode("utf-8")

            img_part = {"mime_type": "image/jpeg", "data": img_base64}
            prompt = "What is the license plate number on the car in this image? Provide only the plate number."

            model = self.get_genai_model()
            response = model.generate_content([prompt, img_part])

            return (response.text or '').strip()

        except FileNotFoundError:
            print(f"Error: Image not found at {image_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_genai_model(self):
        genai.configure(api_key=EnvConfig.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        # model = genai.GenerativeModel('gemini-2.0-flash-latest')
        return model

    def get_license_num_pil_image(self, image_path):
        image = PIL.Image.open(image_path)

        genai.configure(api_key=EnvConfig.GEMINI_API_KEY)
        prompt = "What is the license plate number on the car in this image? Provide only the plate number."

        model = self.get_genai_model()
        response = model.generate_content(contents=[prompt, image])
        return (response.text or '').strip()

    def display_models(self):
        for m in genai.list_models():
            print(m.name, m.supported_generation_methods)
