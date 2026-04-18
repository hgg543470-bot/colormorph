import flet as ft
import os
import base64
from io import BytesIO
from PIL import Image

def main(page: ft.Page):
    page.title = "Jeni's Magic Studio"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.window_width = 400

    # Поля путей
    in_dir = ft.TextField(label="Папка-источник", value="/sdcard/Pictures/clining")
    out_dir = ft.TextField(label="Папка-результат", value="/sdcard/Pictures/cleand")
    
    # Настройки
    threshold = ft.Slider(min=0, max=100, label="Порог: {value}%", value=20)
    color_hex = ft.TextField(label="Цвет (HEX)", value="#FFFFFF", hint_text="#FF0000")
    
    # Окошко превью
    preview_img = ft.Image(src_base64="", width=300, height=300, fit=ft.ImageFit.CONTAIN, visible=False)
    preview_label = ft.Text("Предпросмотр первого файла:", visible=False)

    def get_preview(e):
        try:
            files = [f for f in os.listdir(in_dir.value) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                return
            
            sample_path = os.path.join(in_dir.value, files[0])
            hex_val = color_hex.value.lstrip('#')
            rgb = tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
            thresh_val = (threshold.value / 100) * 255

            with Image.open(sample_path).convert("RGBA") as img:
                datas = img.getdata()
                new_data = []
                for item in datas:
                    brightness = (item[0] + item[1] + item[2]) // 3
                    if brightness > thresh_val:
                        new_data.append((rgb[0], rgb[1], rgb[2], item[3]))
                    else:
                        new_data.append((0, 0, 0, 0))
                
                img.putdata(new_data)
                
                # Конвертируем в base64 для отображения во Flet
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                preview_img.src_base64 = img_str
                preview_img.visible = True
                preview_label.visible = True
                page.update()
        except Exception as ex:
            print(f"Ошибка превью: {ex}")

    def run_full(e):
        # Тут остается твоя логика полной обработки всех файлов
        # (Просто вызываем ту же функцию обработки, что была раньше)
        pass

    page.add(
        ft.Text("Мастерская Джени", size=30, weight="bold", color="cyan"),
        in_dir,
        out_dir,
        ft.Divider(),
        ft.Row([color_hex, ft.IconButton(icon=ft.icons.REFRESH, on_click=get_preview)]),
        ft.Text("Порог фона:"),
        threshold,
        ft.Column([preview_label, preview_img], horizontal_alignment="center"),
        ft.ElevatedButton("Обработать всё", on_click=run_full, width=400, bgcolor="blue", color="white"),
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)

