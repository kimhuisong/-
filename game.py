import os
import sys
import pygame
import math
import random

# 初期設定
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("クリスマスゲーム")

# 色の設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'images')
music_dir = os.path.join(current_dir,'music')

if not os.path.exists(images_dir):
    print(f"画像ディレクトリが存在しません: {images_dir}")
    sys.exit()

# 画像の読み込み
try:
    background_image = pygame.image.load(os.path.join(images_dir, 'background.png'))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    santa_image = pygame.image.load(os.path.join(images_dir, 'santa.png'))
    santa_image = pygame.transform.scale(santa_image, (200, 200))

    comic_image = pygame.image.load(os.path.join(images_dir, 'comic.png'))  # 漫画
    comic_image = pygame.transform.scale(comic_image, (50, 50))

    clothes_image = pygame.image.load(os.path.join(images_dir, 'clothes.png'))  # 洋服
    clothes_image = pygame.transform.scale(clothes_image, (50, 50))

    game_image = pygame.image.load(os.path.join(images_dir, 'game.png'))  # ゲーム
    game_image = pygame.transform.scale(game_image, (50, 50))




    # 家の画像をリストに格納
    house_images = []
    for i in range(1, 5):
        house_image = pygame.image.load(os.path.join(images_dir, f'home{i}.png'))
        house_image = pygame.transform.scale(house_image, (100, 100))
        house_images.append(house_image)
except pygame.error as e:
    print(f"画像の読み込みに失敗しました: {e}")
    sys.exit()

#BGMの読み込み
try:
    pygame.mixer.music.load(os.path.join(music_dir, 'jinglebell.wav'))
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"効果音の読み込みに失敗しました: {e}")
    sys.exit()

#効果音の読み込み
try:
    present_sound = pygame.mixer.Sound(os.path.join(music_dir,'throw.wav'))
except pygame.error as e:
    print(f"効果音の読み込みに失敗しました: {e}")
    sys.exit()

# サンタの位置（固定）
santa_x = 50
santa_y = 200


# プレゼントの種類
PRESENT_TYPES = {
    "comic": comic_image,
    "clothes": clothes_image,
    "game": game_image
}

# プレゼントリスト
items = []

# 家リスト
houses = []

# 日本語フォント設定
try:
    font = pygame.font.SysFont("meiryo", 24)  # meiryoフォントを使用
except:
    font = pygame.font.Font(None, 24)

# ゲーム制限時間
game_duration = 60
score = 0

# サンタの回転動作に関する変数
santa_rotation_angle = 0  # 現在の回転角度
santa_is_throwing = False  # サンタが投げ動作中かどうか
throw_start_time = 0  # 投げ動作の開始時間

# アイテムクラス
class Item:
    def __init__(self, x, y, image, item_type, angle=-50, speed=10):
        self.x = x
        self.y = y
        self.image = image
        self.item_type = item_type

        # 投げる角度と速度を基に水平・垂直速度を計算
        self.velocity_x = speed * math.cos(math.radians(angle))
        self.velocity_y = -speed * math.sin(math.radians(angle))

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

# 家クラス
class House:
    def __init__(self, x):
        self.x = x
        self.y = screen_height - 90
        self.image = random.choice(house_images)  # ランダムに家の画像を選択
        self.want = random.choice(list(PRESENT_TYPES.keys()))  # 欲しいプレゼントをランダムに選択

    def update(self):
        self.x -= 2

    def draw(self, screen):
        # 家の画像を描画
        screen.blit(self.image, (self.x, self.y))

        # 吹き出しの描画
        bubble_width = 60
        bubble_height = 60
        bubble_x = self.x + self.image.get_width() // 2 - bubble_width // 2
        bubble_y = self.y - bubble_height - 10
        pygame.draw.ellipse(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height))
        pygame.draw.ellipse(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2)

        # 欲しいプレゼントの画像を吹き出し内に描画
        want_image = PRESENT_TYPES[self.want]
        want_image_scaled = pygame.transform.scale(want_image, (40, 40))
        screen.blit(want_image_scaled, (bubble_x + 10, bubble_y + 10))

# 家の生成
def generate_house():
    max_attempts = 10
    for _ in range(max_attempts):
        new_x = screen_width
        overlap = False
        for house in houses:
            if abs(house.x - new_x) < 150:  # 距離が150未満なら重なりとみなす
                overlap = True
                break
        if not overlap:
            houses.append(House(new_x))
            break

# スタート画面用の背景画像を読み込み
try:
    start_background_image = pygame.image.load(os.path.join(images_dir, 'start_background.png'))
    # 背景画像を画面サイズにフィットさせるようにスケーリング
    bg_width, bg_height = start_background_image.get_size()
    scale_ratio = min(screen_width / bg_width, screen_height / bg_height) * 1.2
    new_width = int(bg_width * scale_ratio)
    new_height = int(bg_height * scale_ratio)
    start_background_image = pygame.transform.scale(start_background_image, (new_width, new_height))

    start_santa_image = pygame.image.load(os.path.join(images_dir,'start_santa.png'))
    start_santa_image = pygame.transform.scale(start_santa_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"スタート画面用背景画像の読み込みに失敗しました: {e}")
    sys.exit()

# スコアランキングファイル
score_file = os.path.join(current_dir, "scores.txt")

# スコアをロードする関数
def load_scores():
    if not os.path.exists(score_file):
        return []
    with open(score_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines if line.strip()]

# スコアを保存する関数
def save_scores(new_score):
    scores = load_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]  # トップ5を保持
    with open(score_file, "w", encoding="utf-8") as f:
        for score in scores:
            f.write(f"{score}\n")

# スタート画面
def start_screen():
    # 1. ランキング表示ページ
    show_ranking_screen()
    # 2. 遊び方説明ページ
    show_instructions_screen()

def show_ranking_screen():
    # メダル画像の読み込み
    gold_medal = pygame.image.load(os.path.join(images_dir, "Gold_medal.png"))
    silver_medal = pygame.image.load(os.path.join(images_dir, "Silver_medal.png"))
    bronze_medal = pygame.image.load(os.path.join(images_dir, "Bronz_medal.png"))

    # メダル画像をスケール調整
    medal_size = (50, 50)
    gold_medal = pygame.transform.scale(gold_medal, medal_size)
    silver_medal = pygame.transform.scale(silver_medal, medal_size)
    bronze_medal = pygame.transform.scale(bronze_medal, medal_size)

    # 背景画像の描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # 背景画像の上に半透明の黒いレイヤーを追加
    dark_overlay = pygame.Surface((screen_width, screen_height))
    dark_overlay.set_alpha(80)  # 透明度（0〜255、値が大きいほど不透明）
    dark_overlay.fill((0, 0, 0))  # 黒いレイヤー
    screen.blit(dark_overlay, (0, 0))

    # ランキングタイトル
    title_font = pygame.font.SysFont("meiryo", 50, bold=True)
    title_text = title_font.render("ランキング", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 10))

    # ランキングデータをロード
    scores = load_scores()
    if not scores:  # スコアがない場合はデフォルトの0を表示
        scores = [0, 0, 0, 0, 0]

    # ランキングのフォントサイズ設定
    font_sizes = [40, 30, 30, 24, 24]  # 1位～5位のフォントサイズ
    y_positions = [screen_height // 4, screen_height // 4 + 70, screen_height // 4 + 140, screen_height // 4 + 210, screen_height // 4 + 260]

    # 順位ごとの色設定（1位～3位に金・銀・銅色を適用）
    colors = [
        (255, 215, 0),  # 金色
        (192, 192, 192),  # 銀色
        (205, 127, 50),  # 銅色
        WHITE,  # 4位以降は白色
        WHITE,
    ]

    # ランキングリストの表示
    for i, score in enumerate(scores[:5]):  # 上位5位を表示
        rank_font = pygame.font.SysFont("meiryo", font_sizes[i], bold=True)
        rank_text = rank_font.render(f"{i + 1}位: {score}", True, colors[i])

        # メダルの位置
        medal_x = screen_width // 4  # メダルは左側に表示
        medal_y = y_positions[i] - 10  # 少し調整して中央に揃える

        # スコアテキストの位置
        score_x = medal_x + 60  # メダルの右側にスコアを表示
        score_y = y_positions[i]

        # メダルを描画
        if i == 0:
            screen.blit(gold_medal, (medal_x, medal_y))
        elif i == 1:
            screen.blit(silver_medal, (medal_x, medal_y))
        elif i == 2:
            screen.blit(bronze_medal, (medal_x, medal_y))

        # スコアテキストを描画
        screen.blit(rank_text, (score_x, score_y))

    # スタート画面に戻るメッセージ
    return_text = pygame.font.SysFont("meiryo", 30, bold=True).render(
        "Enterキーでスタート画面に戻る", True, RED
    )
    screen.blit(return_text, (screen_width // 2 - return_text.get_width() // 2, screen_height - 130))

    pygame.display.flip()

    # 入力待ちループ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_instructions_screen():
    # 背景画像の描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # 薄暗いレイヤーを追加
    dark_overlay = pygame.Surface((screen_width, screen_height))
    dark_overlay.set_alpha(120)  # 透明度（0〜255）
    dark_overlay.fill((0, 0, 0))  # 黒いレイヤー
    screen.blit(dark_overlay, (0, 0))

    # 「ゲームの遊び方」のタイトル
    title_font = pygame.font.SysFont("meiryo", 60, bold=True)  # 大きなフォント
    title_text = title_font.render("ゲームの遊び方", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 12))

    # 説明文のリスト
    instructions = [
        "1. 家の欲しいプレゼントを見極めて、正しく届けよう！",
        "2. 欲しいプレゼントは家の上に表示されるよ。",
        "3. キーボードで対応するキーを押して投げてね！",
    ]

    # 描画開始位置（中央に寄せるための計算）
    text_y = screen_height // 6 + 60
    instruction_font = pygame.font.SysFont("meiryo", 28)  # 通常サイズの白フォント

    # 説明文の描画（中央寄せ）
    for line in instructions:
        text = instruction_font.render(line, True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text_y))
        text_y += 50  # 行間を空ける

    # プレゼント選択肢を横に並べて表示
    options = [
        ("１：ゲーム", game_image),
        ("２：洋服", clothes_image),
        ("３：漫画", comic_image),
    ]

    # 横並びの配置設定
    option_spacing = 180  # 各選択肢の間隔
    start_x = (screen_width - (len(options) * option_spacing)) // 2  # 横方向の開始位置
    option_y = text_y + 50  # プレゼントの選択肢を表示するY座標

    for i, (text, image) in enumerate(options):
        # 各選択肢のX座標を計算
        option_x = start_x + i * option_spacing

        # テキストを描画
        option_font = pygame.font.SysFont("meiryo", 24, bold=True)
        option_text = option_font.render(text, True, WHITE)
        text_x = option_x + (option_spacing // 2 - option_text.get_width() // 2)  # テキストを中央揃え
        screen.blit(option_text, (text_x, option_y + 60))

        # 画像をテキストの上に描画
        image_scaled = pygame.transform.scale(image, (70, 70))
        image_x = option_x + (option_spacing // 2 - image_scaled.get_width() // 2)  # 画像を中央揃え
        screen.blit(image_scaled, (image_x, option_y - 20))  # 画像のY座標を調整

    # 制限時間の説明
    time_font = pygame.font.SysFont("meiryo", 28, bold=True)
    time_text = time_font.render("制限時間: 60秒", True, WHITE)
    screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, option_y + 140))

    # スタートメッセージ
    start_text = pygame.font.SysFont("meiryo", 32, bold=True).render(
        "Enterキーで開始", True, RED
    )
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height - 50))

    # 描画を反映
    pygame.display.flip()

    # 入力待ちループ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enterキーでゲーム開始
                    waiting = False





def main_game():
    global score, santa_is_throwing, santa_rotation_angle, throw_start_time
    start_ticks = pygame.time.get_ticks()
    running = True
    while running:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, game_duration - int(elapsed_time))

        if remaining_time <= 0:
            running = False

        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # キー入力処理
            if event.type == pygame.KEYDOWN:
                # アイテムを生成する位置を計算
                item_start_x = santa_x + santa_image.get_width() - 20  # サンタ画像の右端付近
                item_start_y = santa_y + santa_image.get_height() // 2 - 10  # サンタ画像の中央付近

                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    # サンタが投げる動作
                    santa_is_throwing = True
                    santa_rotation_angle = -20  # サンタを少し左に傾ける
                    throw_start_time = pygame.time.get_ticks()  # 投げ動作の開始時間

                    # 投げるアイテムを生成
                    if event.key == pygame.K_1:
                        items.append(Item(item_start_x, item_start_y, game_image, "game"))
                    elif event.key == pygame.K_2:
                        items.append(Item(item_start_x, item_start_y, clothes_image, "clothes"))
                    elif event.key == pygame.K_3:
                        items.append(Item(item_start_x, item_start_y, comic_image, "comic"))

                    # 効果音を再生
                    present_sound.play()

        if random.randint(0, 100) < 5:
            generate_house()

        for house in houses:
            house.update()
            house.draw(screen)

        items_to_remove = []
        houses_to_remove = []
        for item in items:
            item.update()
            item.draw(screen)

            for house in houses:
                if house.x <= item.x <= house.x + 100 and house.y <= item.y <= house.y + 100:
                    if house.want == item.item_type:
                        score += 10
                    else:
                        score -= 5
                    items_to_remove.append(item)
                    houses_to_remove.append(house)
                    break

        for item in items_to_remove:
            if item in items:
                items.remove(item)
        for house in houses_to_remove:
            if house in houses:
                houses.remove(house)

        # サンタの描画処理
        if santa_is_throwing:
            rotated_santa_image = pygame.transform.rotate(santa_image, santa_rotation_angle)
            rotated_rect = rotated_santa_image.get_rect(center=(santa_x + santa_image.get_width() // 2, santa_y + santa_image.get_height() // 2))
            screen.blit(rotated_santa_image, rotated_rect.topleft)

            if pygame.time.get_ticks() - throw_start_time > 300:
                santa_is_throwing = False
                santa_rotation_angle = 0
        else:
            screen.blit(santa_image, (santa_x, santa_y))

        # プレゼントの選択肢を右上に表示
        option_font = pygame.font.SysFont("meiryo", 24, bold=True)
        options = [
            ("1 :  ", game_image),
            ("2 :  ", clothes_image),
            ("3 :  ", comic_image),
        ]

        # オプション描画の開始位置
        option_x = screen_width - 150  # 右端から少し離した位置
        option_y = 20  # 上端から少し下がった位置
        option_spacing = 70  # 各選択肢の縦方向の間隔

        for i, (number, image) in enumerate(options):
            # 番号テキストの描画
            text = option_font.render(number, True, WHITE)
            screen.blit(text, (option_x, option_y + i * option_spacing))

            # 画像の描画
            image_scaled = pygame.transform.scale(image, (40, 40))
            screen.blit(image_scaled, (option_x + 50, option_y + i * option_spacing))

        # タイマーとスコアの表示
        time_text = font.render(f"[Time]: {remaining_time}", True, WHITE)
        score_text = font.render(f"[Score]: {score}", True, WHITE)
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (180, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    game_over_screen()


def game_over_screen():
    global score

    # スコアをランキングに記録
    save_scores(score)

    # 背景画像を描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # ゲームオーバー画面の説明文
    instructions = [
        "ゲーム終了！",
        f"最終スコア: {score}",
        "もう一度プレイするにはRキーを押してください",
    ]

    # 説明文の描画位置を計算
    text_y = screen_height // 2 - 60  # 中央付近に配置
    for line in instructions:
        text_color = RED if line.startswith("ゲーム終了") or line.startswith("最終スコア") else WHITE
        text = font.render(line, True, text_color)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text_y))
        text_y += 40  # 行間を調整

    # 描画を反映
    pygame.display.flip()

    # 入力待ちループ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    start_screen()  # スタート画面に戻る


# 実行
start_screen()
main_game()
pygame.quit()