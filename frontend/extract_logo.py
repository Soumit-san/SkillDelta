import sys
from PIL import Image

def extract_logo_mark():
    in_path = r"C:\Users\KIIT0001\.gemini\antigravity\brain\c07371c2-c0d1-478d-bda1-d0f25922d5cc\media__1772818088339.jpg"
    out_path = r"C:\Users\KIIT0001\SkillDelta-main\frontend\src\assets\logo.png"

    img = Image.open(in_path).convert("RGBA")
    
    width, height = img.size
    
    min_x, min_y = width, height
    max_x, max_y = 0, 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            
            # check if pixel is colorful
            color_diff = max(r, g, b) - min(r, g, b)
            if color_diff > 40: # threshold for colorfulness
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                
    if max_x < min_x:
        print("Could not find colored logo mark.")
        return
        
    pad = 5
    crop_box = (
        max(0, min_x - pad),
        max(0, min_y - pad),
        min(width, max_x + pad),
        min(height, max_y + pad)
    )
    
    logo_img = img.crop(crop_box)
    
    # Make background transparent
    new_data = []
    for r, g, b, a in logo_img.getdata():
        if r > 240 and g > 240 and b > 240:
            new_data.append((255, 255, 255, 0))
        else:
            # Better anti-aliasing approximation for white background
            # If a pixel is somewhat white, reduce its alpha so it blends into the new dark background
            brightness = (r + g + b) / 3.0
            if brightness > 150:
                # White-ish edge pixel. Calculate alpha
                alpha = int(255 - ((brightness - 150) / 105.0) * 255)
                # Guess the original color before it mixed with white
                if alpha > 0:
                    r_orig = min(255, int((r - 255 * (1 - alpha/255.0)) / (alpha/255.0)))
                    g_orig = min(255, int((g - 255 * (1 - alpha/255.0)) / (alpha/255.0)))
                    b_orig = min(255, int((b - 255 * (1 - alpha/255.0)) / (alpha/255.0)))
                    new_data.append((max(0, r_orig), max(0, g_orig), max(0, b_orig), alpha))
                else:
                    new_data.append((255, 255, 255, 0))
            else:
                new_data.append((r, g, b, 255))
            
    logo_img.putdata(new_data)
    logo_img.save(out_path, "PNG")
    print("Logo extracted and saved to", out_path)

extract_logo_mark()
