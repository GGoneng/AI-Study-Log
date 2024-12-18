from PIL import ImageDraw, Image

input_path = r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\기업 프로젝트\MyWEB\static\image\green_circle.png'
output_path = r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\기업 프로젝트\MyWEB\static\image\yellow_circle.png'

# Reload the image in case something went wrong in the previous step
image = Image.open(input_path).convert("RGBA")

# Create a blank image for output with a transparent background
output_image = Image.new("RGBA", image.size, (255, 255, 255, 0))

# Draw the outline in light gray
draw = ImageDraw.Draw(output_image)
for y in range(image.height):
    for x in range(image.width):
        # If the pixel is black (outline), change it to light gray
        if image.getpixel((x, y))[3] > 0:  # Check alpha channel for non-transparent pixels
            draw.point((x, y), fill=(255, 223, 9, 255))  # Light gray

# Save the updated image
output_image.save(output_path)
output_path
