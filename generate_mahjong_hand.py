import random
from PIL import Image, ImageDraw, ImageFont

# 麻雀牌のUnicode文字
# 萬子(マンズ): 🀇-🀏, 筒子(ピンズ): 🀙-🀡, 索子(ソーズ): 🀐-🀘, 字牌(ジハイ): 🀀-🀆, 三元牌(サンゲンパイ): 🀄︎🀅🀄︎
MANZU = [chr(i) for i in range(0x1F007, 0x1F010)]
PINZU = [chr(i) for i in range(0x1F019, 0x1F022)]
SOUZU = [chr(i) for i in range(0x1F010, 0x1F019)]
JIHAI = [chr(i) for i in range(0x1F000, 0x1F007)]
SANGEN = [chr(0x1F004), chr(0x1F005), chr(0x1F006)]

# 全ての牌
ALL_TILES = MANZU + PINZU + SOUZU + JIHAI + SANGEN

def generate_hand():
    """ランダムな14牌の配牌を生成する"""
    return sorted([random.choice(ALL_TILES) for _ in range(14)])

def create_image(hand):
    """配牌の文字列から画像を生成する"""
    text = "".join(hand)
    # フォントはGoogle Noto Fontsなど、麻雀牌に対応したものを指定するのが望ましい
    # ここでは一般的なフォントを探す
    font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
    try:
        font = ImageFont.truetype(font_path, 60)
    except IOError:
        # フォントが見つからない場合の代替
        try:
            font = ImageFont.truetype("Arial.ttf", 60)
        except IOError:
            font = ImageFont.load_default()

    # テキストの描画サイズを計算
    # Pillow 10.0.0以降では getbbox を使用
    try:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # 古いPillowでは getsize を使用
        text_width, text_height = font.getsize(text)


    # 画像サイズを決定
    padding = 20
    img_width = text_width + padding * 2
    img_height = text_height + padding * 2

    # 画像を作成
    image = Image.new("RGB", (img_width, img_height), "black")
    draw = ImageDraw.Draw(image)

    # テキストを描画
    draw.text((padding, padding), text, font=font, fill="white")

    # 画像を保存
    image.save("mahjong_hand.png")

if __name__ == "__main__":
    hand = generate_hand()
    create_image(hand)
    print(f"Generated hand: {''.join(hand)}")
