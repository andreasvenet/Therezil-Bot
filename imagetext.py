from urllib.request import urlopen, Request
import numpy as np
import cv2
import bot_sync
import random

"""
Imagetext command

Usage:
imagetext <text>, <img_link>
"""
class Imagetext():
    msg_error_action_too_fast = "Μην βιάζεσαι μαγκάρα."
    msg_error_action_invalid = "Πες τι να γράψω κουφάλα και δώσε μου κανά link για εικόνα."
    msg_error_action_invalid_image = "Δώσε μου μία κανονική εικόνα σε link (jpg, png, gif...)"

    supported_image_extensions = ['.jpg', '.png', '.jpeg']

    def __init__(self, name):
        self.name = name
        pass

    def get_image(self, img_url):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }
        req = Request(url=img_url, headers=headers)
        with urlopen(req) as response:
            return response.read()

    def attach_text_to_image(self, text, image_link):
        if not image_link:
            return False

        image = self.get_image(image_link)
        image_bytearray = np.asarray(bytearray(image), dtype="uint8")
        img = cv2.imdecode(image_bytearray, cv2.COLOR_BGR2RGB)

        h, w, c = img.shape

        # Max resolution for custom images (Alter carefully, this is to avoid costs!)
        max_width = 1024
        max_height = 768

        # Max resolution used for scaling
        max_scaling_width = max_width / 2 + 140

        # Image text scaling settings
        font_size_small_min = 0.7
        font_size_small_max = 0.9
        font_size_normal_min = 0.9
        font_size_normal_max = 1.0

        # Sets the image within the maximum allowed size
        if max_height < h or max_width < w:
            scaling_factor = max_height / float(h)

            if max_width / float(w) < scaling_factor:
                scaling_factor = max_width / float(w)

            # resize image
            img = cv2.resize(img,
                             None,
                             fx=scaling_factor,
                             fy=scaling_factor,
                             interpolation=cv2.INTER_AREA)

        # Font
        font = cv2.FONT_HERSHEY_SIMPLEX
        offset = int(h / len(text)) + random.randint(10, 20)
        offset_w = int(w / len(text)) + random.randint(10, 20)

        # Font scale
        font_scale = min(w, h) / max_scaling_width
        if font_scale < font_size_small_min:
            font_scale = random.uniform(font_size_small_min,
                                        font_size_small_max)
        elif font_scale > font_size_normal_max:
            font_scale = random.uniform(font_size_normal_min,
                                        font_size_normal_max)

        # Color randomisation
        color_min_value = 100
        color_max_value = 255

        random_color_r = random.randint(color_min_value, color_max_value)
        random_color_g = random.randint(color_min_value, color_max_value)
        random_color_b = random.randint(color_min_value, color_max_value)

        # Place text with a random color
        cv2.putText(img, text, (offset_w, offset), font, font_scale,
                    (random_color_r, random_color_g, random_color_b), 0,
                    cv2.LINE_AA)

        # Write the image and send it
        img_written = cv2.imwrite("temp.png", img)
        if (img_written):
            discord_image = self.discord.File(r'./temp.png')
            return discord_image
        else:
            return False

    async def command(self, message, discord):
        self.discord = discord
        has_image = message.content.split(self.name + " ", 1)
        command_str = ""
        split_text_and_image = ""
        text_and_image = command_str.join(has_image).split(self.name + " ", 1)
        text_and_image_arr = split_text_and_image.join(text_and_image).split(
            ",", 2)

        if (bot_sync.is_action_too_soon()):
            await message.channel.send(self.msg_error_action_too_fast)
        else:
            bot_sync.update_last_action()

            if (len(has_image) == 1 or len(text_and_image_arr) < 2):
                await message.channel.send(self.msg_error_action_invalid)

            else:
                if (text_and_image_arr[1].startswith(" ")):
                    text_and_image_arr[1] = text_and_image_arr[1].lstrip()

                for ext in self.supported_image_extensions:
                    discord_attachment = self.attach_text_to_image(
                        text_and_image_arr[0], text_and_image_arr[1])

                if (discord_attachment):
                    await message.channel.send(file=discord_attachment)
                else:
                    await message.channel.send(
                        self.msg_error_action_invalid_image)
