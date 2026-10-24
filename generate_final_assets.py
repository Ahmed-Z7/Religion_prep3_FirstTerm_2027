import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))

def get_font(name, size):
    paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        f"C:/Windows/Fonts/{name.upper()}",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)

def create_styled_qr(url, output_path="qr_code_styled.png"):
    # 1. Create center emblem logo
    logo_size = 140
    logo = Image.new("RGBA", (logo_size, logo_size), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(logo)
    
    # Outer white ring for clearance
    ldraw.ellipse([2, 2, logo_size - 2, logo_size - 2], fill=(255, 255, 255))
    # Inner navy circle with gold border
    ldraw.ellipse([6, 6, logo_size - 6, logo_size - 6], fill=(13, 37, 76), outline=(212, 175, 55), width=5)
    
    # Gold Letter 'ز'
    font_z = get_font("trado.ttf", 80)
    z_txt = ar("ز")
    bbox = ldraw.textbbox((0, 0), z_txt, font=font_z)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    ldraw.text(((logo_size - tw) / 2 - bbox[0], (logo_size - th) / 2 - bbox[1] - 4), z_txt, font=font_z, fill=(245, 208, 100))
    logo.save("temp_logo.png")

    # 2. QR Code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=(10, 25, 47),
            edge_color=(23, 60, 120),
            back_color=(255, 255, 255)
        ),
        embedded_image_path="temp_logo.png"
    )
    img.save(output_path, "PNG", dpi=(300, 300))
    
    # Verify scan with OpenCV
    detector = cv2.QRCodeDetector()
    val, pts, _ = detector.detectAndDecode(cv2.imread(output_path))
    assert val == url, f"Verification failed: {val}"
    print(f"Verified QR successfully: {output_path} -> {val}")
    return output_path

def create_student_flyer(qr_path, output_path="student_qr_card.png"):
    W, H = 1200, 1800
    canvas = Image.new("RGBA", (W, H), (10, 25, 47, 255))
    draw = ImageDraw.Draw(canvas)

    # 1. Luxurious Deep Background Gradient
    for y in range(H):
        ratio = y / H
        # Deep Sapphire #143261 -> Midnight Navy #061122
        r = int(20 * (1 - ratio) + 6 * ratio)
        g = int(50 * (1 - ratio) + 17 * ratio)
        b = int(98 * (1 - ratio) + 34 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Ambient Top Light
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([W//2 - 450, -80, W//2 + 450, 500], fill=(212, 175, 55, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    canvas.paste(glow, (0, 0), glow)

    # 2. Islamic Architectural Double Border
    margin = 32
    draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=32, outline=(212, 175, 55), width=4)
    draw.rounded_rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], radius=24, outline=(245, 208, 100), width=1)

    # Corner Decorative Squares
    for cx, cy in [(margin+18, margin+18), (W-margin-38, margin+18), (margin+18, H-margin-38), (W-margin-38, H-margin-38)]:
        draw.rectangle([cx, cy, cx + 20, cy + 20], fill=(212, 175, 55))

    # Fonts
    font_bismillah = get_font("trado.ttf", 46)
    font_sub_series = get_font("tahomabd.ttf", 26)
    font_title_main = get_font("arialbd.ttf", 64)
    font_title_sub = get_font("arialbd.ttf", 44)
    font_grade = get_font("tahomabd.ttf", 32)
    font_scan_hint = get_font("tahomabd.ttf", 32)
    font_url = get_font("arialbd.ttf", 32)
    font_feature = get_font("tahomabd.ttf", 25)
    font_teacher_title = get_font("tahoma.ttf", 28)
    font_teacher_name = get_font("arialbd.ttf", 52)
    font_phone = get_font("arialbd.ttf", 38)
    font_wish = get_font("tahomabd.ttf", 26)

    def draw_centered(y, text, font, fill, shadow_color=None):
        t_ar = ar(text)
        bbox = draw.textbbox((0, 0), t_ar, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (W - tw) // 2 - bbox[0]
        if shadow_color:
            draw.text((x + 2, y + 2), t_ar, font=font, fill=shadow_color)
        draw.text((x, y), t_ar, font=font, fill=fill)
        return y + th

    # 1. Bismillah
    draw_centered(65, "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", font_bismillah, (254, 240, 138), (0, 0, 0))

    # 2. Golden Ribbon Banner
    ribbon_txt = "السلسلة الذهبية المعتمدة في التربية الإسلامية"
    r_ar = ar(ribbon_txt)
    r_bbox = draw.textbbox((0, 0), r_ar, font=font_sub_series)
    rw = r_bbox[2] - r_bbox[0] + 60
    rh = r_bbox[3] - r_bbox[1] + 20
    rx = (W - rw) // 2
    draw.rounded_rectangle([rx, 140, rx + rw, 140 + rh], radius=20, fill=(180, 130, 20), outline=(254, 240, 138), width=2)
    draw_centered(148, ribbon_txt, font_sub_series, (255, 255, 255))

    # 3. Main Titles
    draw_centered(215, "سلسلة الزَّيْدَان", font_title_main, (245, 208, 100), (0, 0, 0))
    draw_centered(295, "في التَّرْبِيَةِ الإِسْلاَمِيَّةِ التَّفَاعُلِيَّةِ", font_title_sub, (255, 255, 255), (0, 0, 0))

    # 4. Grade Badge (Emerald Green)
    badge_txt = "الصف الثالث الإعدادي — الفصل الدراسي الأول"
    b_ar = ar(badge_txt)
    b_bbox = draw.textbbox((0, 0), b_ar, font=font_grade)
    bw = b_bbox[2] - b_bbox[0] + 60
    bh = b_bbox[3] - b_bbox[1] + 22
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, 375, bx + bw, 375 + bh], radius=18, fill=(5, 120, 85), outline=(167, 243, 208), width=2)
    draw_centered(385, badge_txt, font_grade, (255, 255, 255))

    # 5. QR Code Hero Card (White Background Container)
    box_w, box_h = 740, 750
    box_x = (W - box_w) // 2
    box_y = 460

    # White box with shadow & gold border
    draw.rounded_rectangle([box_x + 5, box_y + 8, box_x + box_w + 5, box_y + box_h + 8], radius=32, fill=(0, 0, 0, 140))
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=32, fill=(255, 255, 255), outline=(212, 175, 55), width=6)

    # Paste QR Code
    qr_img = Image.open(qr_path).convert("RGBA")
    qr_display_size = 530
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    canvas.paste(qr_resized, (box_x + (box_w - qr_display_size) // 2, box_y + 30), qr_resized)

    # Instruction under QR
    t_hint = ar("امسح الكود بكاميرا الهاتف لفتح الملزمة فوراً")
    h_bbox = draw.textbbox((0, 0), t_hint, font=font_scan_hint)
    hw = h_bbox[2] - h_bbox[0]
    draw.text(((W - hw) // 2 - h_bbox[0], box_y + 580), t_hint, font=font_scan_hint, fill=(13, 37, 76))

    # URL Button Pill
    url_text = "https://religon-prep3.vercel.app/"
    u_bbox = draw.textbbox((0, 0), url_text, font=font_url)
    uw = u_bbox[2] - u_bbox[0] + 44
    uh = u_bbox[3] - u_bbox[1] + 18
    ux = (W - uw) // 2
    draw.rounded_rectangle([ux, box_y + 640, ux + uw, box_y + 640 + uh], radius=16, fill=(15, 23, 42), outline=(56, 189, 248), width=2)
    draw.text(((W - (u_bbox[2] - u_bbox[0])) // 2 - u_bbox[0], box_y + 648), url_text, font=font_url, fill=(125, 211, 252))

    # 6. Features Grid (Solid High Contrast Pills)
    features_r1 = [
        "ملخص شامل ومركّز لكل فروع المنهج تفصيلياً",
        "حل جميع تدريبات وأسئلة كتاب الوزارة بالكامل",
    ]
    features_r2 = [
        "بنك أسئلة شامل ونماذج امتحانات متوقعة",
        "اختبارات تفاعلية ذاتية والوضع الليلي وطباعة",
    ]

    def draw_feature_pills(items, y_pos):
        total_w = 0
        boxes = []
        for it in items:
            it_ar = ar(it)
            ibox = draw.textbbox((0, 0), it_ar, font=font_feature)
            iw = ibox[2] - ibox[0] + 40
            ih = ibox[3] - ibox[1] + 20
            boxes.append((it_ar, iw, ih, ibox))
            total_w += iw + 18
        total_w -= 18
        cur_x = (W - total_w) // 2
        for it_ar, iw, ih, ibox in boxes:
            draw.rounded_rectangle([cur_x, y_pos, cur_x + iw, y_pos + ih], radius=14, fill=(16, 38, 76), outline=(212, 175, 55), width=2)
            draw.text((cur_x + 20 - ibox[0], y_pos + 10 - ibox[1]), it_ar, font=font_feature, fill=(255, 255, 255))
            cur_x += iw + 18

    draw_feature_pills(features_r1, 1245)
    draw_feature_pills(features_r2, 1310)

    # 7. Separator Line
    draw.line([(100, 1385), (W - 100, 1385)], fill=(212, 175, 55), width=2)

    # 8. Teacher Footer Section
    draw_centered(1405, "إعداد وإشراف خبير المادة:", font_teacher_title, (203, 213, 225))
    draw_centered(1448, "مستر / عَلِي زَيْدَان", font_teacher_name, (245, 208, 100), (0, 0, 0))
    draw_centered(1525, "مدرس خبير اللغة العربية والتربية الإسلامية بمرحلة التعليم الإعدادي والثانوي", font_teacher_title, (226, 232, 240))

    # Phone Contact Badge (Emerald Green Solid)
    phone_str = "للحجز والاستفسار وطلب الملازم: 01000936273"
    ph_ar = ar(phone_str)
    ph_bbox = draw.textbbox((0, 0), ph_ar, font=font_phone)
    ph_w = ph_bbox[2] - ph_bbox[0] + 60
    ph_h = ph_bbox[3] - ph_bbox[1] + 26
    ph_x = (W - ph_w) // 2
    draw.rounded_rectangle([ph_x, 1585, ph_x + ph_w, 1585 + ph_h], radius=24, fill=(5, 120, 85), outline=(167, 243, 208), width=2)
    draw_centered(1596, phone_str, font_phone, (255, 255, 255))

    # Final Encouraging Wish
    draw_centered(1705, "مع أطيب تمنياتنا لجميع أبنائنا وبناتنا الطلاب بالتفوق والدرجات النهائية", font_wish, (254, 240, 138))

    canvas = canvas.convert("RGB")
    canvas.save(output_path, "PNG", dpi=(300, 300))
    print(f"Created student flyer successfully: {output_path} ({W}x{H})")

if __name__ == "__main__":
    qr_p = create_styled_qr("https://religon-prep3.vercel.app/", "qr_code_styled.png")
    create_student_flyer(qr_p, "student_qr_card.png")
