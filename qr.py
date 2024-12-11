import qrcode
from PIL import Image

def generate_colored_qr(data, host_image_path, output_path, box_size=10):
    try:
        host_image = Image.open(host_image_path).convert("RGB")
    except IOError:
        print("Unable to load host image. Please check the file path.")
        return

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=0
    )
    qr.add_data(data)
    qr.make()
    qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    host_image = host_image.resize(qr_image.size, Image.Resampling.LANCZOS)

    size = qr_image.size[0]
    module_count = qr.modules_count
    module_size = size // module_count

    finder_size = 7 * module_size
    alignment_size = 5 * module_size
    finder_positions = [
        (0, 0),
        (0, size - finder_size),
        (size - finder_size, 0),
    ]
    alignment_position = (
        size - alignment_size - 4*module_size, 
        size - alignment_size - 4*module_size
    )

    def is_in_region(x, y, regions):
        for top_x, top_y, region_size in regions:
            if top_x <= x < top_x + region_size and top_y <= y < top_y + region_size:
                return True
        return False

    ignore_regions = [(x, y, finder_size) for x, y in finder_positions]
    ignore_regions.append((alignment_position[0], alignment_position[1], alignment_size))

    pixels_qr = qr_image.load()
    pixels_host = host_image.load()

    for y in range(qr_image.size[1]):
        for x in range(qr_image.size[0]):
            if is_in_region(x, y, ignore_regions):
                continue
            r, g, b = pixels_host[x, y]
            if pixels_qr[x, y] == (0, 0, 0):
                if r >= g and r >= b:
                    qr_image.putpixel((x, y), (int(r * 1.05), g, b))
                elif g >= r and g >= b:
                    qr_image.putpixel((x, y), (r, int(g * 1.05), b))
                else:
                    qr_image.putpixel((x, y), (r, g, int(b * 1.05)))
            else:
                qr_image.putpixel((x, y), (int(r + 120), int(g + 120), int(b + 120)))

    try:
        qr_image.save(output_path)
        print(f"Customized QR code without padding saved to {output_path}")
    except IOError:
        print(f"Unable to save the output file to {output_path}. Please check the file path and permissions.")

data = "Good afternoon Vishnu Negi"
host_image_path = "/content/king Kohli.jpg"
output_path = "Final.png"
generate_colored_qr(data, host_image_path, output_path)