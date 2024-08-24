import base64
import json
import logging
from datetime import datetime
import time
from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from channels.generic.websocket import AsyncWebsocketConsumer

from GazeTracking.gaze_tracking import GazeTracking

class CameraConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gaze = GazeTracking()
        self.font_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
        self.font_small = ImageFont.truetype("DejaVuSans.ttf", 16)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    # doing this in sync to avoid headache
    async def receive(self, text_data):
        try:
            start_time = time.time()

            data = json.loads(text_data)
            image_data = data['image'].split(',')[1]
            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)

            if nparr.size == 0:
                logging.error("Buffer is empty after base64 decode")
                return

            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                logging.error("Decoded image is null after CV2's imdecode")
                return

            self.gaze.refresh(frame)
            frame = self.gaze.annotated_frame()

            # using PIL for better text-on-image quality, you can drop this and use only CV2 (@PutText) in add_info()
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            pil_image = self.add_info(pil_image)

            buffer = BytesIO()
            pil_image.save(buffer, format="JPEG")
            processed_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            processing_time = time.time() - start_time

            await self.send(text_data=json.dumps({
                'processed_image': 'data:image/jpeg;base64,' + processed_image,
                'processing_time': processing_time
            }))
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
            return

    def add_info(self, pil_image: Image) -> Image:
        draw = ImageDraw.Draw(pil_image)
        color = (25, 25, 112)

        # Main text (gaze direction / blinking)
        if self.gaze.is_blinking():
            main_text = "Моргает"
        elif self.gaze.is_right():
            main_text = "Смотрит вправо"
        elif self.gaze.is_left():
            main_text = "Смотрит влево"
        elif self.gaze.is_center():
            main_text = "Смотрит прямо"
        else:
            main_text = "Неизвестно"

        # Extra info (pupils coords)
        left_pupil = self.gaze.pupil_left_coords()
        right_pupil = self.gaze.pupil_right_coords()

        if left_pupil:
            left_pupil_text = f"Левый зрачок (X:{left_pupil[0]}, Y:{left_pupil[1]})"
        else:
            left_pupil_text = "Левый зрачок не обнаружен"

        if right_pupil:
            right_pupil_text = f"Правый зрачок (X:{right_pupil[0]}, Y:{right_pupil[1]})"
        else:
            right_pupil_text = "Правый зрачок не обнаружен"

        draw.text((10, 10), main_text, font=self.font_large, fill=color)
        draw.text((10, 50), left_pupil_text, font=self.font_small, fill=color)
        draw.text((10, 70), right_pupil_text, font=self.font_small, fill=color)

        return pil_image
