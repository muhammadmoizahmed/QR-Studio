import qrcode
from PIL import Image
import os

def generate_qr_with_logo(qr_type, data, logo_path=None, output_filename="qr_code.png", version=7, box_size=25, border=10, logo_proportion=3, border_size=60, fill_color="black", back_color="white", logo_position="center", error_correction=qrcode.constants.ERROR_CORRECT_H):
    """
    Generate QR code with logo and black border
    
    Args:
        qr_type (str): Type of QR code
        data (dict): Data for QR code
        logo_path (str): Path to logo image
        output_filename (str): Output filename
        version (int): QR code version
        box_size (int): Box size for QR modules
        border (int): Border width
        logo_proportion (int): Logo size as fraction of QR size
        border_size (int): Thickness of black border
        fill_color (str): QR code color
        back_color (str): Background color
        logo_position (str): Position of logo
        error_correction: Error correction level
    """
    # Create QR code
    qr = qrcode.QRCode(
        version=version,
        box_size=box_size,
        border=border,
        error_correction=error_correction
    )

    # Generate QR data based on type
    qr_data = ""
    if qr_type == 'url':
        qr_data = data.get('url', '')
    elif qr_type == 'text':
        qr_data = data.get('text', '')
    elif qr_type == 'email':
        qr_data = f"mailto:{data.get('email', '')}?subject={data.get('subject', '')}&body={data.get('body', '')}"
    elif qr_type == 'phone':
        qr_data = f"tel:{data.get('phone', '')}"
    elif qr_type == 'sms':
        qr_data = f"smsto:{data.get('phone', '')}:{data.get('message', '')}"
    elif qr_type == 'wifi':
        qr_data = f"WIFI:T:{data.get('encryption', 'WPA')};S:{data.get('ssid', '')};P:{data.get('password', '')};;"
    elif qr_type == 'vcard':
        # vCard format for contact
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{data.get('name', '')}
TEL:{data.get('phone', '')}
EMAIL:{data.get('email', '')}
ORG:{data.get('organization', '')}
TITLE:{data.get('title', '')}
END:VCARD"""
        qr_data = vcard
    elif qr_type == 'whatsapp':
        qr_data = f"https://wa.me/{data.get('phone', '').replace('+', '')}?text={data.get('message', '')}"
    
    if not qr_data:
        raise ValueError("Invalid QR type or missing data")
    
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        # Resize logo
        logo_size = qr_img.size[0] // logo_proportion
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Create white circle background with border
        bg_size = logo_size + 20
        bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))
        bg.paste(logo, (10, 10), logo)

        # Position center
        pos = (
            (qr_img.size[0] - bg_size) // 2,
            (qr_img.size[1] - bg_size) // 2
        )

        # Paste with mask
        qr_img.paste(bg, pos, bg)

    # Add black border if border_size > 0
    if border_size > 0:
        final_img = Image.new("RGB", 
                             (qr_img.size[0] + border_size*2, qr_img.size[1] + border_size*2), 
                             (0, 0, 0))
        final_img.paste(qr_img, (border_size, border_size), qr_img)
    else:
        final_img = qr_img.convert("RGB")

    # Save
    final_img.save(output_filename)
    return f"QR code saved as {output_filename}"

# Example usage (for testing)
if __name__ == "__main__":
    result = generate_qr_with_logo(
        qr_type='url',
        data={'url': 'https://example.com'},
        logo_path="../logo.png",
        output_filename="qr_code.png"
    )
    print(result)